import streamlit as st

USERS = {
    "manager": {"password": "123", "role": "Manager"},
    "staff": {"password": "123", "role": "Staff"},
}

def init_auth():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "role" not in st.session_state:
        st.session_state.role = None

def login_form():
    st.title("Management Login")
    st.caption("Retail Sales Analytics Dashboard")

    with st.form("mgmt_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user_data = USERS.get(username.strip())
            if user_data and user_data["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.session_state.role = user_data["role"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

def logout_button():
    st.sidebar.markdown("---")
    st.sidebar.write(f"User: **{st.session_state.username}**")
    st.sidebar.write(f"Role: **{st.session_state.role}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()
