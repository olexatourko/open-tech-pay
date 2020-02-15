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
    });
});

function fetch_submissions(submissions) {
    if (submissions) {
        submissions.removeAll();
    } else {
        submissions = ko.observableArray([]);
    }

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

    return submissions;
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