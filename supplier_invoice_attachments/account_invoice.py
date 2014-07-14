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
    _inherit ='account.invoice'
    _columns = {
        'validate_attachment': fields.boolean('Validar sin Factura y XML'),
    }

    def invoice_validate(self, cr, uid, ids, context=None):
        result =  super(account_invoice, self).invoice_validate(cr, uid, ids, context=context)

        attachment_obj = self.pool.get('ir.attachment')
        attachment_ids = []

        for rec in self.browse(cr, uid, ids, context=context):
            if rec.type == 'in_invoice':
                attachment_pdf_id = attachment_obj.search(cr, uid,[('res_model','=','account.invoice'),('res_id','=',rec.id),('name','like','.pdf')])
                attachment_xml_id = attachment_obj.search(cr, uid,[('res_model','=','account.invoice'),('res_id','=',rec.id),('name','like','.xml')])
                if not attachment_xml_id or not attachment_xml_id:
                    # group_obj = self.pool.get('res.groups')
                    # group_id = group_obj.search(cr, SUPERUSER_ID, [('name','in',('Financial Manager','Gestor Financiero'))])
                    # print "##################### GRUPO", group_id
                    # for group in group_obj.browse(cr, SUPERUSER_ID, group_id, context=None):

                    #     for user in group.users:
                    #         if user.id == uid: ### Si el que esta confirmando es un gestor Financiero entonces no pedira Validacion del  Asistente
                    #             return result
                    if rec.validate_attachment == False:
                        raise osv.except_osv(
                            _('Error !'),
                            _('No Puede Validar la Factura por que No tiene Adjuntos el PDF y XML, solicite al Manager de Contabilidad valide la Factura ...'))
        return result

    def copy(self, cr, uid, id, default=None, context=None):
        account = self.browse(cr, uid, id, context=context)
        if not default:
            default = {}
        default.update({
                        'validate_attachment': False, 
                        
                        })
        return super(account_invoice, self).copy(cr, uid, id, default, context=context)

account_invoice()

### CREACION DEL WIZARD PARA AUTORIZAR FACTURA
class account_invoice_validate(osv.osv_memory):
    _name = 'account.invoice.validate'
    _description = 'Asistente para Validar Facturas de Compra'
    _columns = {
    'password' : fields.char('Contraseña del Usuario', size=128, required=True),
    }
    _defaults = {  

        }

    def auth(self, cr, uid, ids, context=None):
        active_ids = context.get('active_ids', False)
        password = self.browse(cr, SUPERUSER_ID, ids, context=None)[0].password
        group_obj = self.pool.get('res.groups')
        group_id = group_obj.search(cr, SUPERUSER_ID, [('name','in',('Financial Manager','Gestor Financiero'))])
        users_obj = self.pool.get('res.users')
        user_list = []
        account_obj = self.pool.get('account.invoice')
        for group in group_obj.browse(cr, SUPERUSER_ID, group_id, context=None):
            for user in group.users:
                user_list.append(user.id)
        if user_list:
            user_ids = users_obj.search(cr, SUPERUSER_ID, [('password','=',password),('id','in',tuple(user_list))])
            if user_ids:
                if active_ids:
                    for account in account_obj.browse(cr, SUPERUSER_ID, active_ids, context=None):
                        ret = account.write({'validate_attachment':True})
                return ret
            else:
                raise osv.except_osv(
                        _('Error !'),
                        _('La Contraseña es Incorrecta o el Usuario no tiene Permisos.\n Consulte a su Administrador y Verifique \
                            que el usuario se encuentra en el Grupo [Financial Manager ó Gestor financiero]'))
        else:
            raise osv.except_osv(
                    _('Error !'),
                    _('La Contraseña es Incorrecta o el Usuario no tiene Permisos.\n Consulte a su Administrador y Verifique \
                        que el usuario se encuentra en el Grupo [Financial Manager ó Gestor financiero]'))
        return {'type' : 'ir.actions.act_window_close' }

account_invoice_validate()
