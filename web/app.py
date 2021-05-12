import streamlit as st
import os
import pandas as pd
import joblib
import numpy as np
import bcrypt
from db import *
from analytics import *


def main():
    st.title("Stroke Prediction Tool \n"
             "Artificial Intelligence for Healthcare\n\n")

    st.text("Welcome in a Machine Learning Healthcare Web Application \n"
            "This tool will predict for you the probability of getting a stroke\n"
            "based on health parameters and life habits!")


    st.header("Prediction tool")
    age = st.number_input("Age", 0, 100)
    weight = st.number_input("Weight in kg", 0, 200)
    height = st.number_input("Height in meters", 1.0, 2.5)
    bmi = weight / (height**2)
    avg_glucose_level =st.number_input("Average Glucose Level", 0, 200)

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

    choosed_model = st.radio("Choose an AI model for prediction", ["RandomForestClassifier","Decision Tree", "Logistic Regression", "KNN"])
    if choosed_model == "Decision Tree":
        model = joblib.load(open(os.path.join("models/DecisionTreeClassifier.pkl"), "rb"))
    elif choosed_model == "RandomForestClassifier":
        model = joblib.load(open(os.path.join("models/RandomForestClassifier.pkl"), "rb"))
    elif choosed_model == "Logistic Regression":
        model = joblib.load(open(os.path.join("models/LogisticRegression.pkl"), "rb"))
    else:
        model = joblib.load(open(os.path.join("models/KNeighborsClassifier.pkl"), "rb"))

    run_prediction = st.button("Predict")
    if run_prediction:
        prediction = model.predict(np.array(sample).reshape(1, -1))
        prediction_map = {0: "Healthy",
                          1: "High Stroke Probability"}

        if prediction == 0:
            st.success(prediction_map[prediction[0]])
        else:
            st.warning(prediction_map[prediction[0]])


    # Analytics
    st.header("Humans Health Parameters and Habits Visualisations")
    data = pd.read_csv("../web/dataset/healthcare-dataset-stroke-data.csv")
    st.dataframe(data)
    st.text("Female and male stroke statistical statement")
    fig = plot_gender_stroke(data)
    st.write(fig)

    fig6 = plot_distribution_stroke_vs(data, "age")
    st.pyplot(fig6)
    fig7 = plot_distribution_stroke_vs(data, "bmi")
    st.pyplot(fig7)
    fig8 = plot_distribution_stroke_vs(data, "avg_glucose_level")
    st.pyplot(fig8)

    fig1 = plot_scatter_age_stroke_feature(data, "bmi", range_y=[18, 50])
    st.write(fig1)
    fig3 = plot_scatter_age_stroke_feature(data, "avg_glucose_level", range_y=[60, 200])
    st.write(fig3)



# if __name__ == "__main__":
main()
