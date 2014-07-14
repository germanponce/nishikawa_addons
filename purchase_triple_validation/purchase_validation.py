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

from openerp.osv import fields, osv
from tools.translate import _
import netsvc

class purchase_order(osv.osv):
    _inherit = 'purchase.order'

    _columns = {
    'approved_directive': fields.boolean('Aprobado por el Directivo'),
    'amount_directive': fields.boolean('Monto Limite Sobrepasado'),
    }
    
    def purchase_directive_approve(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'approved_directive': True, 'amount_directive': False})
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'purchase.order', ids[0], 'purchase_approve', cr)
        return True

    def wkf_approve_order(self, cr, uid, ids, context=None):
        res = super(purchase_order, self). wkf_approve_order(cr, uid, ids, context=None)
        config_obj = self.pool.get('parametros.config')
        config_id = config_obj.search(cr, uid, [])
        config = config_obj.browse(cr, uid, config_id, context=None)[0]
        monto_limite = config.limite_compra ## Este se tiene que parametrizar
        for rec in self.browse(cr, uid, ids, context=None):
            if rec.amount_total >= monto_limite:
                if rec.approved_directive == False:
                    raise osv.except_osv(
                            _('Error !'),
                            _('Se supero el Monto Limite Definido, se debe Aprobar por algun Directivo del Grupo: [Purchase / Aprobacion Directiva]\n ó Contacte al Administrador.'))
        return res

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        res = super(purchase_order, self). wkf_confirm_order(cr, uid, ids, context=None)
        config_obj = self.pool.get('parametros.config')
        config_id = config_obj.search(cr, uid, [])
        config = config_obj.browse(cr, uid, config_id, context=None)[0]
        monto_limite = config.limite_compra ## Este se tiene que parametrizar
        for rec in self.browse(cr, uid, ids, context=None):
            if rec. amount_total >= monto_limite:
                rec.write({'amount_directive': True})
        return res

    def copy(self, cr, uid, id, default=None, context=None):
        purchase = self.browse(cr, uid, id, context=context)
        if not default:
            default = {}
        default.update({
                        'approved_directive'          : False, 
                        'amount_directive'    : False, 
                        
                        })
        return super(purchase_order, self).copy(cr, uid, id, default, context=context)
purchase_order()

class parametros_config(osv.osv):
    _name = 'parametros.config'
    _description = 'Parametros para Validaciones'
    _rec_name = 'limite_compra' 
    _columns = {
        'limite_compra': fields.float('Limite Maximo para Compras', digits=(14,2), required=True, help='Este Monto es utilizado para Validar las Compras Maximas por el Encargado de Compras'),
    }

    _defaults = {  
        'limite_compra': 5000,
        }
    def _check_config(self, cr, uid, ids):
        config_obj = self.pool.get('parametros.config')
        config_id = config_obj.search(cr, uid, [('id','!=',ids)])
        if config_id:
            return False
        return True

    _constraints = [(_check_config, 'Error: Solo debe Existir un Registro de Configuracion', ['parametros']), ] 
parametros_config()

