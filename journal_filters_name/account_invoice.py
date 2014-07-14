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

class account_move(osv.osv):
    _name = 'account.move'
    _inherit ='account.move'
    def _get_reference(self, cr, uid, ids, field_name, arg, context=None):
        res = {}

        for rec in self.browse(cr,uid,ids,context=context):
            reference_result = ""

            for rec_lines in rec.line_id:
                reference_result = reference_result + ' | '+ rec_lines.name
                
            res[rec.id] = reference_result

        return res

    _columns = {
            'reference_account_lines': fields.function(_get_reference, string="Referencia de Apuntes Contables", method=True, type='char', size=512, store=True, readonly=True),
                }

    _default = {
        }

    # def copy(self, cr, uid, id, default=None, context=None):
    #     if not default:
    #         default = {}
    #     default.update({
    #                     'reference_account_lines': False, 
                        
    #                     })
    #     return super(account_move, self).copy(cr, uid, id, default, context=context)

account_move()