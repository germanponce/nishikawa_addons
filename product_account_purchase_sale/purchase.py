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

class purchase_order(osv.osv):
    _name = 'purchase.order'
    _inherit ='purchase.order'
    _columns = {
        'department_id': fields.many2one('hr.department', 'Departamento', help='Define el Departamento encargado de la Solicitud de la Compra' ),
        }

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        res = super(purchase_order, self). wkf_confirm_order(cr, uid, ids, context=None)
        
        for rec in self.browse(cr, uid, ids, context=None):
            for line in rec.order_line:
                if line.product_id.analytics_accounts_required == True and not line.account_analytic_id:
                    raise osv.except_osv(
                            _('Error !'),
                            _('El producto %s no tiene cuenta analitica indicada y el producto asi lo requiere \n Verifica la Ficha del Producto o Agrega la Cuenta Analitica en la Linea del Pedido.\n Contacte a su Administrador.\nGracias') % (line.product_id.name))
        attachment_obj = self.pool.get('ir.attachment')
        attachment_id = attachment_obj.search(cr, uid,[('res_model','=','purchase.order'),('res_id','=',ids[0])])
        if not attachment_id:
            raise osv.except_osv(
                _('Error !'),
                _('No se puede Confirmar un Pedido de Compra sin la Cotizacion PDF del Proveedor Adjunta como Referencia.\n Gracias!,'))
        return res

    def view_invoice(self, cr, uid, ids, context=None):
        res = super(purchase_order, self).view_invoice(cr, uid, ids, context=context)
        invoice_id = res['res_id']
        rec = self.browse(cr, uid, ids, context=None)[0]
        invoice_obj = self.pool.get('account.invoice')
        invoice_obj.write(cr, uid, [invoice_id], {'department_id':rec.department_id.id}, context=None)
        return res
    _default = {
        }
purchase_order()

class purchase_order_line(osv.osv):
    _name = 'purchase.order.line'
    _inherit ='purchase.order.line'
    _columns = {
        'analytics_accounts_required': fields.boolean('Cuentas Analiticas Requeridas') ,
        }

    _default = {
        }

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}

        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_supplierinfo = self.pool.get('product.supplierinfo')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        dummy, name = product_product.name_get(cr, uid, product_id, context=context_partner)[0]
        if product.description_purchase:
            name += '\n' + product.description_purchase
        res['value'].update({'name': name})

        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if context.get('purchase_uom_check') and self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.date.context_today(self,cr,uid,context=context)


        supplierinfo = False
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if (qty or 0.0) < min_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})

        # - determine price_unit and taxes_id
        if pricelist_id:
            price = product_pricelist.price_get(cr, uid, [pricelist_id],
                    product.id, qty or 1.0, partner_id or False, {'uom': uom_id, 'date': date_order})[pricelist_id]
        else:
            price = product.standard_price

        taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
        fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
        taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})
        
        #### Validamos que el producto requiera las cuentas Analiticas
        prod_obj = self.pool.get('product.product')
        prod_b = prod_obj.browse(cr, uid, [product_id], context=None)[0]
        if prod_b.analytics_accounts_required:
            res['value'].update({'analytics_accounts_required':True})
        return res
purchase_order_line()

# class purchase_order(osv.osv):
#     _name = 'purchase.order.line'
#     _inherit ='purchase.order.line'
#     _columns = {
#         'analytics_accounts_required': fields.boolean('Cuentas Analiticas Requeridas') ,

#         }

#     _default = {
#         }

#     def onchange_product_analytic(self, cr, uid, ids, product_id, context=None):
#         print "############ PRODUCT ID", product_id
#         prod_obj = self.pool.get('product.product')
#         prod_br = prod_obj.browse(cr, uid, product_id, context=None)
#         ana_req = prod_br.analytics_accounts_required 
#         print "##################### CUENTA REQ", ana_req
#         res = {'analytics_accounts_required':ana_req}
#         return {'value':res}
# purchase_order()