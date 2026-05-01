import streamlit as st


def sidebar_button(label: str, page: str, active: bool = False):
    active_class = "active-nav" if active else ""

    st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)

    if st.button(label, key=f"nav_{label}", use_container_width=True):
        st.switch_page(page)

    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar(active_page: str = "Dashboard"):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-title">Jewlio</div>
                <div class="sidebar-subtitle">Operations Dashboard</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-section">Overview</div>', unsafe_allow_html=True)

        sidebar_button("Dashboard", "app.py", active_page == "Dashboard")
        sidebar_button("Orders", "pages/2_Orders.py", active_page == "Orders")
        sidebar_button("Inventory", "pages/3_Inventory.py", active_page == "Inventory")
        sidebar_button("Shipping", "pages/4_Shipping.py", active_page == "Shipping")
        sidebar_button("Returns", "pages/5_Returns.py", active_page == "Returns")
        sidebar_button("Reports", "pages/6_Reports.py", active_page == "Reports")

        st.markdown('<div class="sidebar-section">System</div>', unsafe_allow_html=True)

        sidebar_button("Settings", "pages/6_Reports.py", active_page == "Settings")

        st.markdown(
            """
            <div style="
                margin-top: 28px;
                padding-top: 18px;
                border-top: 1px solid rgba(234,239,239,0.15);
                color: #BFC9D1;
                font-size: 12px;
                line-height: 1.5;
            ">
                Read-only mode<br>
                WooCommerce REST API
            </div>
            """,
            unsafe_allow_html=True,
        )
