import streamlit as st
import pandas as pd
import joblib

# PAGE CONFIGURATION

st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="wide"
)

# CUSTOM CSS


st.markdown("""
<style>

    /* ================================
       GLOBAL
    ================================= */

    .stApp {
        background: linear-gradient(
            135deg,
            #f4f8fb 0%,
            #eef5f7 100%
        );
        font-family: "Segoe UI", sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ================================
       HEADER
    ================================= */

    .main-header {
        background: linear-gradient(
            135deg,
            #0f766e,
            #14b8a6
        );

        padding: 38px 45px;
        border-radius: 24px;

        color: white;

        margin-bottom: 30px;

        box-shadow:
            0 12px 35px rgba(15, 118, 110, 0.25);
    }

    .main-header h1 {
        font-size: 42px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
    }

    .main-header p {
        font-size: 18px;
        margin-top: 10px;
        margin-bottom: 0;
        opacity: 0.95;
    }


    /* ================================
       INFORMATION CARDS
    ================================= */

    .info-card {
        background: white;

        padding: 25px 20px;

        border-radius: 18px;

        text-align: center;

        min-height: 125px;

        box-shadow:
            0 6px 20px rgba(0, 0, 0, 0.06);

        border: 1px solid #e5e7eb;

        transition: all 0.3s ease;
    }

    .info-card:hover {
        transform: translateY(-4px);

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.10);
    }

    .info-card h3 {
        margin: 0;

        color: #0f766e;

        font-size: 25px;

        font-weight: 700;
    }

    .info-card p {
        color: #64748b;

        font-size: 16px;

        margin-top: 12px;
    }


    /* ================================
       SECTION TITLE
    ================================= */

    .section-title {
        background: white;

        padding: 18px 24px;

        border-radius: 15px;

        margin-top: 30px;
        margin-bottom: 20px;

        border-left: 5px solid #14b8a6;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.05);
    }

    .section-title h2 {
        margin: 0;

        color: #134e4a;

        font-size: 25px;

        font-weight: 700;
    }


    /* ================================
       INPUT LABELS
    ================================= */

    label {
        font-weight: 600 !important;

        color: #334155 !important;
    }


    /* ================================
       INPUT BOXES
    ================================= */

    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    div[data-baseweb="select"] {
        border-radius: 10px;
    }


    /* ================================
       PREDICT BUTTON
    ================================= */

    .stButton > button {

        width: 100%;

        height: 58px;

        border-radius: 14px;

        border: none;

        background: linear-gradient(
            135deg,
            #0f766e,
            #14b8a6
        );

        color: white;

        font-size: 19px;

        font-weight: 700;

        box-shadow:
            0 7px 18px rgba(20, 184, 166, 0.25);

        transition: all 0.3s ease;
    }

    .stButton > button:hover {

        transform: translateY(-2px);

        background: linear-gradient(
            135deg,
            #115e59,
            #0d9488
        );

        box-shadow:
            0 10px 25px rgba(20, 184, 166, 0.35);
    }


    /* ================================
       RESULT CARD
    ================================= */

    .result-card {

        background: white;

        padding: 30px;

        border-radius: 20px;

        margin-top: 20px;

        margin-bottom: 20px;

        text-align: center;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.07);

        border: 1px solid #e5e7eb;
    }

    .result-title {

        color: #475569;

        font-size: 18px;

        font-weight: 600;

        margin-bottom: 15px;
    }


    /* ================================
       HIGH RISK
    ================================= */

    .risk-high {

        background: #fee2e2;

        color: #b91c1c;

        padding: 20px;

        border-radius: 15px;

        font-size: 27px;

        font-weight: 800;

        border: 1px solid #fecaca;
    }


    /* ================================
       MODERATE RISK
    ================================= */

    .risk-moderate {

        background: #fef3c7;

        color: #b45309;

        padding: 20px;

        border-radius: 15px;

        font-size: 27px;

        font-weight: 800;

        border: 1px solid #fde68a;
    }


    /* ================================
       LOW RISK
    ================================= */

    .risk-low {

        background: #dcfce7;

        color: #15803d;

        padding: 20px;

        border-radius: 15px;

        font-size: 27px;

        font-weight: 800;

        border: 1px solid #bbf7d0;
    }


    /* ================================
       CONFIDENCE CARD
    ================================= */

    .confidence-card {

        background: linear-gradient(
            135deg,
            #ecfeff,
            #f0fdfa
        );

        padding: 25px;

        border-radius: 18px;

        text-align: center;

        border: 1px solid #ccfbf1;

        margin-top: 20px;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.04);
    }

    .confidence-title {

        color: #475569;

        font-size: 16px;

        font-weight: 600;
    }

    .confidence-value {

        color: #0f766e;

        font-size: 40px;

        font-weight: 800;

        margin-top: 5px;
    }


    /* ================================
       FOOTER
    ================================= */

    .footer {

        background: #181b24;

        color: #f8fafc;

        padding: 28px;

        border-radius: 16px;

        text-align: center;

        margin-top: 40px;

        font-size: 15px;
    }

    .footer p {

        margin: 7px 0;

    }

    .footer .warning {

        color: #fbbf24;

        font-weight: 600;

    }

    .footer .brand {

        color: #5eead4;

        font-size: 18px;

        font-weight: 700;

    }


    /* ================================
       EXPANDER
    ================================= */

    .streamlit-expanderHeader {

        font-weight: 600;

        color: #134e4a;
    }

</style>
""", unsafe_allow_html=True)

