# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/ibanity.html


from lino.api import dd, _
from lino_xl.lib.accounting.roles import LedgerStaff

with_suppliers = dd.get_plugin_setting("ibanity", "with_suppliers", False)

if with_suppliers:

    class OnboardingStates(dd.ChoiceList):
        verbose_name = _("Onboarding state")
        verbose_name_plural = _("Onboarding states")
        required_roles = dd.login_required(LedgerStaff)

    add = OnboardingStates.add_item
    add('10', _("Draft"), 'draft')
    add('20', _("Created"), 'created')
    add('30', _("Approved"), 'approved')
    add('40', _("Rejected"), 'rejected')
    add('50', _("Onboarded"), 'onboarded')
    add('60', _("Offboarded"), 'offboarded')

    # add('10', _("Active"), 'active')
    # add('20', _("Potential"), 'potential')
    # add('30', _("Unreachable"), 'unreachable')
