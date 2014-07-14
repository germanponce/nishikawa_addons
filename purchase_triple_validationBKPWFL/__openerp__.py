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

{
    'name' : 'Triple Validacion para Compras',
    'version' : '1.1',
    'category': 'Purchase',
    'images' : ['images/purchase_validation.jpeg'],
    'depends' : ['base','purchase','purchase_double_validation'],
    'author' : 'German Ponce Dominguez',
    'description': """

           Este modulo permite alterar el flujo del Pedido de Compra para las Autorizaciones (Modulo puchase_double_validation)
             - Solicitante registra ""Solicitud de Compra""
             - Personal de Compras cotiza
             - El solicitante ""Confirma"" lo(s) Presupuestos
             - El Manager confirma Pedido de Compra (< 5000)
             - Si son mayor en monto a 5,000 solo Director Aprueba (Grupo Purchase Director)
    """,
    'website' : "http://poncesoft.blogspot.com",
    'data': [
        'security/purchase_triple_validation_security.xml',
        'purchase_double_validation_workflow.xml',
        #'purchase_double_validation_installer.xml',
        'purchase_double_validation_view.xml',
        #'board_purchase_view.xml'
    ],
    # 'test': [
    #     'test/purchase_double_validation_demo.yml',
    #     'test/purchase_double_validation_test.yml'
    # ],
    'demo': [],
    'installable': True,
    'auto_install': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
