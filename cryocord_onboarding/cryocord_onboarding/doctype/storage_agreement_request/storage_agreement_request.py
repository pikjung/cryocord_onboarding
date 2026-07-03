# Copyright (c) 2026, Fikri and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from cryocord_onboarding.crm.services.storage_agreement_request import StorageAgreementRequestService


class StorageAgreementRequest(Document):
    def validate(self):
        service = StorageAgreementRequestService(self)
        service.validate_workflow_transition()
        
        self.total_amount = sum(item.amount or 0 for item in self.requested_packages)
        
    def before_save(self):
        service = StorageAgreementRequestService(self)
        service.fill_sales()
        
    def on_update_after_submit(self):
        StorageAgreementRequestService(self).log_audit()