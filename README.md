# 🥂 Wine Quality Classifier

A Streamlit web app that predicts the quality of white wines based on their chemical properties — powered by a hybrid machine learning model that combines Random Forest and Decision Tree classifiers.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-brightgreen)](https://wine-quality-prediction-production.up.railway.app/)

---

## 📊 About the Project

This project is built on the **White Wine Quality Dataset** from the UCI Machine Learning Repository. It includes physicochemical data for white wines, each labeled with a quality score from 3 to 9 (converted here to **Low**, **Medium**, or **High** quality classes for interpretability).

The goal is to build a reliable model that can help producers to estimate wine quality from lab measurements.

---

## 🤖 Model Approach

A **hybrid classification strategy** was implemented:

- 🟢 **Random Forest** is used as the main model for its high performance in predicting the dominant "Medium" class.
- 🟠 **Decision Tree** steps in when RF is not confident or when detecting minority classes ("Low" or "High") is more important.
- This increases the accuracy for underrepresented classes without sacrificing overall performance.

Class imbalance is handled with **SMOTE**, and features were selected based on statistical tests and model performance.

---

## 🧪 Features Used

The model uses the following physicochemical properties:

- `Alc` — Alcohol content  
- `Cl` — Chlorides  
- `TSO2` — Total Sulfur Dioxide  
- `VA` — Volatile Acidity  
- `FSO2` — Free Sulfur Dioxide  
- `FA` — Fixed Acidity  

---

## 🚀 App Features

- 🧪 **Input custom wine samples** or use example data  
- 📈 **Instant prediction** of wine quality (Low / Medium / High)  
- 🧠 **Confidence scores** for used model  
- 🔍 **Simple diagnostic feedback** tips to improve quality

