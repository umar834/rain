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
			"job_title": industry.job_title,
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
			"job_title": academia.designation,
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

@frappe.whitelist(allow_guest=True)
def update_profile(first_name=None, last_name=None, title=None, bio=None):
	roles = frappe.get_roles(frappe.session.user)
	user = frappe.session.user
	if "Industry" in roles:
		industry = frappe.get_doc("Industry", {"email": user})
		user = frappe.get_doc("User",user)
		user.first_name = first_name
		user.last_name = last_name
		user.save()

		industry.first_name = first_name
		industry.last_name = last_name
		industry.bio = bio
		industry.job_title = title
		industry.save()
		return json.dumps({'Success': 'Profile information updated!'}) 
	elif "Academia" in roles:
		academia = frappe.get_doc("Academia", {"email": user})
		user = frappe.get_doc("User",user)
		user.first_name = first_name
		user.last_name = last_name
		user.save()

		academia.first_name = first_name
		academia.last_name = last_name
		academia.bio = bio
		academia.designation = title
		academia.save()
	else:
		frappe.local.response.http_status_code = 400
		frappe.local.response.message = "Nothing"

@frappe.whitelist(allow_guest=True)
def get_thematic_areas():
	thematic_areas = frappe.get_all("Thematic Area")
	index = 0
	for thematic_area in thematic_areas:
		thematic_sub_areas = frappe.get_all("Sub Thematic Table",fields=["*"], filters={'parent': thematic_area.name})
		thematic_areas[index].thematic_sub_areas = thematic_sub_areas
		index += 1
	return thematic_areas