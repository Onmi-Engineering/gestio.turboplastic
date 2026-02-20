================================
#11 TURBO Bascule and Receptions
================================

**Tabla de contenidos**

.. contents::
   :local:

Instalación
***********

Usabilidad
**********

Incluido pesaje de entrada y salida de productos. Unidos a recepciones y salidas de productos con su
peso real. Estos pesajes tienen opción de multiproducto.

Deben coincidir los pesos en pedido de compra/venta y de las órdenes de entrega y salida.

Desarrollo
**********

- Inventario
    - Pesadas:
        Incluidas en albaranes de entrega /salida

- Compras / Ventas:
    - Contacto: Proveedor/cliente.
    - Destino: Dirección de entrega.
    - Destino alternativo: Campo de texto? para destino diferente.
    - Material: material del pedido.
    - Peso aproximado: peso del pedido.

    Incluir botón de solicitud de transporte para que aparezca cuando el pedido está confirmado.
    Este botón abre un formulario con los datos anteriores


- Logística (nuevo menú):
    - Menú Transporte:
        - Vista árbol de solicitudes de transporte con filtro Importado / no importado.
        - Formulario de transporte con los siguientes campos:
            - Nombre:
            - No Tramitado/ Tramitado (boolean: boolean_toggle): Autorellenado cn botón confirmar (pasa de estado solicitado a tramitado).
            - Origen (pedido relacionado): campo de texto con la referencia del pedido ya sea venta o compra.
            - Pedido de Compra: pedido de compra relacionado si aplica.[Many2one]
            - Pedido de Venta: pedido de venta relacionado si aplica.[Many2one]
            - Matricula: [Many2one]
            - Remolque: [Many2one]
            - Fecha recogida:
            - Fecha de entrega:

    - Menú Flota:
        - Menú Matrícula:
            - Nombre:
            - Tipo: Interno/Externo.
            - Descripción:

        - Menú Remolque:
            - Nombre:
            - Matrícula:  requerido para que cuando se cree un remolque se le asocie matrícula.
            - Descripción: