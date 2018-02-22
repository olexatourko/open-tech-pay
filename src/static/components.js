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

        /* Functions used by template */
        self.get_pay_range_text = function(item) {
            return 'C$' + number_with_commas(item.lower) + ' - C$' + number_with_commas(item.upper);
        }
        self.on_submit = function() {
            console.log(self.selected_pay_range());
            console.log(self.selected_perks());
        };

    },
    template: { require: 'text!static/knockout-templates/create-submission.html' }
});

/* Utilities */
const number_with_commas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}