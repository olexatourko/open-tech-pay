ko.components.register('market-data', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.submissions = params.submissions;
        self.show_all = ko.observable(false);
        self.table_submissions = ko.pureComputed(function() {
            if (self.show_all()) {
                return self.submissions();
            } else {
                return self.submissions().slice(0, 3);
            }

        }, this);

        self.toggle_shown = function() {
            self.show_all(!self.show_all());
        }
        self.show_detailed_view = ko.observable(false);
        self.view_button_text = ko.computed(function() {
            if (!self.show_all()) {
                return 'Show All (' + submissions().length + ')';
            } else {
                return 'Show Less';
            }
        }, this);

        /* Functions used by template */
        self.get_pay_range_text = function(item) {
            return '$' + number_with_commas(item.lower) + ' - $' + number_with_commas(item.upper);
        }
    },
    template: { require: 'text!static/knockout-templates/market-data.html' }
});

ko.components.register('create-submission', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.inner_message_bus = new ko.subscribable();

        self.email = ko.observable();
        self.years_experience = ko.observable();
        self.number_of_employers = ko.observable();
        self.years_with_employer = ko.observable();

        self.pay_ranges = params.pay_ranges;
        self.employment_types = params.employment_types;
        self.perks = params.perks;
        self.roles = params.roles;
        self.techs = params.techs;
        self.educations = params.educations,

        self.selected_pay_range = ko.observable();
        self.selected_perks = ko.observableArray();
        self.selected_employment_type = ko.observable();
        self.selected_roles = ko.observableArray();
        self.selected_techs = ko.observableArray();
        self.selected_education = ko.observable();

        self.server_errors = ko.observableArray();

        self.email_focused = ko.observable();
        self.last_email_status = ko.observable('');
        self.email_focused.subscribe(function(newValue) {
           if (!newValue && self.email()) {
                jQuery.getJSON('check_email', { 'email': self.email() }, function(data) {
                    if (data.status == 'error') {
                        self.last_email_status('error');
                    } else if (data.whitelisted) {
                        self.last_email_status('whitelisted');
                    } else {
                        self.last_email_status('');
                    }
                });
           }
        });

        self.unselected_perks = ko.computed(function() {
            arr = ko.observableArray();
            self.perks().forEach(function(value) {
                if (self.selected_perks().indexOf(value) == -1) {
                    arr.push(value);
                }
            });
            return arr();
        }, this);
        self.unselected_roles = ko.computed(function() {
            arr = ko.observableArray();
            self.roles().forEach(function(value) {
                if (self.selected_roles().indexOf(value) == -1) {
                    arr.push(value);
                }
            });
            return arr();
        }, this);
        self.unselected_techs = ko.computed(function() {
            arr = ko.observableArray();
            self.techs().forEach(function(value) {
                if (self.selected_techs().indexOf(value) == -1) {
                    arr.push(value);
                }
            });
            return arr();
        }, this);

        /* Functions used by template */
        self.get_pay_range_text = function(item) {
            return '$' + number_with_commas(item.lower) + ' - $' + number_with_commas(item.upper);
        }

        self.on_submit = function(item, event) {
            var button = event.target;
            var form = jQuery(button).parents('form').get(0);

            /* Perform frontend validation on the form */
            if (!jQuery(form).parsley().validate()) {
                return;
            }

            var mapper_function = function(item) {
               return 'id' in item ?  {'id': item.id} : {'name': item.name}
             };

            /* Build the request data */
            var data = {
                'email': self.email(),
                'years_experience': self.years_experience(),
                'number_of_employers': self.number_of_employers(),
                'years_with_current_employer': self.years_with_employer(),
                'pay_range': self.selected_pay_range().id,
                'employment_type': self.selected_employment_type().id,
                'education': self.selected_education().id,
                'perks': self.selected_perks().map(mapper_function),
                'roles': self.selected_roles().map(mapper_function),
                'techs': self.selected_techs().map(mapper_function)
            }
            var form_data = new FormData();
            form_data.append('payload', JSON.stringify(data));

            jQuery.ajax({
                url: '/submit',
                type: 'POST',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                success: function(data) {
                    if(data.status == 'ok') {
                        self.server_errors.removeAll();
                        self.message_bus.notifySubscribers({}, 'submission_success');
                    } else if(data.status == 'error') {
                        self.server_errors.removeAll();
                        ko.utils.arrayPushAll(self.server_errors, data.errors);
                    }
                }
            });
        };

        /* Check if the array has an object by case-insensitive name */
        var _in_array = function(arr, name) {
            for (i = 0; i < arr.length; i++) {
                if(arr[i].name.toLowerCase() == name.toLowerCase()) {
                    return true;
                }
            };
            return false;
        };

        / *Listen to internal events */
        /* Perks --------------------*/
        self.inner_message_bus.subscribe(function(perk) {
            var in_selected = _in_array(self.selected_perks(), perk.name);
            if(in_selected) { return; }
            self.selected_perks.push(perk);
        }, {}, 'perk_selected')

        self.inner_message_bus.subscribe(function(text) {
            var in_listed = _in_array(self.perks(), text);
            var in_selected = _in_array(self.selected_perks(), text);
            if(in_listed || in_selected) { return; }
            self.selected_perks.push({
                name: text
            });
        }, {}, 'custom_perk_selected')

        self.inner_message_bus.subscribe(function(role) {
            self.selected_perks.remove(role);
        }, {}, 'perk_unselected')


        /* Roles --------------------*/
        self.inner_message_bus.subscribe(function(role) {
            var in_selected = _in_array(self.selected_roles(), role.name);
            if(in_selected) { return; }
            self.selected_roles.push(role);
        }, {}, 'role_selected')

        self.inner_message_bus.subscribe(function(text) {
            var in_listed = _in_array(self.roles(), text);
            var in_selected = _in_array(self.selected_roles(), text);
            if(in_listed || in_selected) { return; }
            self.selected_roles.push({
                name: text
            });

        }, {}, 'custom_role_selected')
        self.inner_message_bus.subscribe(function(role) {
            self.selected_roles.remove(role);
        }, {}, 'role_unselected')


        /* Techs --------------------*/
        self.inner_message_bus.subscribe(function(tech) {
            var in_selected = _in_array(self.selected_techs(), tech.name);
            if(in_selected) { return; }
            self.selected_techs.push(tech);
        }, {}, 'tech_selected')

        self.inner_message_bus.subscribe(function(text) {
            var in_listed = _in_array(self.techs(), text);
            var in_selected = _in_array(self.selected_techs(), text);
            if(in_listed || in_selected) { return; }
            self.selected_techs.push({
                name: text
            });
        }, {}, 'custom_tech_selected')

        self.inner_message_bus.subscribe(function(tech) {
            self.selected_techs.remove(tech);
        }, {}, 'tech_unselected')
    },
    template: { require: 'text!static/knockout-templates/create-submission.html' }
});


/* Elements */
ko.components.register('tag', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.item = params.item;
        self.button_text = params.button_text;
        self.event_name = params.event_name;

        self.on_click = function(item, event) {
            self.message_bus.notifySubscribers(self.item, self.event_name);
        };
    },
    template: { require: 'text!static/knockout-templates/tag.html' }
});
ko.components.register('custom-tag', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.button_text = params.button_text;
        self.event_name = params.event_name;
        self.text = ko.observable('');

        self.on_click = function(item, event) {
            if(self.text().length > 0) {
                self.message_bus.notifySubscribers(self.text(), self.event_name);
                self.text('');
            }
        };
        self.on_keydown = function(item, event) {
            if (event.keyCode == 13 && self.text().length > 0) {
                self.message_bus.notifySubscribers(self.text(), self.event_name);
                self.text('');
                event.stopPropagation();
            }

            return true;
        }
    },
    template: { require: 'text!static/knockout-templates/custom-tag.html' }
});

/* Utilities */
const number_with_commas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}