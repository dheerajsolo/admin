import streamlit as st


def _go(label: str, target: str, active: bool = False):
    container_class = "sidebar-active" if active else "sidebar-normal"
    with st.container():
        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.switch_page(target)
        st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar(active_page: str = "Dashboard"):
    with st.sidebar:
        st.markdown(
            """
            <div class="brand-block">
                <div class="brand-title">Jewlio</div>
                <div class="brand-subtitle">Operations Dashboard</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-section-title">Overview</div>', unsafe_allow_html=True)
        _go("Dashboard", "app.py", active_page == "Dashboard")
        _go("Orders", "pages/2_Orders.py", active_page == "Orders")
        _go("Inventory", "pages/3_Inventory.py", active_page == "Inventory")
        _go("Shipping", "pages/4_Shipping.py", active_page == "Shipping")
        _go("Returns", "pages/5_Returns.py", active_page == "Returns")
        _go("Reports", "pages/6_Reports.py", active_page == "Reports")

        st.markdown('<div class="side-section-title">System</div>', unsafe_allow_html=True)
        _go("Settings", "pages/6_Reports.py", active_page == "Settings")

        st.markdown(
            """
            <div class="side-note">
                Read-only mode enabled.<br>
                WooCommerce data is being fetched through REST API.
            </div>
            """,
            unsafe_allow_html=True,
        )
