// Copyright (c) 2026, Fikri and contributors
// For license information, please see license.txt

frappe.query_reports["Pending Approval by Age"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": "100",
		},
		{
			"fieldname": "sales_officer",
			"label": __("Sales Officer"),
			"fieldtype": "Link",
			"options": "User",
			"width": "100",
		},
		{
			"fieldname": "requested_date",
			"label": __("Requested Date"),
			"fieldtype": "Date",
			"width": "100",
		},
		{
			"fieldname": "from_date",
			"label": __("Creation From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80",
		},
		{
			"fieldname": "to_date",
			"label": __("Creation To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "80",
		},
	],
};