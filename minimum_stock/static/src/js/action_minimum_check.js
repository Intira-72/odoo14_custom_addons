odoo.define('minimum_stock.action_minimum_check', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
        buttons_template: 'minimum_check_button.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_minimum_check': '_MinimumCheck',
        }),
        _MinimumCheck: function () {
            var self = this;
            this._rpc({
                model: 'below.stock',
                method: 'minimum_check_list',
                args: [[],]
            }).then(function () {
                window.location.reload();
            });
        }
     });
var MinimumStockView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TreeButton,
}),
});
    viewRegistry.add('minimum_check_to_list', MinimumStockView);
});