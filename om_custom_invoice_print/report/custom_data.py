from odoo import api, models
from bahttext import bahttext


class CustomInvoice(models.AbstractModel):
    _name = 'report.om_custom_invoice_print.custom_invoices_template'

    @api.model
    def _get_report_values(self, docids, data=[]):
        docs = self.env['account.move'].browse(docids)

        # for doc in docs:
        #     data.append({
        #         'some_code': self.some_code(doc.invoice_origin),
        #         'inv_move_line': self.inv_move_line(doc.invoice_line_ids),
        #         'state_name': 'กรุงเทพมหานคร' if doc.partner_id.state_id.name == 'กรุงเทพ' else doc.partner_id.state_id.name,
        #         'amout_bahttext': f"( {bahttext(doc.amount_total)} )"
        #     })
        
        return {
                'doc_ids': docids,
                'doc_model': 'account.move',
                'docs': docs,
                'data': data,
                'some_code': self.some_code(docs.invoice_origin),
                'inv_move_line': self.inv_move_line(docs.invoice_line_ids),
                'state_name': 'กรุงเทพมหานคร' if docs.partner_id.state_id.name == 'กรุงเทพ' else docs.partner_id.state_id.name,
                'amout_bahttext': f"( {bahttext(docs.amount_total)} )"       
        }


    def some_code(self, inv_id):
        rtn = self.env['sale.order'].search([('name', '=', inv_id)]).m_data_file.buyer_id.name
        return rtn


    def inv_move_line(self, invoice_line_ids):
        inv_list = []

        for inv in invoice_line_ids:
            m_product_id = self.env['om_makro_order_import_xml.makro_products_maching_line'].search([('product_id', '=', inv.product_id.id)])

            data = {
                'p_code': m_product_id.m_product_id.makro_code,
                'p_name': m_product_id.m_product_id.name,
                'quantity': f"{inv.quantity:,.0f}",
                'price_unit': f"{inv.price_unit:,.2f}",
                'price_subtotal': f"{inv.price_subtotal:,.2f}",
            }

            inv_list.append(data)

        return inv_list

    