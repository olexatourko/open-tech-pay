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

        self.pay_ranges = params.pay_ranges;
        self.employment_types = params.employment_types;
        self.years_with_employer = params.years_with_employer;
        self.perks = params.perks;
        self.roles = params.roles;
        self.techs = params.techs;
        self.educations = params.educations,
        self.years_experience = params.years_experience,
        self.number_of_employers = params.number_of_employers

        self.selected_pay_range = ko.observable();
        self.selected_perks = ko.observableArray();
        self.selected_employment_type = ko.observable();
        self.selected_roles = ko.observableArray();
        self.selected_techs = ko.observableArray();
        self.selected_education = ko.observable();

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
            jQuery.ajax({
                url: '/submit',
                type: 'POST',
                data: new FormData(form),
                processData: false,
                contentType: false,
                cache: false,
                success: function(data) {
                    if(data.status == 'ok') {
                        alert('Submission successful')
                    }
                }
            });

            self.message_bus.notifySubscribers({}, 'submission_created');
        };

        / *Listen to internal events */
        /* Perks */
        self.inner_message_bus.subscribe(function(role) {
            self.selected_perks.push(role);
        }, {}, 'perk_selected')
        self.inner_message_bus.subscribe(function(text) {
            self.selected_perks.push({
                name: text
            });
        }, {}, 'custom_perk_selected')
        self.inner_message_bus.subscribe(function(role) {
            self.selected_perks.remove(role);
        }, {}, 'perk_unselected')

        /* Roles */
        self.inner_message_bus.subscribe(function(role) {
            self.selected_roles.push(role);
        }, {}, 'role_selected')
        self.inner_message_bus.subscribe(function(text) {
            self.selected_roles.push({
                name: text
            });
        }, {}, 'custom_role_selected')
        self.inner_message_bus.subscribe(function(role) {
            self.selected_roles.remove(role);
        }, {}, 'role_unselected')

        /* Techs */
        self.inner_message_bus.subscribe(function(tech) {
            self.selected_techs.push(tech);
        }, {}, 'tech_selected')
        self.inner_message_bus.subscribe(function(text) {
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
        self.text = ko.observable();

        self.on_click = function(item, event) {
            if(self.text().length > 0) {
                self.message_bus.notifySubscribers(self.text(), self.event_name);
                self.text('');
            }
        };
    },
    template: { require: 'text!static/knockout-templates/custom-tag.html' }
});

/* Utilities */
const number_with_commas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}