ko.bindingHandlers.autoNumeric = {
    init: function(element, value_accessor) {
        var value = ko.unwrap(value_accessor());
        if (value != null) { element.value = value; }
        var auto_numeric = new AutoNumeric(element, {
            currencySymbol : '$',
            decimalCharacter : '.',
            digitGroupSeparator : ',',
            decimalPlaces: 0,
            minimumValue: 0,
            maximumValue: 1000000
        });
        value_accessor()(auto_numeric.getNumber()); // Set raw_value
        jQuery(element).on('autoNumeric:formatted', function() {
            value_accessor()(auto_numeric.getNumber());
        });
    },
    update: function(element, value_accessor) {
        var old_value = element.value;
        var value = ko.unwrap(value_accessor());
        if(value != null && old_value != value) {
            AutoNumeric.set(element, value);
        }
    }
};
ko.bindingHandlers.resizeOnChange = {
    update: function(element, value_accessor) {
        var value = ko.unwrap(value_accessor());
        var length = 1; // The default length
        if(value != null) {
            var length = value.toString().length;
            length = Math.round(length * 1.1);
        }
        length = Math.max(4, length);
        element.setAttribute('size', length);
    }
};

ko.components.register('market-data', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.submissions = params.submissions;
        self.show_all = ko.observable(false);
        self.min_display_number = params.min_display_number;
        self.table_submissions = ko.pureComputed(function() {
            if (self.show_all()) {
                return self.submissions();
            } else {
                return self.submissions().slice(0, self.min_display_number);
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
        self.get_salary_text = function(salary) {
            return '$' + number_with_commas(salary);
        }
        self.get_perk_text =  function(submission_to_perk) {
            var text = submission_to_perk.perk.name;
            if (submission_to_perk.value) {
                text += ' ($' + number_with_commas(submission_to_perk.value) + ')';
            }

            return text;
        }
    },
    template: { require: 'text!static/knockout-templates/market-data.html' }
});

ko.components.register('create-submission', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.inner_message_bus = new ko.subscribable();

        self.salary = ko.observable();
        self.email = ko.observable();
        self.years_experience = ko.observable();
        self.number_of_employers = ko.observable();
        self.years_with_employer = ko.observable();

        self.locations = params.locations;
        self.employment_types = params.employment_types;
        self.perks = params.perks;
        self.roles = params.roles;
        self.techs = params.techs;
        self.educations = params.educations,

        self.selected_perks = ko.observableArray();
        self.selected_location = ko.observable();
        self.selected_employment_type = ko.observable();
        self.selected_roles = ko.observableArray();
        self.selected_techs = ko.observableArray();
        self.selected_education = ko.observable();

        self.is_submitting = ko.observable(false);
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

        /* Verification form */
        self.display_verification_form = ko.observable(true);
        self.last_email_status.subscribe(function(newValue) {
            if (newValue == 'whitelisted') {
                self.display_verification_form(false)
            }
        });
        self.verification_profile_url = ko.observable();
        self.verification_employer_name = ko.observable();
        self.verification_notes = ko.observable();

        /* Submit logic */
        self.on_submit = function(item, event) {
            var button = event.target;
            var form = jQuery(button).parents('form').get(0);

            /* Perform frontend validation on the form */
            if (!jQuery(form).parsley().validate()) {
                return;
            }

            var mapper_function = function(item) {
                if ('id' in item) {
                    return {'id': item.id}
                } else {
                    return item;
                }
            };
            var perk_mapper_function = function(item) {
                to_return = item
                if ('id' in item) {
                    to_return = {'id': item.id};
                    if ('value' in item && item.value != null) {
                        to_return.value = item.value
                    }
                }
                return to_return;
            }

            /* Build the request data */
            var data = {
                'salary': self.salary(),
                'email': self.email(),
                'years_experience': self.years_experience(),
                'number_of_employers': self.number_of_employers(),
                'years_with_current_employer': self.years_with_employer(),
                'location': self.selected_location().id,
                'employment_type': self.selected_employment_type().id,
                'education': self.selected_education().id,
                'perks': self.selected_perks().map(perk_mapper_function),
                'roles': self.selected_roles().map(mapper_function),
                'techs': self.selected_techs().map(mapper_function)
            }

            /* If we're using a verification form, include that data too */
            if (self.display_verification_form() && self.last_email_status() != 'whitelisted') {
                data['verification_request'] = {
                    'profile_url': self.verification_profile_url(),
                    'employer_name': self.verification_employer_name(),
                    'notes': self.verification_notes()
                }
            }

            var form_data = new FormData();
            form_data.append('payload', JSON.stringify(data));

            self.is_submitting(true);
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
                        // Convert received JSON object into array of errors.
                        errorsArray = [];
                        Object.keys(data.errors).forEach(field => errorsArray.push([field, data.errors[field]]));
                        // Push to Knockout observable array
                        ko.utils.arrayPushAll(self.server_errors, errorsArray);
                    }
                    self.is_submitting(false);
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

        self.inner_message_bus.subscribe(function(item) {
            var in_listed = _in_array(self.perks(), item.text);
            var in_selected = _in_array(self.selected_perks(), item.text);
            if(in_listed || in_selected) { return; }
            self.selected_perks.push({
                name: item.text,
                value: item.value
            });
        }, {}, 'custom_perk_selected')

        self.inner_message_bus.subscribe(function(perk) {
            perk.value = null;
            self.selected_perks.remove(perk);
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


        /* Error Labels --------------------*/
        self.get_error_text = function(error) {
            var labels = {
                'email': 'Email',
                'roles': 'Roles',
                'perks': 'Perks',
                'techs': 'Technologies',
                'years_experience': 'Years Experience',
                'years_with_current_employer': 'Years With Current Employer'
            }

            var key = error[0];
            var message = error[1]
            if (key in labels) {
                return labels[key] + ": " + message;
            }

            return key + ": " + message;
        };
    },
    template: { require: 'text!static/knockout-templates/create-submission.html' }
});


/* Elements */
tag_view_model = function(params) {
    var self = this;
    self.message_bus = params.message_bus;
    self.item = params.item;
    self.button_text = params.button_text;
    self.event_name = params.event_name;

    self.on_click = function(item, event) {
        self = this;
        self.message_bus.notifySubscribers(self.item, self.event_name);
    };
};
custom_tag_view_model = function(params) {
    var self = this;
    self.message_bus = params.message_bus;
    self.button_text = params.button_text;
    self.event_name = params.event_name;
    self.text = ko.observable('');

    self.on_click = function(item, event) {
        self = this;
        if(self.text().length > 0) {
            self.message_bus.notifySubscribers(self.text(), self.event_name);
            self.text('');
        }
    };
    self.on_keydown = function(item, event) {
        self = this;
        if (event.keyCode == 13 && self.text().length > 0) {
            self.message_bus.notifySubscribers(self.text(), self.event_name);
            self.text('');
            event.stopPropagation();
        }

        return true;
    };
};

/* Tag subclasses */
value_tag_view_model = function(params) {
    tag_view_model.call(this, params);
    self = this;
    self.value = ko.observable(self.item.value);
    self.on_click = function(item, event) {
        self = this;
        self.item.value = self.value() ? self.value() : null;
        self.message_bus.notifySubscribers(self.item, self.event_name);
    };
};
value_tag_view_model.prototype = Object.create(tag_view_model.prototype);
value_tag_view_model.prototype.constructor = value_tag_view_model;

value_custom_tag_view_model = function(params) {
    custom_tag_view_model.call(this, params);
    self = this;
    self.value = ko.observable();
    self.on_click = function(item, event) {
        self = this;
        if(self.text().length > 0) {
            self.message_bus.notifySubscribers({
                text: self.text(),
                value: self.value() ? self.value() : null
            }, self.event_name);
            self.text('');
            self.value('');
        }
    };
    self.on_keydown = function(item, event) {
        self = this;
        if (event.keyCode == 13 && self.text().length > 0) {
            self.message_bus.notifySubscribers({
                text: self.text(),
                value: self.value() ? self.value() : null
            }, self.event_name);
            self.name('');
            self.value('');
            event.stopPropagation();
        }

        return true;
    };
};
value_custom_tag_view_model.prototype = Object.create(custom_tag_view_model.prototype);
value_custom_tag_view_model.prototype.constructor = value_custom_tag_view_model;

ko.components.register('tag', {
    viewModel: tag_view_model,
    template: { require: 'text!static/knockout-templates/tags/tag.html' }
});
ko.components.register('custom-tag', {
    viewModel: custom_tag_view_model,
    template: { require: 'text!static/knockout-templates/tags/custom-tag.html' }
});
ko.components.register('value-tag', {
    viewModel: value_tag_view_model,
    template: { require: 'text!static/knockout-templates/tags/value-tag.html' }
});
ko.components.register('value-custom-tag', {
    viewModel: value_custom_tag_view_model,
    template: { require: 'text!static/knockout-templates/tags/value-custom-tag.html' }
});

/* Utilities */
const number_with_commas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}