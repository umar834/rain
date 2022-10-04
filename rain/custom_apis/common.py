import frappe
import json

@frappe.whitelist(allow_guest=True)
def get_user_login_data():
    data = get_request_form_data()
    user = frappe.get_doc("User", data.email)
    user_role = user.roles[0].role

    if user_role == "Industry":
        role = "Industry"
        industry = frappe.get_doc("Industry", {'email': data.email})
        return json.dumps({
            "first_name": industry.first_name, 
            "last_name": industry.last_name, 
            "email": data.email, 
            "role": role,
            "account_status": industry.account_status,
            "type": industry.sector,
            "bio": industry.bio
            })
    elif user_role == "Academia":
        role = "Academia"
        academia = frappe.get_doc("Academia", {'email': data.email})
        return json.dumps({
            "first_name": academia.first_name, 
            "last_name": academia.last_name, 
            "email": academia.email, 
            "role": role,
            "account_status": academia.account_status,
            "type": "Academia",
            "bio": academia.bio
            })
    frappe.local.response.http_status_code = 404
    frappe.local.response.message = "Not Found"
    
def get_request_form_data():
	if frappe.local.form_dict.data is None:
		data = frappe.safe_decode(frappe.local.request.get_data())
	else:
		data = frappe.local.form_dict.data

	try:
		return frappe.parse_json(data)
	except ValueError:
		return frappe.local.form_dict