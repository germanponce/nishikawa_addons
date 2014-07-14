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

# Products => Herencia de Cuentas
class product_product(osv.osv):
    _name = 'product.product'
    _inherit ='product.product'

    _columns = {
        'analytics_accounts_required': fields.boolean('Cuentas Analiticas Requeridas',help='Si esta Casilla Esta activada, sera necesario incluir la cuenta en cada linea de producto en: Compras,Facturas Proveedor, Solicitudes de Compra, Ventas, Facturas Cliente y Presupuestos') ,
        }


    _default = {
        }

product_product()