# LOAD MODEL AND FEATURES

model = joblib.load("diabetes_risk_model.pkl")

feature_columns = joblib.load(
    "feature_columns.pkl"
)


# HEADER

st.html("""
<div class="main-header">

    <h1>🩺 Diabetes Risk Prediction</h1>

    <p>
        AI-powered diabetes risk assessment using Machine Learning
    </p>

</div>
""")


# INFORMATION CARDS

info1, info2, info3 = st.columns(3)


with info1:

    st.html("""
    <div class="info-card">

        <h3>🤖 AI Powered</h3>

        <p>
            Machine Learning based prediction
        </p>

    </div>
    """)


with info2:

    st.html("""
    <div class="info-card">

        <h3>📊 3 Risk Levels</h3>

        <p>
            Low, Moderate and High
        </p>

    </div>
    """)


with info3:

    st.html("""
    <div class="info-card">

        <h3>⚡ Fast Prediction</h3>

        <p>
            Instant model prediction
        </p>

    </div>
    """)

# PATIENT INFORMATION

st.html("""
<div class="section-title">

    <h2>👤 Patient Information</h2>

</div>
""")


col1, col2, col3 = st.columns(3)


# COLUMN 1

with col1:

    Age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=30
    )

    Gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    BMI = st.number_input(
        "BMI",
        min_value=0.0,
        max_value=100.0,
        value=22.0
    )

    Waist_Circumference_cm = st.number_input(
        "Waist Circumference (cm)",
        min_value=0.0,
        max_value=200.0,
        value=80.0
    )

    Blood_Glucose = st.number_input(
        "Blood Glucose",
        min_value=0.0,
        max_value=500.0,
        value=100.0
    )

    HbA1c = st.number_input(
        "HbA1c",
        min_value=0.0,
        max_value=20.0,
        value=5.5
    )

    Fasting_Blood_Sugar = st.number_input(
        "Fasting Blood Sugar",
        min_value=0.0,
        max_value=500.0,
        value=100.0
    )

    Insulin_Level = st.number_input(
        "Insulin Level",
        min_value=0.0,
        max_value=1000.0,
        value=15.0
    )

# COLUMN 2

