import frappe
from frappe.core.doctype.user.user import User

class CustomUser(User):
    def send_welcome_mail_to_user(self):
        from frappe.utils import get_url

        link = self.reset_password()
        parsed_url = urlparse(link)
        link = parse_qs(parsed_url.query)['key'][0]
        link = "http://134.119.192.60:3001/verify-user?key=" + link 
        subject = None
        method = frappe.get_hooks("welcome_email")
        if method:
            subject = frappe.get_attr(method[-1])()
        if not subject:
            site_name = frappe.db.get_default("site_name") or frappe.get_conf().get("site_name")
            if site_name:
                subject = _("Welcome to {0}").format(site_name)
            else:
                subject = _("Complete Registration")

        self.send_login_mail(
            subject,
            "new_user",
            dict(
                link=link,
                site_url=get_url(),
            ),
        )