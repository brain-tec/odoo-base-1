from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalExtended(CustomerPortal):
    CustomerPortal.MANDATORY_BILLING_FIELDS.append("allow_email_marketing")

