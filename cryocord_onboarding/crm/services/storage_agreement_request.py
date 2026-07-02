import frappe

class StorageAgreementRequestService:
    def __init__(self, storage_agreement_request):
        self.doc = storage_agreement_request

    def validate_workflow_transition(self):
        old_doc = self.doc.get_doc_before_save()

        current_status = old_doc.workflow_state if old_doc else "Draft"
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
            
        self.update_approved_data(self)
            
    def update_approved_data(self):
        if self.doc.workflow_state == "Approved":
            self.doc.approved_by = frappe.session.user
            self.doc.approved_at = frappe.utils.now()
            