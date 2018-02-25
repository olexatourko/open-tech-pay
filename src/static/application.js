/* Placeholder submissions */
var submissions = ko.observableArray([]);

var pay_ranges = ko.observableArray();
var perks = ko.observableArray();
var employment_types = ko.observableArray();
var roles = ko.observableArray();
var techs = ko.observableArray();
var educations = ko.observableArray();
var number_of_employers = ko.observable();

require(['static/components'], function() {
    function page_view_model() {
        var self = this;
        self.submitted = ko.observable(false);

        // http://www.knockmeout.net/2012/05/using-ko-native-pubsub.html
        // http://knockoutjs.com/documentation/fn.html
        self.message_bus = new ko.subscribable();


        / *Listen to internal events */
        self.message_bus.subscribe(function(perk) {
            self.submitted(true);
        }, {}, 'submission_success')
    }

    /* Hack to prevent Return key from submitting the form */
    jQuery(document).on("keypress", 'form', function (e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            e.preventDefault();
            return false;
        }
    });

    jQuery(function() {
        var view_model = page_view_model()
        ko.applyBindings(view_model);

        fetch_submissions();
        fetch_pay_ranges();
        fetch_employment_types();
        fetch_educations();
        fetch_perks();
        fetch_roles();
        fetch_techs();
    });
});

function fetch_submissions() {
    submissions.removeAll();
    jQuery.getJSON('fetch_submissions', function(data) {
        ko.utils.arrayPushAll(submissions, data);
    });
}

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