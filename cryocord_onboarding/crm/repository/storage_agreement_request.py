import frappe

class StorageAgreementRequestRepository:
    @staticmethod
    def get_pending_approval_requests():
        requests = frappe.db.sql(
            """
            SELECT
                name,
                sales_officer,
                requested_date,
                workflow_state,
                creation
            FROM `tabStorage Agreement Request`
            WHERE docstatus = 0
                AND workflow_state = 'Pending Approval'
            ORDER BY creation ASC
            """,
            as_dict=1,
        )
        return requests