import streamlit as st
import pandas as pd
# import hashlib
import os

def first_page():

    st.title("Expense Tracker 📈")

    users_file = "users.csv"

    def load_users():
        return pd.read_csv(users_file)

    def hash_password(password):
        # return hashlib.sha256(password.encode()).hexdigest()
        return password

    if not os.path.exists(users_file):
        pd.DataFrame({"username": ["test"],
                    "password": hash_password("123")}).to_csv(users_file, index = False)

    def save_user(username, password):
        df = load_users()
        if username in df["username"].values:
            return False
        df.loc[len(df)] = [username, hash_password(password)]
        df.to_csv(users_file, index = False)
        return True

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            with st.form("login"):
                user = st.text_input("Username:")
                pwd = st.text_input("Password:", type = "password")
                if st.form_submit_button("Login"):
                    df = load_users()
                    if user in df["username"].values:
                        stored_pwd = df[df["username"] == user]["password"].values[0]
                        if hash_password(pwd) == stored_pwd:
                            st.session_state.logged_in = True
                            st.session_state.username = user
                            st.rerun()
                        else:
                            st.toast("Incorrect Password!", icon = "❌")
                    else:
                        st.toast("User not found!", icon = "❌")
        with tab2:
            with st.form("sign up"):
                user = st.text_input("New Username:")
                pwd = st.text_input("New Password:", type = "password")
                if st.form_submit_button("Sign Up"):
                    if save_user(user, pwd):
                        st.toast("User created! You can now log in.", icon = "✅")
                    else:
                        st.toast("Username already exists!", icon = "❌")