with col2:

    Blood_Pressure_Systolic = st.number_input(
        "Systolic Blood Pressure",
        min_value=50,
        max_value=250,
        value=120
    )

    Blood_Pressure_Diastolic = st.number_input(
        "Diastolic Blood Pressure",
        min_value=30,
        max_value=150,
        value=80
    )

    Total_Cholesterol = st.number_input(
        "Total Cholesterol",
        min_value=0.0,
        max_value=500.0,
        value=180.0
    )

    HDL = st.number_input(
        "HDL",
        min_value=0.0,
        max_value=200.0,
        value=50.0
    )

    LDL = st.number_input(
        "LDL",
        min_value=0.0,
        max_value=400.0,
        value=100.0
    )

    Triglycerides = st.number_input(
        "Triglycerides",
        min_value=0.0,
        max_value=1000.0,
        value=150.0
    )

    Physical_Activity_Level = st.selectbox(
        "Physical Activity Level",
        ["Low", "Moderate", "High"]
    )

    Exercise_Hours_Per_Week = st.number_input(
        "Exercise Hours Per Week",
        min_value=0.0,
        max_value=100.0,
        value=3.0
    )

    Daily_Walking_Minutes = st.number_input(
        "Daily Walking Minutes",
        min_value=0.0,
        max_value=500.0,
        value=30.0
    )

# COLUMN 3

with col3:

    Diet_Quality = st.selectbox(
        "Diet Quality",
        ["Poor", "Average", "Good"]
    )

    Sugar_Intake_Level = st.selectbox(
        "Sugar Intake Level",
        ["Low", "Moderate", "High"]
    )

    Sleep_Hours = st.number_input(
        "Sleep Hours",
        min_value=0.0,
        max_value=24.0,
        value=7.0
    )

    Stress_Level = st.selectbox(
        "Stress Level",
        ["Low", "Moderate", "High"]
    )

    Smoking_Status = st.selectbox(
        "Smoking Status",
        ["Never", "Former", "Current"]
    )

    Alcohol_Consumption = st.selectbox(
        "Alcohol Consumption",
        ["None", "Moderate", "High"]
    )

    Family_History_Diabetes = st.selectbox(
        "Family History of Diabetes",
        ["No", "Yes"]
    )

    Hypertension = st.selectbox(
        "Hypertension",
        ["No", "Yes"]
    )

# ADDITIONAL INFORMATION

st.html("""
<div class="section-title">

    <h2>📋 Additional Information</h2>

</div>
""")


col4, col5, col6 = st.columns(3)


with col4:

    Heart_Disease = st.selectbox(
        "Heart Disease",
        ["No", "Yes"]
    )

    Fatty_Liver = st.selectbox(
        "Fatty Liver",
        ["No", "Yes"]
    )

    PCOS = st.selectbox(
        "PCOS",
        ["No", "Yes"]
    )


with col5:

    Work_Type = st.selectbox(
        "Work Type",
        [
            "Private",
            "Self-employed",
            "Government",
            "Student",
            "Other"
        ]
    )

    Residence_Type = st.selectbox(
        "Residence Type",
        ["Urban", "Rural"]
    )


with col6:

    Daily_Water_Intake_L = st.number_input(
        "Daily Water Intake (L)",
        min_value=0.0,
        max_value=20.0,
        value=2.0
    )

# PREDICTION BUTTON

st.markdown("<br>", unsafe_allow_html=True)


