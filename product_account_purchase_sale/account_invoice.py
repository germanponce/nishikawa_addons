# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2010 moylop260 - http://www.hesatecnica.com.com/
#    All Rights Reserved.
#    info skype: german_442 email: (german.ponce@hesatecnica.com)
############################################################################
#    Coded by: german_442 email: (german.ponce@hesatecnica.com)
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
from openerp import SUPERUSER_ID

class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit ='account.invoice'
    _columns = {
        'department_id': fields.many2one('hr.department', 'Departamento', help='Define el Departamento encargado de la Solicitud de la Compra' ),
        }

    _default = {
        }
account_invoice()
class account_invoice_line(osv.osv):
    _inherit ='account.invoice.line'
    _columns = {
        'analytics_accounts_required': fields.boolean('Cuentas Analiticas Requeridas') ,
    }
    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, context=None, company_id=None):
        value = {}
        if context is None:
            context = {}
        company_id = company_id if company_id != None else context.get('company_id',False)
        context = dict(context)
        context.update({'company_id': company_id, 'force_company': company_id})
        if not partner_id:
            raise osv.except_osv(_('No Partner Defined!'),_("You must first select a partner!") )
        if not product:
            if type in ('in_invoice', 'in_refund'):
                return {'value': {}, 'domain':{'product_uom':[]}}
            else:
                return {'value': {'price_unit': 0.0}, 'domain':{'product_uom':[]}}
        part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        fpos_obj = self.pool.get('account.fiscal.position')
        fpos = fposition_id and fpos_obj.browse(cr, uid, fposition_id, context=context) or False

        if part.lang:
            context.update({'lang': part.lang})
        result = {}
        res = self.pool.get('product.product').browse(cr, uid, product, context=context)

        if type in ('out_invoice','out_refund'):
            a = res.property_account_income.id
            if not a:
                a = res.categ_id.property_account_income_categ.id
        else:
            a = res.property_account_expense.id
            if not a:
                a = res.categ_id.property_account_expense_categ.id
        a = fpos_obj.map_account(cr, uid, fpos, a)
        if a:
            result['account_id'] = a

        if type in ('out_invoice', 'out_refund'):
            taxes = res.taxes_id and res.taxes_id or (a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False)
        else:
            taxes = res.supplier_taxes_id and res.supplier_taxes_id or (a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False)
        tax_id = fpos_obj.map_tax(cr, uid, fpos, taxes)

        if type in ('in_invoice', 'in_refund'):
            result.update( {'price_unit': price_unit or res.standard_price,'invoice_line_tax_id': tax_id} )
        else:
            result.update({'price_unit': res.list_price, 'invoice_line_tax_id': tax_id})
        result['name'] = res.partner_ref

        result['uos_id'] = uom_id or res.uom_id.id
        if res.description:
            result['name'] += '\n'+res.description

        domain = {'uos_id':[('category_id','=',res.uom_id.category_id.id)]}

        res_final = {'value':result, 'domain':domain}

        if not company_id or not currency_id:
            return res_final

        company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
        currency = self.pool.get('res.currency').browse(cr, uid, currency_id, context=context)

        if company.currency_id.id != currency.id:
            if type in ('in_invoice', 'in_refund'):
                res_final['value']['price_unit'] = res.standard_price
            new_price = res_final['value']['price_unit'] * currency.rate
            res_final['value']['price_unit'] = new_price

        if result['uos_id'] and result['uos_id'] != res.uom_id.id:
            selected_uom = self.pool.get('product.uom').browse(cr, uid, result['uos_id'], context=context)
            new_price = self.pool.get('product.uom')._compute_price(cr, uid, res.uom_id.id, res_final['value']['price_unit'], result['uos_id'])
            res_final['value']['price_unit'] = new_price
        #### Validamos que el producto requiera las cuentas Analiticas
        prod_obj = self.pool.get('product.product')
        prod_b = prod_obj.browse(cr, uid, [product], context=None)[0]
        if prod_b.analytics_accounts_required:
            res_final['value'].update({'analytics_accounts_required':True})
        return res_final
account_invoice_line()


class account_account_template(osv.osv):
    _name = "account.account.template"
    _inherit = "account.account.template"
    _columns = {
        'name': fields.char('Name', size=256, required=True, select=True, translate=True),
                }
account_account_template()

class account_account(osv.osv):
    _name = "account.account"
    _inherit = "account.account"
    _columns = {
        'name': fields.char('Name', size=256, required=True, select=True, translate=True),
                }
account_account()