import streamlit as st
import os
import pandas as pd
import joblib
import numpy as np
import bcrypt
from db import *
from analytics import plot_gender_stroke, plot_scatter_bmi_glu


def hash_password(password):
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pwd


def is_correct_password(password, hashed_pwd_db):
    if bcrypt.hashpw(password.encode("utf-8"), hashed_pwd_db) == hashed_pwd_db:
        return True
    else:
        return False


def login(username, hashed_pwd_db):
    data = login_user(username, hashed_pwd_db)
    return data


def main():
    st.title("Stroke Prediction Tool \n"
             "Artificial Intelligence for Healthcare\n\n")

    st.text("Welcome in a Machine Learning Healthcare Web Application \n"
            "This tool will predict for you the probability of getting a stroke\n"
            "based on health parameters and life habits!")

    menu = ["Learn more about the app", "Login", "Register"]
    submenu = ["Predict your health", "Analytics", "How does the prediction work?"]

    choice = st.selectbox("Menu", menu)

    if choice == "Register":
        with st.form(key="form1"):
            st.subheader("Let's get you on board")
            name = st.text_input("Full Name", "")
            email = st.text_input("Email", "")
            password = st.text_input("Password", type="password")
            confirm_p = st.text_input("Confirm Password", type="password")
            submit_r = st.form_submit_button(label="Register")
            st.text("Already have an account? Go to Login!")
            userExists = False

        if submit_r:
            if not is_username_free(name):
                st.warning("Username already exists!")
                userExists = True
            if password == "" or confirm_p == "":
                st.warning("Invalid data format. Please provide a password")
            if password != confirm_p:
                st.warning("Passwords are not the same!")

            if confirm_p == password and password != "" and name != "" and email != "" and userExists == False:
                hashed_pwd = hash_password(password)
                create_usertable()
                add_userdata(name, hashed_pwd, email)
                st.success("Hello {}! Your are registered!".format(name))
                st.info("Login in to get started!")


    elif choice == "Login":
        st.subheader("Welcome back!\n"
                             "please login to your account")

        with st.form(key="form2"):

            username = st.text_input("User Id", "")
            password = st.text_input("Password", type="password")
            submit_log = st.form_submit_button("Login")
        if submit_log:
            #with st.form(key="form5"):
            create_usertable()
            hashed_pwd_db = validate_hashed_password(username)
            if not is_correct_password(password, hashed_pwd_db):
                st.warning("Invalid password!")
            else:
                st.success("Welcome back {}".format(username))
                data = login(username, hashed_pwd_db)

                if data != []:
                    count = 0
                    activity = st.selectbox("Choose an action", submenu, key=count)
                    count += 1

                    if activity == "Analytics":
                        with st.form(key="form6"):
                            st.subheader("Humans Health Parameters and Habits Visualisation Platform")
                            data = pd.read_csv("../web/dataset/healthcare-dataset-stroke-data.csv")
                            st.dataframe(data)
                            st.text("Female and male stroke statistical statement")
                            fig = plot_gender_stroke(data)
                            st.write(fig)

                            targets = ["heart_disease", "hypertension", "stroke", "age"]

                            key = np.random.randint(10000, size=1)

                            target_feature = st.selectbox(
                                "Peak a target feature to see the tendency coming from the relation between bmi and average glucose level",
                                targets, key=key[0])

                            fig1 = plot_scatter_bmi_glu(data, target_feature)
                            st.write(fig1)



                    elif activity == "Predict your health":
                        #with st.form(key="form7"):
                        with st.beta_expander("Prediction"):
                            col1, col2 = st.beta_columns([1,1])
                            st.subheader("Prediction tool")
                            with col1:
                                age = st.number_input("Age", 0, 100)
                                weight = st.number_input("Weight in kg", 0, 200)
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

                            with col2:
                                height = st.number_input("Height in meters", 1.0, 2.5)
                                bmi = weight / height
                                avg_glucose_level = st.number_input("Average Glucose Level", 0, 200)

                                residence_type = st.radio("Residence type", ["Rural", "Urban"])
                                if residence_type == "Rural":
                                    residence_type = 0
                                else:
                                    residence_type = 1

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

                            choosed_model = st.radio("Choose an AI model for prediction",
                                                     ["RandomForestClassifier", "Decision Tree", "Logistic Regression",
                                                      "KNN"])
                            if choosed_model == "Decision Tree":
                                model = joblib.load(open(os.path.join("web/models/DecisionTreeClassifier.pkl"), "rb"))
                            elif choosed_model == "RandomForestClassifier":
                                model = joblib.load(open(os.path.join("web/models/RandomForestClassifier.pkl"), "rb"))
                            elif choosed_model == "Logistic Regression":
                                model = joblib.load(
                                    open(os.path.join("web/models/LogisticRegression_ftuning_1.pkl"), "rb"))
                            else:
                                model = joblib.load(open(os.path.join("web/models/KNeighborsClassifier.pkl"), "rb"))

                            run_prediction = st.button(label="Predict")

                        with st.beta_expander("Check results"):
                            if run_prediction:
                                prediction = model.predict(np.array(sample).reshape(1, -1))

                                st.text(prediction)
                                prediction_map = {0: "Healthy",
                                                  1: "High Stroke Probability"}

                                if prediction == 0:
                                    st.success(prediction_map[prediction[0]])
                                else:
                                    st.warning(prediction_map[prediction[0]])


    elif choice == "Learn more about the app":
        st.subheader("AI-based healthcare app")


if __name__ == "__main__":
    main()
