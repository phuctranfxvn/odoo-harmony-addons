# -*- coding: utf-8 -*-
{
    'name': 'Vietcombank Exchange Rate',
    'version': '1.0',
    'category': 'Accounting',
    'website': 'https://github.com/phuctranfxvn/odoo-harmony-addons',
    'summary': """
    Auto update daily currency rate from Vietcombank
        """,

    'description': """
    Auto update daily currency rate from Vietcombank
        """,

    'author': 'Felix VNM',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],

    'depends': [
        'base',
        'currency_rate_update',
    ],

    'data': [

        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        # 'security/',

        # ============================================================
        # DATA
        # ============================================================
        # 'data/',

        # ============================================================
        # VIEWS
        # ============================================================
        # 'view/',

        # ============================================================
        # MENU
        # ============================================================
        # 'menu/',

        # ============================================================
        # FUNCTION USED TO UPDATE DATA LIKE POST OBJECT
        # ============================================================
    ],

}
