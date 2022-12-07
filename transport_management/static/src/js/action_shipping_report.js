odoo.define('transport_management.action_shipping_report', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
        buttons_template: 'shipping_report_button.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_shipping_report': '_OpenReportWizard',
        }),
        _OpenReportWizard: function () {
            var self = this;
             this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'transport.report.wizard',
                name :'Shipping Report',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                res_id: false,
            });
        }
     });
var ShippingReportListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TreeButton,
}),
});
    viewRegistry.add('button_shipping_report', ShippingReportListView);
});