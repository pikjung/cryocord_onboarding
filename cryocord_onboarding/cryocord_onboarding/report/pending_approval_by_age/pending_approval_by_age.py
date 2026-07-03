# Copyright (c) 2026, Fikri and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff, nowdate


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{
			"label": _("Storage Agreement Request"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Storage Agreement Request",
			"width": 220,
		},
		{
			"label": _("Sales Officer"),
			"fieldname": "sales_officer",
			"fieldtype": "Link",
			"options": "User",
			"width": 150,
		},
  		{
			"label": _("Requested Date"),
			"fieldname": "requested_date",
			"fieldtype": "Date",
			"width": 110,
		},
		{
			"label": _("Workflow State"),
			"fieldname": "workflow_state",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Created On"),
			"fieldname": "creation",
			"fieldtype": "Date",
			"width": 110,
		},
		{
			"label": _("Age (Days)"),
			"fieldname": "age_days",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("Age Bucket"),
			"fieldname": "age_bucket",
			"fieldtype": "Data",
			"width": 120,
		},
	]


def get_data(filters):
	conditions = get_conditions(filters)

	requests = frappe.db.sql(
		f"""
		SELECT
			name,
			sales_officer,
			requested_date,
			workflow_state,
			creation
		FROM `tabStorage Agreement Request`
		WHERE docstatus = 0
			AND workflow_state = 'Pending Approval'
			{conditions}
		ORDER BY creation ASC
		""",
		filters,
		as_dict=1,
	)

	today = nowdate()
	data = []
	for row in requests:
		age = date_diff(today, row.creation)
		row["age_days"] = age
		row["age_bucket"] = get_age_bucket(age)
		data.append(row)

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("requested_date"):
		conditions += " AND requested_date = %(requested_date)s"
  
	if filters.get("sales_officer"):
		conditions += " AND sales_officer = %(sales_officer)s"

	if filters.get("from_date"):
		conditions += " AND creation >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND creation <= %(to_date)s"

	return conditions


def get_age_bucket(age):
	if age <= 3:
		return "0-3 days"
	elif age <= 7:
		return "4-7 days"
	elif age <= 14:
		return "8-14 days"
	elif age <= 30:
		return "15-30 days"
	else:
		return "30+ days"


def get_chart(data):
	bucket_order = ["0-3 days", "4-7 days", "8-14 days", "15-30 days", "30+ days"]
	bucket_counts = {b: 0 for b in bucket_order}

	for row in data:
		bucket_counts[row["age_bucket"]] += 1

	return {
		"data": {
			"labels": bucket_order,
			"datasets": [{"name": "Pending Requests", "values": [bucket_counts[b] for b in bucket_order]}],
		},
		"type": "bar",
		"colors": ["#e74c3c"],
	}


def get_summary(data):
	total = len(data)
	overdue = len([d for d in data if d["age_days"] > 7])

	return [
		{
			"label": _("Total Pending"),
			"value": total,
			"indicator": "Orange" if total else "Green",
		},
		{
			"label": _("Overdue (>7 days)"),
			"value": overdue,
			"indicator": "Red" if overdue else "Green",
		},
	]
