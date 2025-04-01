# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from django.conf import settings
# from lino.utils.instantiator import Instantiator
# from lino.utils import Cycler
# from lino.api import dd, rt, _
# from lino_xl.lib.ibanity.utils import DEMO_SUPPLIER_ID
#
#
# def objects():
#     # be = rt.models.countries.Country.objects.get(iso_code="BE")
#     # com = yield rt.models.ibanity.Company(
#     #     vat_id="BE1234567890", country=be, name="Old Name S.A.",
#     #     )
#     # yield com
#     if dd.plugins.ibanity.with_suppliers:
#         yield rt.models.ibanity.Supplier(supplier_id=DEMO_SUPPLIER_ID)
#         yield rt.models.ibanity.Supplier(supplier_id="1234-4567-89")
