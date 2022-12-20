odoo.define('om_makro_order_import_xml.action_import_orders', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
        buttons_template: 'makro_import_orders_button.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_import_orders': '_OpenImportWizard',
        }),
        _OpenImportWizard: function () {
            var self = this;
             this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'makro_orders.wizard',
                name :'Import Orders',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                res_id: false,
            });
        }
     });
var ImportOrdersListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TreeButton,
}),
});
    viewRegistry.add('button_import_orders', ImportOrdersListView);
});