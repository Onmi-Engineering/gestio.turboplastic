TDG22012 #01 SII - TURBO EDI documents
======================================
Turboplastic
+ Branch -> main

Desarrollo
==========
- [*OVERRIDE*] del metodo aplicado en ir.cron de EDI documents para que no efectúe el trigger.

Configuración
=============
- Es necesario duplicar la acción y desactivar la anterior, ya que, si no, el trigger seguirá afectado 
en la acción anterior y, por ese motivo, seguiría funcionando igual. 