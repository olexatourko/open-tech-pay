/* Placeholder submissions */
var submissions = ko.observableArray([]);

var perks = ko.observableArray();
var locations = ko.observableArray();
var employment_types = ko.observableArray();
var roles = ko.observableArray();
var techs = ko.observableArray();
var educations = ko.observableArray();
var number_of_employers = ko.observable();

requirejs.config({
  packages: [{
    name: 'moment',
    location: 'static/packages/moment',
    main: 'moment'
  }]
});

require(['static/components', 'moment'], function() {
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

    var moment = require('moment');
    jQuery.getJSON('fetch_submissions', function(data) {
        data.forEach(function(submission) {
            local_date = moment(submission['created_at']).format('YYYY-MM-DD');
            submission['created_at'] = local_date;
        });

        if ('randomize_market_data' in config && config['randomize_market_data']) {
            shuffle_array(data);
        }
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


/**
 * Shuffles array in place.
 * @param {Array} a items An array containing the items.
 */
function shuffle_array(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
}