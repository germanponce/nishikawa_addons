
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
#
#
#    info skype: german_442 email: (german.ponce@hesatecnica.com)
############################################################################
#    Coded by: german_442 email: (german_442@hotmail.com)
#
##############################################################################

from osv import osv, fields
from tools.translate import _
from tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, date
import decimal_precision as dp
import time
import netsvc
import base64
import csv
import StringIO

class supplier_payment_export(osv.osv_memory):
    _name = 'supplier.payment.export'
    _description = 'Importacion de Inventarios por Codigo EAN13'
    _columns = {
        # 'csv_file': fields.binary('Archivo CSV', filters="*.csv", required=True),
        'csv_file': fields.char('Nombre Archivo CSV', size=256, required=True),
        'name': fields.char('Referencia del Pago', required=True, help='Indica en el Pago de Clientes la Referencia por el monto que se esta transfiriendo a su Cuenta, Ejemplo: Pago de Enero por Productos XXX, Esta referencia se puede editar en el Archivo CSV'),
        'date': fields.datetime('Fecha y Hora', required=True),
        'bank_selection': fields.selection([('banamex','Banamex')],'Tipo', required=True),
        'export_lines': fields.one2many('supplier.payment.export.line','export_id', 'Detalle de Pagos', help='Para indicar el Tipo de Pago por Proveedor basta con ponerselo a una sola linea de cada proveedor.'),
        # 'date_start': fields.date('Fecha Inicio', required=True),
        # 'date_end': fields.date('Fecha Fin', required=True),
        'visible_lines': fields.boolean('Ver lineas'),
        'select_partner': fields.boolean('Seleccionar Proveedor'),
        'partner_id': fields.many2one('res.partner','Proveedor'),
        'amount_global_total': fields.float('Total', digits=(14,2)),
        'company_id': fields.many2one('res.company', 'Compañia', required=True),
    }

    def on_change_export_lines(self, cr, uid, ids, date_start, date_end, context=None):
        vals = {}
        if date_start and date_end:
            vals['visible_lines']=True
            ### Aqui va toda la operacion para los pagos de los proveedores
        return {'value':vals}

    def on_change_load_lines(self, cr, uid, ids, date, context=None):
        vals = {}
        vals['visible_lines']=True
        ###### AQUI CARGAMOS TODO EL PROCESO PARA MOSTRAR LAS LINEAS DE TODOS
        ###### LOS VENDEDORES QUE TIENEN EL CHECK PAGO MEDIANTE CSV ACTIVO
        invoice_obj = self.pool.get('account.invoice')
        partner_obj = self.pool.get('res.partner')
        partner_payment_csv_ids = partner_obj.search(cr, uid, [('payment_csv','=',True)])
        if partner_payment_csv_ids:
            export_lines = []
            amount_global_total = 0.0
            invoice_ids = invoice_obj.search(cr, uid, [('type','=','in_invoice'),('state','=','open'),('partner_id','in',tuple(partner_payment_csv_ids))])
            print "### Comienza lo bueno"
            for invoice in invoice_obj.browse(cr, uid, invoice_ids, context=None):
                print "################### FACTURA", invoice.number
                print "################### FACTURA", invoice.number
                print "################### FACTURA", invoice.number
                amount_global_total += invoice.amount_total
                xline = (0,0,{
                    'partner_id': invoice.partner_id.id,
                    'date_payment': date,
                    'invoice_id': invoice.id,
                    'date_invoice': invoice.date_invoice,
                    'date_end': invoice.date_due,
                    'amount_total': invoice.amount_total,
                    })
                export_lines.append(xline)
            if export_lines:
                vals['export_lines'] = [x for x in export_lines]
                vals['amount_global_total'] = amount_global_total
        return {'value':vals}

    def on_change_load_lines_partner(self, cr, uid, ids, partner_id, date, context=None):
        vals = {}
        vals['visible_lines']=True
        ###### AQUI CARGAMOS TODO EL PROCESO PARA MOSTRAR LAS LINEAS DE TODOS
        ###### LOS VENDEDORES QUE TIENEN EL CHECK PAGO MEDIANTE CSV ACTIVO
        invoice_obj = self.pool.get('account.invoice')
        # partner_obj = self.pool.get('res.partner')
        # partner_payment_csv_ids = partner_obj.search(cr, uid, [('payment_csv','=',True)])
        if partner_id:
            export_lines = []
            amount_global_total = 0.0
            invoice_ids = invoice_obj.search(cr, uid, [('type','=','in_invoice'),('state','=','open'),('partner_id','=',partner_id)])
            print "### Comienza lo bueno"
            for invoice in invoice_obj.browse(cr, uid, invoice_ids, context=None):
                print "################### FACTURA", invoice.number
                print "################### FACTURA", invoice.number
                print "################### FACTURA", invoice.number
                amount_global_total += invoice.amount_total
                xline = (0,0,{
                    'partner_id': invoice.partner_id.id,
                    'date_payment': date,
                    'invoice_id': invoice.id,
                    'date_invoice': invoice.date_invoice,
                    'date_end': invoice.date_due,
                    'amount_total': invoice.amount_total,
                    })
                export_lines.append(xline)
            if export_lines:
                vals['export_lines']=False
                vals.update({'export_lines':[x for x in export_lines]})
                vals['amount_global_total'] = amount_global_total
        return {'value':vals}

    def _get_company(self, cr, uid, context=None):
        company_id = 0
        user_obj = self.pool.get('res.users')
        user_br = user_obj.browse(cr, uid, [uid], context=None)[0]
        if user_br.company_id:
            company_id = user_br.company_id.id
        return company_id

    _defaults = {  
        'date': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'bank_selection': 'banamex',
        'company_id': _get_company,
        }

    def export_csv_file(self, cr, uid, ids, context=None):
        #TODO : OpenERP Business Process 
        
        return True
