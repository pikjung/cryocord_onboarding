import frappe
from cryocord_onboarding.crm.services.storage_agreement_request import StorageAgreementRequestService

@frappe.whitelist()
def get_pending_approval_requests(filters=None):
    storage_agreement_request_service = StorageAgreementRequestService
    pending_requests = storage_agreement_request_service.get_pending_approval_requests()
    return pending_requests