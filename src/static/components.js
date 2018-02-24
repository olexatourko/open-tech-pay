ko.components.register('market-data', {
    viewModel: function(params) {
        var self = this;
        self.message_bus = params.message_bus;
        self.submissions = params.submissions;
        self.simple_view = ko.observable(true);

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
        self.pay_ranges = params.pay_ranges;
        self.employment_types = params.employment_types;
        self.years_with_employer = params.years_with_employer;
        self.roles = params.roles;
        self.techs = params.techs;
        self.educations = params.educations,
        self.years_experience = params.years_experience,
        self.number_of_employers = params.number_of_employers

        self.selected_pay_range = params.selected_pay_range;
        self.selected_perks = params.selected_perks;
        self.selected_employment_type = params.selected_employment_type;
        self.selected_roles = params.selected_roles;
        self.selected_techs = params.selected_techs;
        self.selected_education = params.selected_education;

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
    },
    template: { require: 'text!static/knockout-templates/create-submission.html' }
});

/* Utilities */
const number_with_commas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}