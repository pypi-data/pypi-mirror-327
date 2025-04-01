# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/peppol.html


from lino.api import ad, _
from .utils import Session


class Plugin(ad.Plugin):

    verbose_name = _("Ibanity")
    needs_plugins = ['lino_xl.lib.vat']
    menu_group = "contacts"

    with_suppliers = False
    supplier_id = None
    cert_file = None
    key_file = None
    credentials = None

    def pre_site_startup(self, site):
        cd = site.site_dir / "secrets"
        if cd.exists():
            self.cert_file = cd / "certificate.pem"
            self.key_file = cd / "decrypted_private_key.pem"
            self.credentials = (cd / "credentials.txt").read_text().strip()

    def get_ibanity_session(self):
        if not self.credentials:
            return
        return Session(self.cert_file, self.key_file, self.credentials)

    def setup_main_menu(self, site, user_type, m, ar=None):
        if self.with_suppliers:
            mg = self.get_menu_group()
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('ibanity.Suppliers')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        if self.with_suppliers:
            mg = self.get_menu_group()
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('ibanity.OnboardingStates')
