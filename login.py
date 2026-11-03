import streamlit as st

st.set_page_config(
    page_title="Asset Safety Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    * {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background-color: #F4F6FA;
    }
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
    .login-box {
        width: 1100px;
        min-height: 520px;
        display: grid;
        grid-template-columns: 35% 65%;
        background: #FFFFFF;
        border: 1px solid #D9DEE7;
    }
    .brand-panel {
        background-color: #0D2C5C;
        padding: 55px 45px;
        display: flex;
        height: 800px;
        flex-direction: column;
        justify-content: space-between;
        color: white;
    }
    .brand-logo {
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .brand-title {
        font-size: 34px;
        line-height: 1.15;
        font-weight: 600;
        margin-top: 120px;
    }
    .brand-description {
        font-size: 12px;
        line-height: 1.7;
        color: #D9E4F5;
        margin-top: 18px;
        max-width: 230px;
    }
    .brand-footer {
        font-size: 10px;
        color: #AFC1DC;
        margin-top: 50px;
    }
    .form-panel {
        padding: 70px 75px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .welcome-title {
        font-size: 28px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }
    .welcome-description {
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 35px;
    }
    div[data-testid="stTextInput"] label {
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }
    div[data-testid="stTextInput"] input {
        height: 45px;
        border: 1px solid #D1D5DB;
        border-radius: 0px;
        background-color: #FFFFFF;
        color: #111827;
        font-size: 13px;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #0D2C5C;
        box-shadow: 0 0 0 1px #0D2C5C;
    }
    div.stButton > button {
        display: flex;
        width: 190px;
        height: 25px;
        border-radius: 10px;
        background-color: #0D2C5C;
        color: white;
        border: 1px solid #0D2C5C;
        font-size: 12px;
        font-weight: 100;
        transition: 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #173B79;
        border-color: #173B79;
        color: white;
    }
    div[data-testid="stAlert"] {
        border-radius: 0px;
        font-size: 12px;
    }
    @media (max-width: 700px) {
        .login-box {
            width: 90%;
            grid-template-columns: 1fr;
        }
        .brand-panel {
            min-height: 250px;
            padding: 35px;
        }
        .brand-title {
            margin-top: 50px;
            font-size: 28px;
        }
        .form-panel {
            padding: 45px 35px;
        }
    }
</style>
""", unsafe_allow_html=True)

def access_page():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    left, right = st.columns([35, 65], gap="small")
    with left:
        st.markdown("""
        <div class="brand-panel">
            <div>
                <div class="brand-logo">
                    ASSET MANAGEMENT
                </div>
                <div class="brand-title">
                    Safety<br>
                    starts<br>
                    with us.
                </div>
                <div class="brand-description">
                    Platform terintegrasi untuk
                    pengelolaan program keselamatan
                    di Asset Management.
                </div>
            </div>
            <div class="brand-footer">
                Asset Management<br>
                OHS Department<br>
                © 2026 All Rights Reserved
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="form-panel">
            <div class="welcome-title">
                Welcome to Asset Management 
            </div>
            <div class="welcome-description">
                Enter your access code to continue.
            </div>
        </div>
        """, unsafe_allow_html=True)

        access_code = st.text_input(
            "Access Code",
            type="password",
            placeholder="Enter access code",
            label_visibility="visible"
        )
        st.write("")
        space, btn = st.columns([2,1])
        with btn :
            enter = st.button(
                "Continue →"
            )
            if enter:
                correct_code = "12132026"

                if access_code == correct_code:

                    st.session_state.authenticated = True
                    st.switch_page("pages/home.py")

                else:

                    st.error(
                        "Invalid access code. Please try again."
                    )

        st.markdown("""
        <div style="
            margin-top: 35px;
            font-size: 10px;
            color: #9CA3AF;
            text-align: center;
        ">
            Authorized personnel only
        </div>
        """, unsafe_allow_html=True)


        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    access_page()
else:
    st.switch_page("pages/home.py")