supplier_payment_export()

class supplier_payment_export_line(osv.osv_memory):
    _name = 'supplier.payment.export.line'
    _description = 'Lineas del Asistente de Exportacion de Pagos'
    _columns = {
        'type_payment': fields.selection([('INTB','INTB'),('BNMX','BNMX'),('REF','REF')], 'Tipo de Pago'),
        #'csv_file': fields.binary('Archivo CSV', readonly=True),
        'partner_id': fields.many2one('res.partner','Proveedor', required=True),
        'export_id': fields.many2one('supplier.payment.export', 'ID Referencia'),
        'date_payment': fields.date('Fecha de Pago'),
        'invoice_id': fields.many2one('account.invoice','Factura', required=True, help='Este Campo Indica por que Factura estamos creando el Pago del Proveedor' ),
        'date_invoice': fields.date('Fecha de Factura', required=True),
        'date_end': fields.date('Fecha de Vencimiento', required=True),
        'amount_total': fields.float('Monto de la Factura', digits=(14,2), required=True),
    }
    _defaults = {  
        'date_payment': lambda *a: datetime.now().strftime('%Y-%m-%d'),
        }
    _order = 'partner_id'
supplier_payment_export_line()


class supplier_payment_model(osv.osv):
    _name = 'supplier.payment.model'
    _description = 'Listade de Archivos CSV de Pago a Proveedores'
    _columns = {
        'csv_file': fields.binary('Archivo CSV', readonly=True),
        'csv_file_name': fields.char('Nombre Archivo CSV', size=256, required=True),
        'name': fields.char('Referencia del Pago', required=True),
        'date': fields.datetime('Fecha y Hora', required=True),
        'bank_selection': fields.selection([('banamex','Banamex')],'Tipo', required=True),
        'amount_total': fields.float('Monto de Pago', digits=(14,2), required=True),
        'supplier_ids': fields.many2many('res.partner','supplier_payment_csv_rel','payment_csv_id','partner_id','Proveedores'),
    }
    _defaults = {  
        }
    _order = 'date' 

supplier_payment_model