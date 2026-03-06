# #11 TURBO Bascule and Receptions

![Licencia OPL-1](https://img.shields.io/badge/licence-OPL--1-blue.svg)
![Versión 18.0](https://img.shields.io/badge/version-18.0-brightgreen.svg)

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Instalación](#instalación)
- [Modelos](#modelos)
  - [weighing — Pesaje](#weighing--pesaje)
  - [carriage.order — Orden de Transporte](#carriageorder--orden-de-transporte)
  - [license.plate — Matrícula](#licenseplate--matrícula)
  - [trailer — Remolque](#trailer--remolque)
- [Modelos heredados](#modelos-heredados)
  - [stock.picking — Albarán](#stockpicking--albarán)
  - [sale.order — Pedido de Venta](#saleorder--pedido-de-venta)
  - [purchase.order — Pedido de Compra](#purchaseorder--pedido-de-compra)
  - [stock.move — Movimiento de Stock](#stockmove--movimiento-de-stock)
  - [stock.move.line — Línea de Movimiento](#stockmoveline--línea-de-movimiento)
- [Funciones principales](#funciones-principales)
- [Vistas](#vistas)
- [Seguridad y permisos](#seguridad-y-permisos)
- [Flujo de trabajo completo](#flujo-de-trabajo-completo)
- [Historial de versiones](#historial-de-versiones)
- [Créditos](#créditos)

---

## Descripción general

Módulo de gestión de pesajes vinculados a recepciones y entregas de productos. Permite registrar
el peso real de entrada y salida de mercancía asociándolo a pedidos de compra y venta,
controlando el flujo logístico completo desde la solicitud de transporte hasta la validación del albarán.

**Características principales:**

- Pesajes de entrada (compras) y salida (ventas) multiproducto.
- Los pesos finales deben coincidir con las cantidades de los pedidos o, en su defecto, el sistema permite reconfirmarlos.
- Gestión de matrículas y remolques asociados a cada transporte.
- Solicitudes de transporte (órdenes de carriage) vinculadas a pedidos de compra/venta.
- Menú de Logística independiente con gestión de flota y transporte.

**Dependencias:** `sale_management`, `purchase`, `stock`, `uom`

---

## Instalación

1. Copiar el módulo `onmi_turbo_weighings` en la carpeta de addons del servidor.
2. Actualizar la lista de módulos desde **Ajustes → Activar el modo desarrollador → Actualizar lista de aplicaciones**.
3. Instalar el módulo desde el menú de Aplicaciones buscando *"Turbo Bascule"*.
4. Asegurarse de que el idioma español está instalado para cargar las traducciones automáticamente.

---

## Modelos

### `weighing` — Pesaje

Modelo principal del módulo. Registra cada pesaje individual asociado a un movimiento de stock.

| Campo                    | Tipo                | Descripción                                                            |
|--------------------------|---------------------|------------------------------------------------------------------------|
| `type`                   | Selection           | Tipo de pesaje: `input` (Entrada, compras) / `output` (Salida, ventas) |
| `state`                  | Selection           | Estado: `new` · `on_weighing` · `confirmed`                            |
| `first_weight`           | Float               | Primer peso registrado en báscula                                      |
| `second_weight`          | Float               | Segundo peso registrado en báscula                                     |
| `waste`                  | Float               | Merma a descontar del peso final                                       |
| `final_weight`           | Float (computed)    | Peso final calculado automáticamente                                   |
| `final_weight_calculate` | Float (computed)    | Campo auxiliar de cálculo paralelo                                     |
| `product_id`             | Many2one            | Producto asociado (`product.product`)                                  |
| `license_plate_id`       | Many2one            | Matrícula del vehículo de transporte                                   |
| `trailer_id`             | Many2one            | Remolque asociado al transporte                                        |
| `upload_date`            | Date                | Fecha de carga del transporte                                          |
| `contact`                | Many2one            | Contacto/cliente/proveedor (`res.partner`)                             |
| `picking_id`             | Many2one            | Albarán al que pertenece (`stock.picking`)                             |
| `sale_id`                | Many2one            | Pedido de venta relacionado                                            |
| `purchase_id`            | Many2one            | Pedido de compra relacionado                                           |
| `move_line_id`           | Many2one            | Línea de movimiento de stock (`stock.move`)                            |
| `code_led`               | Char                | Código L.E.R. (Lista Europea de Residuos)                              |
| `description`            | Text (computed)     | Descripción extraída de la línea del pedido                            |
| `partner_picking`        | Char (computed)     | Nombre del partner del albarán                                         |
| `date_done_picking`      | Datetime (computed) | Fecha programada del albarán                                           |
| `company_id`             | Many2one (computed) | Empresa del albarán                                                    |
| `picking_state`          | Selection (related) | Estado del albarán relacionado                                         |

> **Lógica de cálculo del peso final:**
> - **Salidas (ventas):** el primer peso debe ser *menor* que el segundo (tara < bruto).
>   `final_weight = second_weight - first_weight - waste`
> - **Entradas (compras):** el primer peso debe ser *mayor* que el segundo (bruto > tara).
>   `final_weight = first_weight - second_weight - waste`
>
> Si la condición no se cumple se lanza un `ValidationError`.

---

### `carriage.order` — Orden de Transporte

Gestiona las solicitudes de transporte vinculadas a pedidos de compra o venta.

| Campo                  | Tipo                | Descripción                                                 |
|------------------------|---------------------|-------------------------------------------------------------|
| `name`                 | Char                | Referencia generada por secuencia (ej: `OT/2025/0001`)      |
| `contact`              | Many2one            | Contacto del pedido (`res.partner`)                         |
| `partner_shipping_alt` | Char                | Dirección de entrega alternativa (texto libre)              |
| `weight`               | Float               | Peso aproximado del transporte                              |
| `weight_uom`           | Many2one (computed) | Unidad de medida — autoasignada a `kg`                      |
| `processed`            | Boolean (computed)  | Indica si la orden está procesada                           |
| `origin`               | Char (computed)     | Referencia del pedido de origen                             |
| `sale_order_id`        | Many2one            | Pedido de venta relacionado (solo lectura)                  |
| `purchase_order_id`    | Many2one            | Pedido de compra relacionado (solo lectura)                 |
| `license_plate_id`     | Many2one            | Matrícula del vehículo asignado                             |
| `trailer_id`           | Many2one            | Remolque asignado                                           |
| `pick_up_date`         | Datetime            | Fecha y hora de recogida                                    |
| `delivery_date`        | Datetime            | Fecha y hora de entrega                                     |
| `state`                | Selection           | `draft` · `processing` · `processed` · `confirm` · `cancel` |
| `company_id`           | Many2one            | Empresa (autoasignada)                                      |

---

### `license.plate` — Matrícula

Catálogo de matrículas de vehículos.

| Campo            | Tipo                 | Descripción                                         |
|------------------|----------------------|-----------------------------------------------------|
| `name`           | Char                 | Identificador único (restricción `unique`)          |
| `type`           | Selection            | `internal` (vehículo propio) / `external` (externo) |
| `description`    | Char                 | Descripción libre del vehículo                      |
| `weighing_ids`   | Many2many (computed) | Pesajes asociados a esta matrícula                  |
| `weighing_count` | Integer (computed)   | Número de pesajes (botón inteligente)               |

---

### `trailer` — Remolque

Catálogo de remolques.

| Campo              | Tipo                 | Descripción                                |
|--------------------|----------------------|--------------------------------------------|
| `name`             | Char                 | Identificador único (restricción `unique`) |
| `description`      | Char                 | Descripción libre                          |
| `license_plate_id` | Many2one             | Matrícula habitualmente asociada           |
| `weighing_ids`     | Many2many (computed) | Pesajes asociados a este remolque          |
| `weighing_count`   | Integer (computed)   | Número de pesajes (botón inteligente)      |

---

## Modelos heredados

### `stock.picking` — Albarán

| Campo                            | Tipo             | Descripción                                                      |
|----------------------------------|------------------|------------------------------------------------------------------|
| `date_planned`                   | Datetime         | Fecha del peso final confirmado                                  |
| `license_plate_id`               | Many2one         | Matrícula — se propaga a todos los pesajes al modificarse        |
| `trailer_id`                     | Many2one         | Remolque — se propaga a todos los pesajes al modificarse         |
| `upload_date`                    | Date             | Fecha de carga — se propaga a todos los pesajes al modificarse   |
| `weighing_ids`                   | One2many         | Lista de pesajes vinculados al albarán                           |
| `confirmed_weighings`            | Boolean          | Indica si todos los pesajes están confirmados                    |
| `active_reconfirm_new_weighings` | Boolean          | Activa el botón de reconfirmación si hay diferencias de peso     |
| `text_warning`                   | Text             | Mensaje de aviso cuando hay diferencias en los pesos             |
| `weighings_is_required`          | Boolean          | Indica si el albarán requiere confirmar pesajes antes de validar |
| `total_ordered`                  | Float (computed) | Suma de cantidades pedidas                                       |
| `total_delivered`                | Float (computed) | Suma de cantidades realizadas                                    |
| `total_wasted`                   | Float (computed) | Suma de mermas de todos los pesajes                              |

### `sale.order` — Pedido de Venta

| Campo              | Tipo                 | Descripción                           |
|--------------------|----------------------|---------------------------------------|
| `carriage_ids`     | Many2many (computed) | Órdenes de transporte asociadas       |
| `carriage_count`   | Integer (computed)   | Número de órdenes (botón inteligente) |
| `license_plate_id` | Many2one (computed)  | Matrícula del primer albarán          |
| `trailer_id`       | Many2one (computed)  | Remolque del primer albarán           |
| `upload_date`      | Date (computed)      | Fecha de carga del primer albarán     |

### `purchase.order` — Pedido de Compra

| Campo            | Tipo                 | Descripción                           |
|------------------|----------------------|---------------------------------------|
| `carriage_ids`   | Many2many (computed) | Órdenes de transporte asociadas       |
| `carriage_count` | Integer (computed)   | Número de órdenes (botón inteligente) |

### `stock.move` — Movimiento de Stock

| Campo         | Tipo                | Descripción                             |
|---------------|---------------------|-----------------------------------------|
| `code_led`    | Char                | Código L.E.R. propagado desde el pesaje |
| `weighing_id` | Many2one (computed) | Pesaje asociado a este movimiento       |
| `waste_qty`   | Float (computed)    | Cantidad de merma del pesaje asociado   |

### `stock.move.line` — Línea de Movimiento

| Campo         | Tipo                        | Descripción                                      |
|---------------|-----------------------------|--------------------------------------------------|
| `weighing_id` | Many2one (computed, stored) | Pesaje asociado, heredado del `stock.move` padre |
| `waste_qty`   | Float (computed)            | Cantidad de merma del pesaje asociado            |

---

## Funciones principales

### `weighing`

| Función                          | Descripción                                                                                                                                 |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `compute_final_weight`           | Calcula `final_weight` cuando cambian `first_weight`, `second_weight` o `waste`. Valida el orden de los pesos según el tipo entrada/salida. |
| `update_final_weight`            | Onchange sobre `waste`: recalcula el peso final en tiempo real.                                                                             |
| `compute_final_weight_calculate` | Campo auxiliar de cálculo, almacenado por separado.                                                                                         |
| `compute_final_descripcion`      | Obtiene la descripción de la línea del pedido si difiere del nombre del producto.                                                           |
| `_compute_date_done_picking`     | Copia la fecha programada del albarán al pesaje.                                                                                            |
| `_compute_company_id`            | Asigna la empresa del albarán al pesaje.                                                                                                    |
| `compute_partner_picking`        | Obtiene y almacena el nombre del partner del albarán.                                                                                       |

### `stock.picking`

| Función                        | Descripción                                                                                                                                        |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `_compute_totals`              | Calcula totales de cantidades pedidas, entregadas y mermas.                                                                                        |
| `asign_license_plate`          | Onchange: propaga la matrícula del albarán a todos sus pesajes.                                                                                    |
| `asign_trailer`                | Onchange: propaga el remolque a todos sus pesajes.                                                                                                 |
| `asign_date`                   | Onchange: propaga la fecha de carga a todos sus pesajes.                                                                                           |
| `action_confirm_weighings`     | Valida y confirma los pesajes. Comprueba: orden de transporte procesada, pesos > 0 y coincidencia con la demanda. Actualiza las `stock.move.line`. |
| `action_reconfirm_weighings`   | Acepta pesos que no coinciden con la demanda y actualiza las cantidades en el pedido.                                                              |
| `action_reset_weighings`       | Devuelve todos los pesajes a `on_weighing` y pone a cero las cantidades de movimiento.                                                             |
| `action_recalculate_weighings` | Genera pesajes para operaciones que no tengan uno asociado.                                                                                        |
| `button_validate`              | Override: comprueba que todos los pesajes estén `confirmed` antes de validar. Marca las órdenes de transporte como `confirm`.                      |
| `_action_done`                 | Override: crea líneas de pedido de venta para movimientos sin línea asociada y actualiza pesos finales.                                            |
| `change_descriptions`          | Copia descripciones de líneas de pedido de venta a los movimientos del albarán.                                                                    |

### `carriage.order`

| Función             | Descripción                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| `action_processing` | Pasa la orden al estado `processing`.                                                 |
| `action_processed`  | Valida matrícula y remolque, los propaga a albaranes y pesajes, y pasa a `processed`. |
| `action_cancelled`  | Cancela la orden de transporte.                                                       |
| `create`            | Override: asigna secuencia automática y establece estado inicial `processing`.        |
| `unlink`            | Override: decrementa el contador de secuencia al eliminar una orden.                  |

### `sale.order`

| Función                        | Descripción                                                                            |
|--------------------------------|----------------------------------------------------------------------------------------|
| `action_confirm`               | Override: crea pesajes de tipo `output` por cada operación de los albaranes generados. |
| `action_create_carriage_order` | Abre formulario de nueva orden de transporte prellenado con los datos del pedido.      |
| `action_view_carriage`         | Botón inteligente: navega a las órdenes de transporte del pedido.                      |

### `purchase.order`

| Función                        | Descripción                                                                           |
|--------------------------------|---------------------------------------------------------------------------------------|
| `button_confirm`               | Override: crea pesajes de tipo `input` por cada operación de los albaranes generados. |
| `action_create_carriage_order` | Abre formulario de nueva orden de transporte prellenado con los datos del pedido.     |
| `action_view_carriage`         | Botón inteligente: navega a las órdenes de transporte del pedido.                     |

### `stock.move.line`

| Función                              | Descripción                                                                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `_get_aggregated_product_quantities` | Override: añade `first_weight`, `second_weight` y `code_led` al informe de albarán. Compatible con el cambio `qty_done` → `quantity` de Odoo 18. |

---

## Vistas

### Menú Logística

Menú principal del módulo, independiente de Inventario, Ventas y Compras.

**Transporte → Órdenes de Transporte**
- Vista árbol con columnas de estado, origen, matrícula, remolque y fechas.
- Vista formulario con todos los campos y botones de cambio de estado.
- Filtros por estado (No Tramitado / Tramitado / Entregado / Cancelado) y empresa.

**Flota → Matrículas**
- Vista árbol con tipo y descripción.
- Vista formulario con botón inteligente de pesajes asociados.

**Flota → Remolques**
- Vista árbol con matrícula asociada y descripción.
- Vista formulario con botón inteligente de pesajes asociados.

**Pesajes**
- Vista árbol global con filtros por estado, tipo y empresa.
- Vista formulario con todos los campos de peso, producto, transporte y estado.
- Vista pivot y gráfico para análisis por periodo, producto o proveedor/cliente.

### Albaranes (Inventario)

- **Pestaña Pesajes:** tabla editable con todos los pesajes del albarán. Permite introducir pesos directamente.
- **Campos de transporte:** matrícula, remolque y fecha de carga en cabecera.
- **Totales informativos:** total pedido, total entregado y total merma.
- **Botones de acción:**
  - *Confirmar Pesajes* — `action_confirm_weighings`
  - *Reconfirmar Pesajes* — visible solo cuando hay diferencias (`active_reconfirm_new_weighings`)
  - *Resetear Pesajes* — `action_reset_weighings`
  - *Recalcular Pesajes* — `action_recalculate_weighings`

### Pedidos de Venta y Compra

- **Botón inteligente** de Órdenes de Transporte con contador.
- **Botón** *Crear Solicitud de Transporte* disponible tras confirmar el pedido.
- **Campos informativos:** matrícula, remolque y fecha de carga del primer albarán.

---

## Seguridad y permisos

El módulo define la categoría **Logística** con dos grupos propios:

| Grupo                         | Acceso                                                                                        |
|-------------------------------|-----------------------------------------------------------------------------------------------|
| **Logística / Empleado**      | Lectura + escritura en `carriage.order`. Solo lectura en `license.plate` y `trailer`.         |
| **Logística / Administrador** | CRUD completo en `carriage.order`, `license.plate` y `trailer`. Incluye permisos de Empleado. |

Permisos sobre grupos estándar de Odoo:

| Grupo                                    |        `license.plate`         |  `trailer`   | `carriage.order` | `weighing` |
|------------------------------------------|:------------------------------:|:------------:|:----------------:|:----------:|
| Ventas (`group_sale_salesman_all_leads`) |          Solo lectura          | Solo lectura |       CRUD       |    CRUD    |
| Compras (`group_purchase_user`)          |          Solo lectura          | Solo lectura |       CRUD       |    CRUD    |
| Stock (`group_stock_user`)               | ⚠️ Añadir creación manualmente |      —       |        —         |     —      |

> **Nota:** Para que los usuarios de almacén puedan crear matrículas directamente desde el formulario de pesaje en un albarán, hay que añadir `perm_create: 1` sobre `license.plate` para el grupo `stock.group_stock_user` en el archivo `security.xml`.

También se define una **regla multicompañía** sobre `carriage.order` para que cada empresa solo vea sus propias órdenes.

---

## Flujo de trabajo completo

### Recepción de compra

```
Confirmar PO
    └─► Se crean pesajes tipo "Entrada" en los albaranes generados
         └─► Crear Solicitud de Transporte (matrícula + remolque)
              └─► Logística pulsa "Procesar" en la orden
                   └─► Matrícula y remolque se propagan al albarán y pesajes
                        └─► En el albarán: introducir primer peso y segundo peso
                             └─► "Confirmar Pesajes"
                                  ├─ Pesos == demanda ──► Pesajes confirmados ──► Validar albarán
                                  └─ Pesos != demanda ──► "Reconfirmar Pesajes" ──► Validar albarán
```

### Entrega de venta

```
Confirmar SO
    └─► Se crean pesajes tipo "Salida" en los albaranes generados
         └─► (Opcional) Crear Solicitud de Transporte
              └─► En el albarán: primer peso = tara, segundo peso = bruto
                   └─► "Confirmar Pesajes" ──► Validar albarán
```

---

## Historial de versiones

| Versión    | Cambios                                                                                                                                                               |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 18.0.1.0.0 | Versión inicial adaptada a Odoo 18. Corrección del campo `quantity` (antes `qty_done`) en `stock.move.line`. Compatibilidad con la nueva API de movimientos de stock. |

---

## Créditos

- **Autor:** ONMI Engineering
- **Licencia:** OPL-1
- **Soporte:** info@onmi.es
