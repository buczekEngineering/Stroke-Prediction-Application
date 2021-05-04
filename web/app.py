import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
import sklearn
import bcrypt
from pymongo import MongoClient
from db import *

def hash_password(password):
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pwd

def is_correct_password(password, hashed_pwd_db):
    if bcrypt.hashpw(password.encode("utf-8"), hashed_pwd_db) == hashed_pwd_db:
        return True
    else:
        return False
def main():
    st.title("Stroke Prediction Tool \n"
             "Artificial Intelligence for Healthcare\n\n")

    st.text("Welcome in a Machine Learning Healtcare Web Application \n"
            "This tool will predict for you the probability of getting a stroke\n"
            "based on health parameters and life habits!")

    menu = ["Learn more about the app", "Login", "New User?  Register!"]
    submenu = ["Predict your health", "Monitoring Dashboard", "Visualization", "How does it work?"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.sidebar.subheader("Welcome back!\n"
                             "please login to your account")
        username = st.sidebar.text_input("User Id", "")
        password = st.sidebar.text_input("Password", type="password")
        submit = st.sidebar.button("Login")
        if submit:
            create_usertable()
            # bug! the hashed password must be cleaned with regex
            hashed_pwd_db = validate_hashed_password(username)
            st.sidebar.text(hashed_pwd_db)
            if is_correct_password(password, hashed_pwd_db):
                st.sidebar.success("Welcome back {}".format(username))

                result = login_user(username, hashed_pwd_db)
                st.sidebar.text(hashed_pwd_db)
                if result:
                    st.sidebar.success("Welcome back {}".format(username))
                    activity = st.sidebar.selectbox("Choose an action", submenu)
                    if activity == "Predict your health":
                        st.subheader("Prediction tool")
                        age = st.number_input("Age", 0, 100)
                        weight = st.number_input("Weight in kg", 0, 200)
                        height = st.number_input("Height in meters", 1.0, 2.5)
                        bmi = weight / height
                        avg_glucose_level = st.number_input("Average Glucose Level", 0, 200)

                        residence_type = st.radio("Residence type", ["Rural", "Urban"])
                        if residence_type == "Rural":
                            residence_type = 0
                        else:
                            residence_type = 1

                        hypertension = st.radio("Hypertension", ["Yes", "No"])
                        if hypertension == "Yes":
                            hypertension = 1
                        else:
                            hypertension = 0

                        heart_dis = st.radio("Heart Diseases", ["Yes", "No"])
                        if heart_dis == "Yes":
                            heart_dis = 1
                        else:
                            heart_dis = 0

                        ever_married = st.radio("Ever Married", ["Yes", "No"])
                        if ever_married == "Yes":
                            ever_married = 1
                        else:
                            ever_married = 0

                        columns = ["age", "avg_glucose_level", "bmi", "residence_type",
                                   "hypertension", "ever_married", "heart_dis"]
                        sample = pd.DataFrame(columns=columns)
                        sample.loc[0] = [age, avg_glucose_level, bmi, residence_type,
                                         hypertension, ever_married, heart_dis]

                        st.text("Your Parameters")
                        st.dataframe(sample)

                        choosed_model = st.radio("Choose an AI model for prediction", ["Logistic Regression", "KNN"])
                        if choosed_model == "Logistic Regression":
                            model = joblib.load("models/LogisticRegression.pkl")
                        else:
                            model = joblib.load("models/KNeighborsClassifier.pkl")

                        run_prediction = st.button("Predict")
                        if run_prediction:
                            prediction = model.predict(np.array(sample).reshape(1, -1))
                            prediction_map = {0: "Healthy",
                                              1: "High Stroke Probability"}

                            if prediction == 0:
                                st.success(prediction_map[prediction[0]])
                            else:
                                st.warning(prediction_map[prediction[0]])



    if choice == "New User?  Register!":
        st.subheader("Let's get you on board")
        name = st.text_input("Full Name", "")
        email = st.text_input("Email", "")
        password = st.text_input("Password", type="password")
        confirm_p = st.text_input("Confirm Password", type="password")
        submit = st.button("Register")
        st.text("Already have an account? Go to Login!")
        if submit:
            if password == "" or confirm_p =="":
                st.warning("Invalid data format. Please provide a password")
            if password != confirm_p:
                 st.warning("Passwords are not the same!")

            if confirm_p == password and password != "" and name != "" and email != "":
                hashed_pwd = hash_password(password)
                create_usertable()
                add_userdata(name, hashed_pwd, email)
                st.success("Hello {}! Your are registered!".format(name))
                st.info("Login in to get started!")






    if choice == "Learn more about the app":
        st.subheader("AI-based healthcare app")


if __name__ == "__main__":
    main()
