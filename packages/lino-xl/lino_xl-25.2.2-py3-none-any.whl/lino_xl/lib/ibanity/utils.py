# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/ibanity.html

import requests
import base64
import json
# from lino.api import dd


DEMO_SUPPLIER_ID = '273c1bdf-6258-4484-b6fb-74363721d51f'

# def get_cred_settings(cert_dir):
#     if cert_dir.exists():
#         yield ("ibanity", "cert_file", cert_dir / "certificate.pem")
#         yield ("ibanity", "key_file", cert_dir / "decrypted_private_key.pem")
#         credentials = (cert_dir / "credentials.txt").read_text().strip()
#         yield ("ibanity", "credentials", credentials)


root_url = "https://api.ibanity.com/einvoicing"

# client_id = dd.get_plugin_setting("peppol", "client_id", None)
# client_secret = dd.get_plugin_setting("peppol", "client_secret", None)
# cert_file = dd.get_plugin_setting("peppol", "cert_file", None)
# key_file = dd.get_plugin_setting("peppol", "key_file", None)
# credentials = f"{client_id}:{client_secret}"

class Session:

    def __init__(self, cert_file, key_file, credentials):
        if not cert_file.exists():
            raise Exception(f"Certificate file {cert_file} doesn't exist")
        if not key_file.exists():
            raise Exception(f"Key file {key_file} doesn't exist")
        self.cert_file = cert_file
        self.key_file = key_file
        self.credentials = credentials
        # Create an HTTPS session
        self.session = requests.Session()
        # Attach client certificate and key
        self.session.cert = (self.cert_file, self.key_file)

    def get_response(self, meth_name, *args, **kwargs):
        meth = getattr(self.session, meth_name)
        try:
            response = meth(*args, **kwargs)
        except Exception as e:
            raise Exception(f"{meth_name} failed: {e}")
        if not response.status_code in {200, 201}:
            raise Exception(f"{meth_name} returned unexpected status code {response.status_code}")
        return response.text

    def get_json_response(self, *args, **kwargs):
        txt = self.get_response(*args, **kwargs)
        return json.loads(txt)

    def get_access_token(self):
        # Base64 encode client_id and client_secret for Basic Auth
        encoded_credentials = base64.b64encode(self.credentials.encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",  # Required for OAuth2 requests
        }
        # return f"20250204 {headers}"

        url = f"{root_url}/oauth2/token"
        data = {"grant_type": "client_credentials"}
        return self.get_json_response('post', url, data=data, headers=headers)

    def get_headers(self, accept="application/vnd.api+json"):
        rv = self.get_access_token()
        access_token = rv['access_token']
        headers = {
            "Accept": accept,
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def list_suppliers(self):
        # Get a list of suppliers
        url = f"{root_url}/suppliers"
        return self.get_json_response('get', url, headers=self.get_headers())

    def create_supplier(self, **attributes):
        url = f"{root_url}/suppliers/"
        data = {
            "type": "supplier",
            "attributes": attributes}
        data = {"data": data}
        return self.get_json_response('post', url, json=data, headers=self.get_headers())

    def get_supplier(self, supplier_id):
        url = f"{root_url}/suppliers/{supplier_id}"
        return self.get_json_response('get', url, headers=self.get_headers())

    def list_registrations(self, supplier_id):
        url = f"{root_url}/peppol/suppliers/{supplier_id}/registrations"
        return self.get_json_response('get', url, headers=self.get_headers())

    def list_inbound_documents(self):
        url = f"{root_url}/peppol/inbound-documents"
        return self.get_json_response('get', url, headers=self.get_headers())

    def get_inbound_document_xml(self, doc_id):
        url = f"{root_url}/peppol/inbound-documents/{doc_id}"
        return self.get_response(
            'get', url, headers=self.get_headers("application/xml"))

    # Customer search. Check whether my customer exists.
    # Belgian participants are registered with the Belgian company number, for which
    # identifier 0208 can be used. Optionally, the customer can be registered with
    # their VAT number, for which identifier 9925 can be used.
    # The Flowin sandbox contains hard-coded fake data.  Using another reference as
    # customerReference will in result a 404
    def customer_search(self, customerReference):
        url = f"{root_url}/peppol/customer-searches"
        data = {
            "type": "peppolCustomerSearch",
            # "id": str(uuid.uuid4()),
            "attributes": {
                "customerReference": customerReference,
                # "supportedDocumentFormats": doc_formats
            }
        }
        data = {"data": data}
        # pprint(data)
        return self.get_json_response('post', url, headers=self.get_headers(), json=data)
