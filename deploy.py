import streamlit as st
import warnings
import pickle
warnings.filterwarnings("ignore")

import base64

def set_bg(bg_image):
    with open(bg_image, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("bg.png")

st.set_page_config(
    page_title="Diabetes Predictor",
    layout="wide"
)
model = pickle.load(open("diabetes-predictor.pkl", "rb"))

st.markdown("""
<style>
label {
    color: gray !important;
    font-weight: bold;
    background-color:white;
}

.main-box{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    padding:25px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.25);
}
.stButton>button{

    width:100%;
    height:55px;
    font-size:20px;
    font-weight:bold;

    border-radius:15px;

    background:linear-gradient(90deg,#0B5ED7,#2D9CDB);

    color:white;

    border:none;

    transition:0.3s;
}

.stButton>button:hover{

    transform:scale(1.02);

    background:linear-gradient(90deg,#084298,#0B5ED7);

}



</style>
<h1 style='text-align:center;color:#0B5ED7;'>
🩺 Diabetes Prediction System
</h1>
<h4 style='text-align:center;color:gray;'>
AI-powered Diabetes Risk Assessment
</h4>

""", unsafe_allow_html=True)




left, right = st.columns(2)
with left:
    preg = st.number_input("Number of Pregnancies", min_value=0, value=0)
    gluc = st.number_input("Glucose Level (mg/dL)", value=120)
    bp   = st.number_input("Blood Pressure (mm Hg)", value=70)
    skin = st.number_input("Skin Thickness (mm)", value=20)
with right:    
    ins  = st.number_input("Insulin (µU/mL)", value=80)
    bmi  = st.number_input("Body Mass Index", value=25.0)
    dpf  = st.number_input("Diabetes Pedigree Function", value=0.50)
    age  = st.number_input("Age (Years)", value=30)

if st.button("Predict"):
    out = model.predict([[preg, gluc, bp, skin, ins, bmi, dpf, age]])

    if out[0] == 1:
        st.error("⚠️ Based on the entered information, the model predicts a high likelihood of diabetes. Please consult a healthcare professional.")
    else:
        st.success("✅ Based on the entered information, the model predicts that you are unlikely to have diabetes.")
st.markdown("---")

st.caption(
"⚠️ This application is for educational purposes only and should not be considered medical advice."
)