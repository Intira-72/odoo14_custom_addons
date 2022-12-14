from odoo import api, models
from bahttext import bahttext


class CustomInvoice(models.AbstractModel):
    _name = 'report.om_custom_invoice_print.custom_invoices_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        print(bahttext(docs.amount_total))
        return {
              'doc_ids': docids,
              'doc_model': 'account.move',
              'docs': docs,
              'data': data,
              'some_code': self.some_code(docs.invoice_origin),
              'inv_move_line': self.inv_move_line(docs.invoice_line_ids),
              'amout_bahttext': f"( {bahttext(docs.amount_total)} )"
        }

    def some_code(self, inv_id):
        rtn = self.env['sale.order'].search([('name', '=', inv_id)])
        return rtn.store_id.name


    def inv_move_line(self, invoice_line_ids):
        inv_list = []

        for inv in invoice_line_ids:
            data = {
                'p_code': inv.product_id.default_code,
                'p_name': inv.product_id.product_tmpl_id.name,
                'quantity': f"{inv.quantity:,.0f}",
                'price_unit': f"{inv.price_unit:,.2f}",
                'price_subtotal': f"{inv.price_subtotal:,.2f}",
            }

            inv_list.append(data)

        return inv_list

    