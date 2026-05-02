
from __future__ import annotations

import pandas as pd
import streamlit as st

from config import DEMO_USERS, ROLE_ACCESS


def render_users_page() -> None:
    st.markdown('<div class="page-title">Users</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Manage staff access structure. Current users are demo users for testing.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    rows = []

    for email, user in DEMO_USERS.items():
        role = user.get("role", "Viewer")
        allowed_pages = ROLE_ACCESS.get(role, [])

        rows.append(
            {
                "email": email,
                "name": user.get("name", ""),
                "role": role,
                "access": ", ".join(allowed_pages),
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info("Real user management can be connected later through database or admin settings.")
