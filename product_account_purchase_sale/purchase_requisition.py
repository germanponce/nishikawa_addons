# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################


from osv import osv, fields
import time
from datetime import datetime, date
from tools.translate import _
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class purchase_requisition(osv.osv):
    _name = 'purchase.requisition'
    _inherit ='purchase.requisition'
    _columns = {
        'department_id': fields.many2one('hr.department', 'Departamento', help='Define el Departamento encargado de la Solicitud de la Compra', required=True),
        }

    def _get_department(self, cr, uid, context=None):
        department_obj = self.pool.get('hr.department')
        department_id = department_obj.search(cr, uid, [('manager_id','=',uid)])
        return department_id[0] if department_id else False

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):
        res = super(purchase_requisition, self).make_purchase_order(cr, uid, ids, partner_id, context=None)
        rec = self.browse(cr, uid, ids, context=None)[0]
        purchase_id = res[rec.id]
        purchase_obj = self.pool.get('purchase.order')
        purchase_order_line = self.pool.get('purchase.order.line')
        res_partner = self.pool.get('res.partner')
        fiscal_position = self.pool.get('account.fiscal.position')
        supplier = res_partner.browse(cr, uid, partner_id, context=context)
        supplier_pricelist = supplier.property_product_pricelist_purchase or False
        for purchase in purchase_obj.browse(cr, uid, [purchase_id], context=None):
            purchase.write({
                            'department_id': rec.department_id.id,
                            })
            for line in purchase.order_line:
                line.unlink()
        for line in rec.line_ids:
            product = line.product_id
            seller_price, qty, default_uom_po_id, date_planned = self._seller_details(cr, uid, line, supplier, context=context)
            taxes_ids = product.supplier_taxes_id
            taxes = fiscal_position.map_tax(cr, uid, supplier.property_account_position, taxes_ids)
            purchase_order_line.create(cr, uid, {
                'order_id': purchase_id,
                'name': product.partner_ref+'\n'+line.comments,
                'product_qty': qty,
                'product_id': product.id,
                'product_uom': default_uom_po_id,
                'price_unit': seller_price,
                'date_planned': date_planned,
                'taxes_id': [(6, 0, taxes)],
                #### Revisar estas Lineas, para poder validar si se queda aqui o con la validacion de confirmacion en compras
                'analytics_accounts_required': line.product_id.analytics_accounts_required,
            }, context=context)           
        return res
    _defaults = {
        'department_id': _get_department,
        }

purchase_requisition()

class purchase_requisition_line(osv.osv):
    _name = 'purchase.requisition.line'
    _inherit ='purchase.requisition.line'
    _columns = {
        'comments': fields.text('Comentarios', help='Comentarios acerca de la compra de este Producto'),
        }
    _default = {
        }
purchase_requisition_line()

# class purchase_requisition_partner(osv.osv_memory):
#     _name = 'purchase.requisition.partner'
#     _inherit ='purchase.requisition.partner'
#     _columns = {
#         }
#     _defaults = {
#         }
#     def create_order(self, cr, uid, ids, context=None):
#         res = super(purchase_requisition_partner, self).create_order(cr, uid, ids, context=context)
#         print "################################### resultado final", res
#         print "################################### resultado final", res
#         print "################################### resultado final", res
#         print "################################### resultado final", res
#         print "################################### resultado final", res
#         return res

# purchase_requisition_partner()