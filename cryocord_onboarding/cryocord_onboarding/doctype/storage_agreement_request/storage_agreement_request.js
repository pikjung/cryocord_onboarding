// Copyright (c) 2026, Fikri and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Storage Agreement Request", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Storage Agreement Item", {
	qty: function(frm, cdt, cdn) {
		calculate_row(frm, cdt, cdn);
	},

	unit_price: function(frm, cdt, cdn) {
		calculate_row(frm, cdt, cdn);
	},

	discount: function(frm, cdt, cdn) {
		calculate_row(frm, cdt, cdn);
	},

	requested_packages_add: function(frm) {
		calculate_total(frm);
	},

	requested_packages_remove: function(frm) {
		calculate_total(frm);
	}
});

function calculate_row(frm, cdt, cdn) {
	let row = locals[cdt][cdn];

	let subtotal = flt(row.qty) * flt(row.unit_price);
	let discount_amount = subtotal * flt(row.discount) / 100;
	let amount = subtotal - discount_amount;

	frappe.model.set_value(cdt, cdn, "amount", amount);

	calculate_total(frm);
}

function calculate_total(frm) {
	let total = 0;

	(frm.doc.requested_packages || []).forEach(row => {
		total += flt(row.amount);
	});

	frm.set_value("total", total);
}