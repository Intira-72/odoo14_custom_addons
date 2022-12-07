odoo.define('mapping_products_name.action_import_sale_order', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
        buttons_template: 'import_sale_order_button.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_list_button_upload': '_OpenWizard',
        }),
        _OpenWizard: function () {
            var self = this;
             this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'import.sale.order.wiz',
                name :'Import Product Sale Order List',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                res_id: false,
            });
        }
     });
var SaleOrderListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TreeButton,
}),
});
    viewRegistry.add('button_in_tree', SaleOrderListView);
});