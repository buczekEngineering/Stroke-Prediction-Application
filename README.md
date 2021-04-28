# Stroke-Prediction-Application

## Goal
The goal of the project is to create a machine learning-based web application with Flask Framework that will predict the probability of getting a stroke in the futures.

## Dataset 
https://www.kaggle.com/fedesoriano/stroke-prediction-dataset/tasks?taskId=3281 

## Project Workflow
1. Data Preparation 
2. Exploratory Data Analysis
3. Feature Selection 
4. Creating a Pipeline
5. Writing tests for different levels:  input data, feature engineering, effectiveness of different pipelines 
6. Serialization 
7. Deployment
8. Testing in shadow mode (production environment)



Analyzed features: 
    id: unique identifier
    gender: "Male", "Female" or "Other"
    age: age of the patient
    hypertension: 0 if the patient doesn't have hypertension, 1 if the patient has hypertension
    heart_disease: 0 if the patient doesn't have any heart diseases, 1 if the patient has a heart disease
    ever_married: "No" or "Yes"
    work_type: "children", "Govt_jov", "Never_worked", "Private" or "Self-employed"
    Residence_type: "Rural" or "Urban"
    avg_glucose_level: average glucose level in blood
    bmi: body mass index
    smoking_status: "formerly smoked", "never smoked", "smokes" or "Unknown"*
    stroke: 1 if the patient had a stroke or 0 if not
