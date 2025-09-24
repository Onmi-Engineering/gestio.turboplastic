from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    user_lang = env.user.lang

    # para borrar campos
    cr.execute("""
        DELETE FROM ir_model_fields
        WHERE name = 'not_in_mod347';
        """)
    # para borrar vistas
    cr.execute(f"""
        DELETE FROM IR_UI_VIEW
        WHERE arch_db->>'{user_lang}' ILIKE '%not_in_mod347%';
        """)
    # para borrar registro del campo
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE name ILIKE '%not_in_mod_347%';
        """)

    _logger.info("Limpieza de campos completado")
