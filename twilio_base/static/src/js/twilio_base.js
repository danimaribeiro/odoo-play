odoo.define('twilio_base', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Model = require('web.Model');
    var session = require('web.session');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var webclient = require('web.web_client');

    var QWeb = core.qweb;
    var _t = core._t;

    var OpenDialer = Widget.extend({
        template: 'twilio_base.phone.dial',
        start: function() {
            session.rpc("/twilio/token", {}).then(function (data) {
                Twilio.Device.setup(data);
                Twilio.Device.ready(function (device) {
                    alert('twilio pronto');
                });
            });
        },
        events: {
            'click .num': 'on_link_analytics_settings',
            'click .btn-twilio-call': 'on_click_make_call',
            'click .btn-twilio-hangup': 'on_click_disconnect',
        },
        on_link_analytics_settings: function(ev) {
            var self = this;
            var $target = $(ev.currentTarget);
            var num = $target.data('num');
            this.$('#dial-twilio-number').val(this.$('#dial-twilio-number').val() + num);
        },
        on_click_make_call: function(e){
            var params = {
                To: this.$('#dial-twilio-number').val()
            };
            console.log('Calling ' + params.To + '...');
            Twilio.Device.connect(params);
        },
        on_click_disconnect: function(e){
            Twilio.Device.disconnectAll();
        },
    });

    core.action_registry.add('twilio_base.open_dialer', OpenDialer);
});
