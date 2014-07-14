# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import fields, osv

class purchase_config_settings(osv.osv_memory):
    _inherit = 'purchase.config.settings'
    _columns = {
        'limit_amount_02': fields.integer('limit to require a second approval',required=True,
            help="Amount after which validation of purchase is required."),
    }

    _defaults = {
        'limit_amount_02': 10000,
    }

    def get_default_limit_amount(self, cr, uid, fields, context=None):
        ir_model_data = self.pool.get('ir.model.data')
        transition = ir_model_data.get_object(cr, uid, 'purchase_double_validation', 'trans_waiting_validated_router')
        field, value = transition.condition.split('<', 1)
        return {'limit_amount_02': int(value)}

    def set_limit_amount(self, cr, uid, ids, context=None):
        ir_model_data = self.pool.get('ir.model.data')
        config = self.browse(cr, uid, ids[0], context)
        waiting = ir_model_data.get_object(cr, uid, 'purchase_double_validation', 'trans_validated_router')
        waiting.write({'condition': 'amount_total >= %s' % config.limit_amount})
        confirm = ir_model_data.get_object(cr, uid, 'purchase_double_validation', 'trans_waiting_validated_router')
        confirm.write({'condition': 'amount_total < %s' % config.limit_amount})

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    
    STATE_SELECTION = [
        ('draft', 'Request for Quotation'),
        ('wait', 'Waiting'),
        ('confirmed', 'Waiting Approval'),
        ('validated', 'Waiting Validation'),
        ('approved', 'Approved'),
        ('except_picking', 'Shipping Exception'),
        ('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]
    
    _columns = {
        'state': fields.selection(STATE_SELECTION, 'State', readonly=True, help="The state of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' state. Then the order has to be confirmed by the user, the state switch to 'Confirmed'. Then the supplier must confirm the order to change the state to 'Approved'. When the purchase order is paid and received, the state becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the state becomes in exception.", select=True),
    }
    
    def action_validated(self, cr, uid, ids, context=None):
        """ Sets state to validated.
        @return: True
        """
        self.write(cr, uid, ids, {'state':'validated'})
        return True
    
purchase_order()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

