from __future__ import annotations

import streamlit as st

from controllers.auth_controller import can_access_page

from modules.overview.page import render_overview_page
from modules.orders.page import render_orders_page
from modules.inventory.page import render_inventory_page
from modules.shipping.page import render_shipping_page
from modules.coupons.page import render_coupons_page
from modules.reviews.page import render_reviews_page
from modules.blog.page import render_blog_page
from modules.email_support.page import render_email_support_page
from modules.seo.page import render_seo_page
from modules.push_notifications.page import render_push_notifications_page
from modules.reports.page import render_reports_page
from modules.users.page import render_users_page
from modules.settings.page import render_settings_page


PAGE_ROUTES = {
    "Overview": render_overview_page,
    "Orders": render_orders_page,
    "Inventory": render_inventory_page,
    "Shipping": render_shipping_page,
    "Coupons": render_coupons_page,
    "Reviews": render_reviews_page,
    "Blog": render_blog_page,
    "Email Support": render_email_support_page,
    "SEO": render_seo_page,
    "Push Notifications": render_push_notifications_page,
    "Reports": render_reports_page,
    "Users": render_users_page,
    "Settings": render_settings_page,
}


def render_selected_page(page_name: str) -> None:
    if not can_access_page(page_name):
        st.error("You do not have access to this section.")
        render_overview_page()
        return

    page_function = PAGE_ROUTES.get(page_name, render_overview_page)
    page_function()
