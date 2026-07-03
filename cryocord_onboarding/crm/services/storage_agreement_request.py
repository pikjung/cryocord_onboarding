import frappe

from cryocord_onboarding.crm.repository.storage_request_audit import StorageRequestAuditRepository
from cryocord_onboarding.crm.repository.storage_agreement_request import StorageAgreementRequestRepository

class StorageAgreementRequestService:
    def __init__(self, storage_agreement_request):
        self.doc = storage_agreement_request
        self.audit_repository = StorageRequestAuditRepository()

    def validate_workflow_transition(self):
        old_doc = self.doc.get_doc_before_save()

        self.doc._old_workflow_state = (
            old_doc.workflow_state if old_doc else "Draft"
        )

        current_status = self.doc._old_workflow_state
        new_status = self.doc.workflow_state

        if current_status == new_status:
            return

        allowed_transitions = {
            "Draft": ["Pending Approval"],
            "Pending Approval": ["Approved", "Rejected"],
            "Approved": ["Ready"],
            "Ready": ["Closed"],
            "Rejected": [],
        }

        if new_status not in allowed_transitions.get(current_status, []):
            frappe.throw(
                f"Transition from {current_status} to {new_status} is not allowed."
            )

        if new_status == "Approved":
            if not self.doc.approval_reason:
                frappe.throw("Approval reason is required when approving the request.")
            
            if self.doc.owner == frappe.session.user:
                frappe.throw(
                    "The document creator is not allowed to approve this request."
                )
            
        self.update_workflow_data()
        self.log_audit()
        
            
    def update_workflow_data(self):
        if self.doc.workflow_state == "Approved":
            self.doc.approved_by = frappe.session.user
            self.doc.approved_at = frappe.utils.now()
            
        if self.doc.workflow_state == "Pending Approval":
            self.doc.requested_date = frappe.utils.now()
            
    def fill_sales(self):
        self.doc.sales_officer = frappe.session.user
        
    def log_audit(self):
        doc_before_save = self.doc.get_doc_before_save()
        from_state = doc_before_save.workflow_state if doc_before_save else None
        to_state = self.doc.workflow_state

        if from_state == to_state:
            return

        self.audit_repository.log_storage_request(
            self.doc.name,
            from_state,
            to_state,
        )
        
    @staticmethod
    def get_pending_approval_requests():
        repository = StorageAgreementRequestRepository()
        return repository.get_pending_approval_requests()