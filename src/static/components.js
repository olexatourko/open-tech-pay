/* Single Selectors */
ko.components.register('pay-range-selector', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.options = params.options;
        self.onclick = function() {
            self.messageBus.notifySubscribers(this, 'pay_range_selected');
        }

        self.get_options_text = function(item) {
            return 'C$' + number_with_commas(item.lower) + ' - C$' + number_with_commas(item.upper);
        }
    },
    template: { require: 'text!static/knockout-templates/selector.html' }
});

ko.components.register('employment-type-selector', {
    viewModel: function(params) {
        var self = this;
        self.messageBus = params.message_bus;
        self.options = params.options;
        self.onclick = function() {
            self.messageBus.notifySubscribers(this, 'employment_type_selected');
        }

        self.get_options_text = function(item) {
            return item.name
        }
    },
    template: { require: 'text!static/knockout-templates/selector.html' }
});

ko.components.register('education-selector', {
    viewModel: function(params) {
        var self = this;
        self.messageBus = params.message_bus;
        self.options = params.options;
        self.onclick = function() {
            self.messageBus.notifySubscribers(this, 'education_selected');
        }

        self.get_options_text = function(item) {
            return item.name
        }
    },
    template: { require: 'text!static/knockout-templates/selector.html' }
});

/*Multiselectors*/
ko.components.register('perks-selector', {
    viewModel: function(params) {
        var self = this;
        self.messageBus = params.message_bus;
        self.options = params.options;
        self.onclick = function() {
            self.messageBus.notifySubscribers(this, 'perks_selected');
        }

        self.get_options_text = function(item) {
            return item.name
        }
    },
    template: { require: 'text!static/knockout-templates/multi-selector.html' }
});
ko.components.register('roles-selector', {
    viewModel: function(params) {
        var self = this;
        self.messageBus = params.message_bus;
        self.options = params.options;
        self.onclick = function() {
            self.messageBus.notifySubscribers(this, 'roles_selected');
        }

        self.get_options_text = function(item) {
            return item.name
        }
    },
    template: { require: 'text!static/knockout-templates/multi-selector.html' }
});
ko.components.register('techs-selector', {
    viewModel: function(params) {
        var self = this;
        self.messageBus = params.message_bus;
        self.options = params.options;
        self.onclick = function() {
            self.messageBus.notifySubscribers(this, 'techs_selected');
        }

        self.get_options_text = function(item) {
            return item.name
        }
    },
    template: { require: 'text!static/knockout-templates/multi-selector.html' }
});

/* Utilities */
const number_with_commas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}