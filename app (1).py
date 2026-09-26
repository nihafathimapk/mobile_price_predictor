import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

try:
    model = joblib.load('mobile_price_model.pkl')
except FileNotFoundError:
    st.error("Error: 'mobile_price_model.pkl' not found. Please ensure it is in the same directory as this script.")

# Page configuration
st.set_page_config(
    page_title="MobileValue - Smart Price Predictor",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 38px;
            color: #4C6E91;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #6F6875;
            font-size: 18px;
            margin-bottom: 20px;
        }

        .stButton>button {
            width: 100%;
            background-color: #A9C6DE;
            color: #2F3E4D;
            font-size: 18px;
            font-weight: 600;
            padding: 10px;
            border-radius: 15px;
            border: 1px solid #C9DCC5;
        }

        .stButton>button:hover {
            background-color: #8FB3D1;
            color: white;
        }

        .card {
            background-color: #FFFDF7;
            box-shadow: 1px 1px 10px #E6DDE0;
            padding: 14px;
            border-radius: 15px;
            border: 1px solid #EADCC8;
        }

        .footer{
            text-align : center;
            color: #6F6875;
            font-size: 14px;
            margin-top: 25px;
        }

    </style>
""", unsafe_allow_html=True)

# App header
st.markdown('<div class="title">📱 MobileValue</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Mobile Phone Price Predictor</div>', unsafe_allow_html=True)

# Input section
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    sale_date = st.date_input("Sale Date", datetime.now())
    units_sold = st.number_input("Units Sold", 0, 1000, step=1, value=50)
    customer_age = st.number_input("Customer Age", 1, 100, step=1, value=30)
with col2:
    customer_gender = st.selectbox("Customer Gender", ["Female", "Male", "Other"])
    payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Online", "Cash"])
st.markdown('</div>', unsafe_allow_html=True)

# Prediction button
st.write("")
predict_btn = st.button("Predict Price")
if predict_btn:
    year = sale_date.year
    month = sale_date.month
    day = sale_date.day
    day_of_week = sale_date.weekday()
    is_weekend = 1 if day_of_week >= 5 else 0

    input_data = pd.DataFrame({
        'UnitsSold': [units_sold],
        'CustomerAge': [customer_age],
        'Year': [year],
        'Month': [month],
        'Day': [day],
        'DayOfWeek': [day_of_week],
        'IsWeekend': [is_weekend],
        'CustomerGender': [customer_gender],
        'PaymentMethod': [payment_method]
    })
    predicted_price = model.predict(input_data)[0]
    predicted_price = max(predicted_price, 0)
    st.success(f"💰 **Estimated Price:** ${predicted_price:.2f}")

# Footer with copyright
st.write("---")