if st.button(
    "🔍 Predict Diabetes Risk",
    use_container_width=True
):

    # CREATE INPUT DATA

    input_data = {

        "Age": Age,

        "Gender": Gender,

        "BMI": BMI,

        "Waist_Circumference_cm":
            Waist_Circumference_cm,

        "Blood_Glucose":
            Blood_Glucose,

        "HbA1c":
            HbA1c,

        "Fasting_Blood_Sugar":
            Fasting_Blood_Sugar,

        "Insulin_Level":
            Insulin_Level,

        "Blood_Pressure_Systolic":
            Blood_Pressure_Systolic,

        "Blood_Pressure_Diastolic":
            Blood_Pressure_Diastolic,

        "Total_Cholesterol":
            Total_Cholesterol,

        "HDL":
            HDL,

        "LDL":
            LDL,

        "Triglycerides":
            Triglycerides,

        "Physical_Activity_Level":
            Physical_Activity_Level,

        "Exercise_Hours_Per_Week":
            Exercise_Hours_Per_Week,

        "Daily_Walking_Minutes":
            Daily_Walking_Minutes,

        "Diet_Quality":
            Diet_Quality,

        "Sugar_Intake_Level":
            Sugar_Intake_Level,

        "Sleep_Hours":
            Sleep_Hours,

        "Stress_Level":
            Stress_Level,

        "Smoking_Status":
            Smoking_Status,

        "Alcohol_Consumption":
            Alcohol_Consumption,

        "Family_History_Diabetes":
            Family_History_Diabetes,

        "Hypertension":
            Hypertension,

        "Heart_Disease":
            Heart_Disease,

        "Fatty_Liver":
            Fatty_Liver,

        "PCOS":
            PCOS,

        "Work_Type":
            Work_Type,

        "Residence_Type":
            Residence_Type,

        "Daily_Water_Intake_L":
            Daily_Water_Intake_L
    }

    # DATAFRAME

    input_df = pd.DataFrame(
        [input_data]
    )


    # ENCODE CATEGORICAL FEATURES

    input_encoded = pd.get_dummies(
        input_df,
        drop_first=True,
        dtype=int
    )


    # MATCH TRAINING FEATURES

    input_encoded = input_encoded.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # MODEL PREDICTION

    prediction = model.predict(
        input_encoded
    )[0]


    # PROBABILITIES

    probabilities = model.predict_proba(
        input_encoded
    )[0]

    class_names = model.classes_

    probability = max(probabilities) * 100


    # RESULT TITLE

    st.html("""
    <div class="section-title">

        <h2>📊 Prediction Result</h2>

    </div>
    """)


    # DISPLAY RISK

    if prediction == "High":

        st.html("""
        <div class="result-card">

            <div class="result-title">
                Predicted Diabetes Risk
            </div>

            <div class="risk-high">
                🔴 HIGH DIABETES RISK
            </div>

        </div>
        """)


    elif prediction == "Moderate":

        st.html("""
        <div class="result-card">

            <div class="result-title">
                Predicted Diabetes Risk
            </div>

            <div class="risk-moderate">
                🟠 MODERATE DIABETES RISK
            </div>

        </div>
        """)


    elif prediction == "Low":

        st.html("""
        <div class="result-card">

            <div class="result-title">
                Predicted Diabetes Risk
            </div>

            <div class="risk-low">
                🟢 LOW DIABETES RISK
            </div>

        </div>
        """)


    else:

        st.html(f"""
        <div class="result-card">

            <div class="result-title">
                Predicted Diabetes Risk
            </div>

            <div class="risk-moderate">
                {prediction}
            </div>

        </div>
        """)

    # MODEL CONFIDENCE

    st.html(f"""
    <div class="confidence-card">

        <div class="confidence-title">
            🤖 Model Confidence
        </div>

        <div class="confidence-value">
            {probability:.2f}%
        </div>

    </div>
    """)

    # PROBABILITY TABLE

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📈 Risk Probability")


    probability_df = pd.DataFrame({

        "Risk Level":
            class_names,

        "Probability (%)":
            probabilities * 100
    })


    probability_df[
        "Probability (%)"
    ] = probability_df[
        "Probability (%)"
    ].round(2)


    st.dataframe(
        probability_df,
        use_container_width=True,
        hide_index=True
    )

    # PROBABILITY CHART

    st.subheader("📊 Probability Distribution")

    chart_df = probability_df.set_index(
        "Risk Level"
    )

    st.bar_chart(
        chart_df["Probability (%)"]
    )

    # PATIENT INFORMATION

    with st.expander(
        "👤 View Patient Information"
    ):

        st.dataframe(
            input_df,
            use_container_width=True,
            hide_index=True
        )

# FOOTER

st.html("""
<div class="footer">

    <p class="warning">
        ⚠️ This prediction is generated by a Machine Learning
        model and should not be considered a medical diagnosis.
    </p>

    <p class="brand">
        🩺 Diabetes Risk Prediction System
    </p>

    <p>
        Built with Python • Streamlit • Machine Learning
    </p>

</div>
""")