import streamlit as st
import pickle
import warnings
import base64  


warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="Diabetes Predictor",
    page_icon="🩺",
    layout="centered"
)


def set_bg(bg_image):
    with open(bg_image, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        /* Sets the background image */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Creates a sleek, semi-transparent white card over the background */
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        /* FORCES all text and labels to be dark grey so it's readable on the white card */
        p, h1, h2, h3, h4, h5, h6, label, .stMarkdown {{
            color: #1F2937 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("bg.png")


@st.cache_resource
def load_model():
    with open("diabetes-predictor.pkl", "rb") as file:
        return pickle.load(file)

model = load_model()


st.title("🩺 Diabetes Prediction System")
st.markdown("### AI-powered Diabetes Risk Assessment")
st.markdown("Please enter the patient's medical details below to assess the likelihood of diabetes.")
st.divider()


col1, col2 = st.columns(2)

with col1:
    preg = st.number_input("Number of Pregnancies", min_value=0, max_value=20, value=0, step=1)
    gluc = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=120, step=1)
    bp   = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=70, step=1)
    skin = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20, step=1)

with col2:    
    ins  = st.number_input("Insulin (µU/mL)", min_value=0, max_value=1000, value=80, step=1)
    bmi  = st.number_input("Body Mass Index", min_value=0.0, max_value=70.0, value=25.0, step=0.1)
    dpf  = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.50, step=0.01)
    age  = st.number_input("Age (Years)", min_value=0, max_value=120, value=30, step=1)

st.divider()


if st.button("Predict Risk", type="primary", use_container_width=True):
    input_data = [[preg, gluc, bp, skin, ins, bmi, dpf, age]]
    
    try:
        prediction_proba = model.predict_proba(input_data)
        risk_percentage = prediction_proba[0][1] * 100
        
        if risk_percentage >= 50:
            st.error(f"⚠️ **High Risk Detected ({risk_percentage:.1f}%):** Based on the entered information, the model predicts a high likelihood of diabetes. Please consult a healthcare professional.")
        else:
            st.success(f"✅ **Low Risk ({risk_percentage:.1f}%):** Based on the entered information, the model predicts that you are unlikely to have diabetes.")
            
        st.write("### Risk Level Indicator")
        st.progress(int(risk_percentage))
        
    except AttributeError:
        out = model.predict(input_data)
        if out[0] == 1:
            st.error("⚠️ **High Risk Detected:** Based on the entered information, the model predicts a high likelihood of diabetes.")
        else:
            st.success("✅ **Low Risk:** Based on the entered information, the model predicts that you are unlikely to have diabetes.")


st.markdown("---")
st.caption("⚠️ **Disclaimer:** This application is for educational purposes only and should not be considered medical advice.")