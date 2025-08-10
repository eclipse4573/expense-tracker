import streamlit as st
import pandas as pd
import os
import login

def customise():
    if login.st.session_state.logged_in:
        category_file = f"customisation/categories/{login.st.session_state.username}.csv"

        if not os.path.exists(category_file):
            pd.DataFrame([{"category": "Food"}]).to_csv(category_file, index = False)
        
        def load_categories():
            return pd.read_csv(category_file)
        
        def add_category(category):
            df = load_categories()
            if category in df["category"].values:
                return False
            df.loc[len(df)] = [category]
            df.to_csv(category_file, index = False)
            return True
        
        def delete_category(category):
            df = load_categories()
            if category not in df["category"].values:
                return False
            df = df.drop(index = df["category"].tolist().index(category))
            df.to_csv(category_file, index = False)
            return True
        
        with st.form("category", clear_on_submit = True):
            col1, col2 = st.columns(2)
            with col1:
                action = st.selectbox("Action", ["Add New Category", "Delete Category"])
            with col2:
                new_category = st.text_input("Category Name:")
            if st.form_submit_button("Update"):
                if action == "Add New Category":
                    if not add_category(new_category):
                        st.toast("Category already exists!", icon = "❌")
                    else:
                        st.toast("Category added!", icon = "✅")
                else:
                    if not delete_category(new_category):
                        st.toast("Category does not exist!", icon = "❌")
                    else:
                        st.toast("Category deleted!", icon = "✅")
