import frappe

class StorageRequestAuditRepository:
    @staticmethod
    def log_storage_request(storage_request, from_state, to_state):
        audit_entry = frappe.get_doc({
            "doctype": "Storage Request Audit",
            "request": storage_request,
            "from_state": from_state,
            "to_state": to_state,
            "changed_by": frappe.session.user,
            "changed_at": frappe.utils.now()
        })
        audit_entry.insert(ignore_permissions=True)