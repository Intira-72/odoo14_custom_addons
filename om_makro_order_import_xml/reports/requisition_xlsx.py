from odoo import models

class RequisitionReportXLSX(models.AbstractModel):
    _name = 'report.om_makro_order_import_xml.report_requisition_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    
    def _header_requisition(self, ids):
        order_lines = self.env['sale.order.line'].search([('order_id', 'in', [order.id for order in ids.order_ids])])       
        product_lists = []

        for order in order_lines:
            if order.product_id.id not in [i['id'] for i in product_lists]:
                m_info = self.env['om_makro_order_import_xml.makro_products_maching_line'].search([('product_id', '=', order.product_id.id)], order='create_date desc', limit=1)

                product_attr = f" ({order.product_id.product_template_attribute_value_ids.name})" if order.product_id.product_template_attribute_value_ids else ""

                product_lists.append({'id': order.product_id.id,
                                    'name': {
                                        'short_name': m_info.categ_name if m_info.categ_name else "-",
                                        'brand': order.product_id.brand if order.product_id.brand else "-",
                                        'series': f"{m_info.default_code}{ product_attr }" if m_info.default_code else "-",
                                    }})

        data = {
            'date': ids.create_date.replace(hour=ids.create_date.hour+7).strftime('%d/%m/%Y %H:%M'),
            'code_no': int(ids.name),
            'scheduled_date': ids.delivery_date.strftime('%d/%m/%Y'),
            'zone': "MK-" + ids.zone_id.name,
            't_header': sorted(product_lists, key=lambda d: d['id'])
        }


        data['t_data'] = self._order_lists(order_lines, [p['id'] for p in data['t_header']])

        return data


    def _order_lists(self, order_ids, product_ids):
        order_lists = []
        sum_total = [0 for o in product_ids] + [0]

        for order in order_ids:
            order_dict = {}
            product_lists = [0 for o in product_ids]

            order_no = str(order.order_id.client_order_ref)
            
            if order_no in [o['store_po'] for o in order_lists]:                
                in_dex = order_lists.index(next(item for item in order_lists if item["store_po"] == order_no))
                order_lists[in_dex]['product_list'][product_ids.index(order.product_id.id)] = order.product_uom_qty
            else:
                order_dict['store'] = order.order_id.partner_id.display_name
                order_dict['store_po'] = order_no
                
                product_lists[product_ids.index(order.product_id.id)] = order.product_uom_qty
                order_dict['product_list'] = product_lists            

                order_lists.append(order_dict)

        for r_order in order_lists:
            sum_order = sum(r_order['product_list'])
            r_order['product_list'].append(sum_order)
            
            for r in range(len(r_order['product_list'])):                
                sum_total[r] += r_order['product_list'][r]
                
        order_lists.append(sum_total)
        return order_lists

   
    def generate_xlsx_report(self, workbook, data, requisition):
        reqs = self._header_requisition(requisition)         

        sheet = workbook.add_worksheet(f'{reqs["zone"]}')
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 15)      

        cell_format = workbook.add_format()
        cell_format.set_font_name('AngsanaUPC')
        cell_format.set_font_size(16)  

        col_header_format = workbook.add_format()
        col_header_format.set_align('center')
        col_header_format.set_align('vcenter')
        col_header_format.set_font_name('AngsanaUPC')
        col_header_format.set_font_size(22)
        col_header_format.set_border(2)

        p_col_format = workbook.add_format()
        p_col_format.set_align('center')
        p_col_format.set_align('vcenter')
        p_col_format.set_font_name('AngsanaUPC')
        p_col_format.set_font_size(16)
        p_col_format.set_shrink()
        p_col_format.set_border(2)        

        sheet.merge_range('A1:B1', f'วันที่ {reqs["date"]} น.', cell_format)
        sheet.merge_range('A2:B2', f'กำหนดส่ง {reqs["scheduled_date"]}', cell_format)
        sheet.write('C2', f'{reqs["zone"]}', cell_format)
        sheet.write(0, len(reqs['t_header']) + 3, reqs["code_no"], cell_format)

        sheet.merge_range('A3:A5', f'No.', p_col_format)
        sheet.merge_range('B3:B5', f'สาขา', col_header_format)
        sheet.merge_range('C3:C5', f'Store.PO', col_header_format)

        col = 2
        for i in reqs['t_header']:
            col += 1
            sheet.write(2, col, f'{i["name"]["short_name"]}', p_col_format)
            sheet.write(3, col, f'{i["name"]["brand"]}', p_col_format)
            sheet.write(4, col, f'{i["name"]["series"]}', p_col_format)

        sheet.set_column(3, col, 15)

        sheet.set_column(col+1, col+1, 15)
        sheet.merge_range(2, col+1, 4, col+1, f'รวม', col_header_format)

        t_data_format = workbook.add_format()
        t_data_format.set_font_name('AngsanaUPC')
        t_data_format.set_font_size(16)
        t_data_format.set_align('center')
        t_data_format.set_align('vcenter')
        t_data_format.set_border(1)

        s_data_format = workbook.add_format()
        s_data_format.set_font_name('AngsanaUPC')
        s_data_format.set_font_size(16)
        s_data_format.set_align('center')
        s_data_format.set_align('vcenter')
        s_data_format.set_border(1)
        s_data_format.set_right(2)

        no_format = workbook.add_format()
        no_format.set_font_name('AngsanaUPC')
        no_format.set_font_size(16)
        no_format.set_align('center')
        no_format.set_align('vcenter')
        no_format.set_border(1)
        no_format.set_left(2)        

        row_count = 0
        try:            
            for order_data in reqs['t_data']:
                row_count += 1
                sheet.write(row_count+4, 0, f'{row_count}', no_format)
                sheet.write(row_count+4, 1, f'{order_data["store"]}', t_data_format)
                sheet.write(row_count+4, 2, f'{order_data["store_po"]}', s_data_format)

                o_col = 3
                for order_qty in order_data["product_list"]:
                    sheet.write(row_count+4, o_col, int(order_qty), s_data_format)
                    o_col += 1
            
        except TypeError:
            b_data_format = workbook.add_format()
            b_data_format.set_font_name('AngsanaUPC')
            b_data_format.set_font_size(36)
            b_data_format.set_bold()
            b_data_format.set_align('center')
            b_data_format.set_align('vcenter')
            b_data_format.set_border(2)

            sheet.merge_range(row_count + 4, 0, row_count + 4, 2, f'รวม', b_data_format)
            t_col = 2
            
            for r_sum in reqs['t_data'][-1]:
                t_col += 1
                sheet.write(row_count+4, t_col, r_sum, b_data_format)

        workbook.close()

