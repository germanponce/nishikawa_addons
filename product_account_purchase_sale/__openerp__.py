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
{
    'name': 'Cuenta Analitica Requerida',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "Nishikawa",
    'description': """

            Este modulo agrega ala Ficha de Producto 2 Opciones:
                - Cuenta Analitica para Compras: Esta Opcion permite que cada ves que se realice una Compra, Presupuesto ó Solicitud de Compra, la cuenta Analitica sea Requerida, por este producto. Esto Mismo Aplica para Facturas de Proveedores.
                    - Fomulario Producto --> Pestaña Abastecimiento --> Cuentas Analiticas Requeridas
                - Cuenta Analitica para Ventas: Igual que el punto anterior, cada vez que se crea una Venta la cuenta Analitica sera requerida. Aplicado para las Facturas de Clientes.
            Agrega en la Ficha de Solicitud de Compra:
                - Departamento Encargado de la Compra.
                - Descripcion del Producto que se esta Comprando.
                - El departamento se arrastra hasta el pedido y la factura.
            Solicitudes de Compra:
                - El campo Notas de los productos en las Solicitudes, se arrastra al pedido de Compra por cada Linea, se agrega despues de la descripcion del Proveedor.
            Validaciones:
                - No deja Confirmar un pedido que no tenga alguna cuenta analitica de alguna linea del pedido, las cuentas son requeridas si el producto tiene Activo el Check Box para requerirla.
                - No deja Validar un Pedido de Compra si no tiene Un Documento Adjunto(PDF de la Cotizacion del Proveedor).
                - No se puede Confirmar un Pedido de Compra si no se tiene el Reporte PDF del Proveedor como archivo adjunto.
            Contabilidad:
                - El campo Cuenta es Traducible por otro usuario.
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","purchase","purchase_requisition","sale","hr"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'product_view.xml',
                    'purchase_view.xml',
                    'purchase_requisition_view.xml',
                    'account_invoice_view.xml',
                    ],
    "installable" : True,
    "active" : False,
}
