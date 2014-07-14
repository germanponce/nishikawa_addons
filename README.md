nishikawa_addons
================

Addons adaptados para un Cliente, hechos para la version 7 >>> Migrando a 8.

Los Principales modulos que se manejan son:

 - Purchase Triple validation >>> Genera una Tercera Validacion para Compras para un grup especifico, llamado Directivos Compra
 
 - Compras >>> Se modificaron las Cuentas analiticas para definir en que productos seran requeridas, lo mismo sucede con Facturacion.
   Se modifico la Solicitud de Compra, se le agrego una columna para especificar, datos ó comentarios de algun producto que se requiere.
   
 - Generación del archivo para Banca Electrónica (Banamex) para el pago de proveedores >>> Se Creó un asistente que genera un Layout para Pago a Proveedores.
 
 - Que el sistema NO permita Validar la factura si no tiene adjunto el XML y PDF del proveedor >>> El Sistema verifica al Utilizar el Boton Validar,
   que el Documento tenga adjunto el XML y PDF del Proveedor.

 - No se permite confimar una cotizacion si no se tienen la Cotizacion del Proveedor un reporte PDF, si no se tiene se podra adjuntar x archivo.
 
 - Que TODAS las partidas contables de Producción se "liguen" a la Orden de Producción >>> Se agrego a las Polizas Contables, un filtro para poder buscar ó filtrarlas
   por el nombre de las partidas (nombre de las lineas de cada poliza).

 - Agregar check en Ficha del producto, que indique que al usarse en Pedido de Compra SIEMPRE “pida” la cuenta analítica en la línea del Pedido de Compra y/ Factura de Proveedor.
 
 - Formato de Factura Electrónica, especifica indicada por el Cliente.
 
 - Formato de Pedido de Compra.
