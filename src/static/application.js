/* Placeholder submissions */
var submissions = ko.observableArray([
    {
        'pay_range': 'C$55,000.00 - C$59,999.99',
        'employment_type': 'Full-Time',
        'perks': 'Yearly Bonus, Food / Drinks',
        'roles': 'Web: Backend Developer',
        'tech': 'PHP, MySQL, Linux',
        'years_experience': 2,
        'education': 'Completed Bachelor\'s Degree',
        'years_with_current_employer': 1,
        'number_of_employers': 2
    },
    {
        'pay_range': 'C$60,000.00 - C$64,999.99',
        'perks': 'Quarterly Bonus',
        'employment_type': 'Full-Time',
        'roles': 'Web: Full-Stack',
        'tech': 'Python, MySQL, Javascript, HTML, CSS',
        'years_experience': 5,
        'education': 'Completed Bachelor\'s Degree',
        'years_with_current_employer': 2,
        'number_of_employers': 2
    }
]);

var email = ko.observableArray();
var pay_ranges = ko.observableArray();
var perks = ko.observableArray();
var employment_types = ko.observableArray();
var roles = ko.observableArray();
var techs = ko.observableArray();
var educations = ko.observableArray();
var years_with_current_employer = ko.observable();
var years_experience = ko.observable();
var number_of_employers = ko.observable();

var selected_pay_range = ko.observable();
var selected_perks = ko.observableArray();
var selected_employment_type = ko.observable();
var selected_roles = ko.observableArray();
var selected_techs = ko.observableArray();
var selected_education = ko.observable();

require(['static/components'], function() {
    function page_view_model() {
        var self = this;
        // http://www.knockmeout.net/2012/05/using-ko-native-pubsub.html
        // http://knockoutjs.com/documentation/fn.html
        self.message_bus = new ko.subscribable();
    }

    jQuery(function() {
        var view_model = page_view_model()
        ko.applyBindings(view_model);

        fetch_pay_ranges();
        fetch_employment_types();
        fetch_educations();
        fetch_perks();
        fetch_roles();
        fetch_techs();
    });
});

function fetch_pay_ranges() {
    pay_ranges.removeAll();
    jQuery.getJSON('fetch_pay_ranges', function(data) {
        ko.utils.arrayPushAll(pay_ranges, data);
    });
}

function fetch_employment_types() {
    employment_types.removeAll();
    jQuery.getJSON('fetch_employment_types', function(data) {
        ko.utils.arrayPushAll(employment_types, data);
    });
}

function fetch_educations() {
    educations.removeAll();
    jQuery.getJSON('fetch_educations', function(data) {
        ko.utils.arrayPushAll(educations, data);
    });
}

function fetch_perks() {
    perks.removeAll();
    jQuery.getJSON('fetch_perks', function(data) {
        ko.utils.arrayPushAll(perks, data);
    });
}

function fetch_roles() {
    roles.removeAll();
    jQuery.getJSON('fetch_roles', function(data) {
        ko.utils.arrayPushAll(roles, data);
    });
}

function fetch_techs() {
    techs.removeAll();
    jQuery.getJSON('fetch_techs', function(data) {
        ko.utils.arrayPushAll(techs, data);
    });
}