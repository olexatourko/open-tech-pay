/* Placeholder submissions */
var submissions = ko.observableArray([]);

var perks = ko.observableArray();
var locations = ko.observableArray();
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
        fetch_fields();
    });
});

function fetch_submissions() {
    submissions.removeAll();
    jQuery.getJSON('fetch_submissions', function(data) {
        ko.utils.arrayPushAll(submissions, data);
    });
}

function fetch_fields() {
    employment_types.removeAll();
    locations.removeAll();
    educations.removeAll();
    perks.removeAll();
    roles.removeAll();
    techs.removeAll();

    jQuery.getJSON('fetch_fields', function(data) {
        ko.utils.arrayPushAll(employment_types, data['employment_types']);
        ko.utils.arrayPushAll(locations, data['locations']);
        ko.utils.arrayPushAll(educations, data['educations']);
        ko.utils.arrayPushAll(perks, data['perks']);
        ko.utils.arrayPushAll(roles, data['roles']);
        ko.utils.arrayPushAll(techs, data['techs']);
    });
}