import streamlit as st
from streamlit.components.v1 import html
import base64

if not st.session_state.get("authenticated", False):
    st.switch_page("login.py")

st.set_page_config(layout="wide", 
                   initial_sidebar_state=None, 
                   page_title="Asset Management", 
                   page_icon=":bar_chart:")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none}
    [data-testid="collapsedControl"] {display: none}
    [data-testid="stHeader"] {
            background-color: rgba(0, 0, 0, 0);}
    </style>

    """, unsafe_allow_html=True)

st.markdown(f"""
    <div style="
        color: black;
        font-size: 30px;
        font-weight: 700;
        margin-bottom : 0px;
        margin-left : 25px">
        ASSET MANAGEMENT
    </div>
    <div style="
        color: #ffbd59;
        font-size: 39px;
        font-weight: 300;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-top : -55px;
        margin-left : 25px">
        _________________
    </div>
    <div style="
        color: black;
        font-size: 18px;
        font-weight: 20;
        margin-top : 0px;
        margin-left : 25px">
        Platform terintegrasi untuk mendukung pengelolaan berbagai program keselamatan di Asset Management. <br> Pilih program yang ingin dikelola dan lakukan submission, pemantauan, serta pelaporan dengan lebih mudah dan efisien.
    </div>
""",unsafe_allow_html=True)

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    div.st-key-open_program button {
        background-color: #0d47a1;
        border-color: white;
        width: 100%;
        justify-content: flex-end;
        align-items: right;
        margin-left: 65px;
    }
    div.st-key-open_program2 button {
        background-color: #0d47a1;
        border-color: white;
        width: 100%;
        margin-left: 65px;
        justify-content: flex-end;
        align-items: right;
    }
    div[data-testid="stButton"] button{
        height:600px;
        width : 600px;
        margin-left: 65px;
        background:transparent;
        border:none;
        margin-top:-8px;
        border-radius:10px;
    }
    </style>
    """,
    unsafe_allow_html=True)
with st.container(width=1700):
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    card_sct = get_base64_image("image/sct.png")
    card_ac = get_base64_image("image/ac.png")
    col1, col2 = st.columns([3, 3], gap="small")
    with col1:
        with st.container():
            st.markdown(f"""
                <div class="stVerticalBlock st-emotion-cache-1n6tfoc e12zf7d53"
                    style="
                    background-image:url('data:image/png;base64,{card_sct}');
                    height: 600px;
                    width: 600px;
                    background-position: bottom;
                    background-repeat: no-repeat;
                    background-size: cover;
                    margin-bottom: -1000px;
                    margin-left: 150px;
                    border-radius: 10px;
                    display: flex;
                    box-shadow: 0 5px 6px rgba(0,0,0.3,0.4);">
                    <div class="overlay">
                        <div style="
                            color: white;
                            font-size: 60px;
                            font-weight: 900;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                            padding-left: 25px;
                            margin-top : 350px; 
                            margin-bottom : -10px;">
                            Safety
                        </div>
                        <div style="
                            color: white;
                            font-size: 60px;
                            font-weight: 900;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                            padding-left: 25px;
                            margin-top : -30px;">
                            Champion Traffic
                        </div>
                        <div style="
                            color: white;
                            font-size: 15px;
                            font-weight: 100;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                            padding-left: 25px;
                            padding-right: 25px;
                            margin-top : -10px;">
                            Program apresiasi bagi driver dan operator yang berprestasi dalam penerapan keselamatan kerja, sekaligus membangun budaya K3 dan meningkatkan rasa kepemilikan terhadap keselamatan.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True) 
            if st.button("", key="sct"):
                st.switch_page("pages/sct.py")               
    with col2:
        with st.container():
            st.markdown(f"""
                <div class="stVerticalBlock st-emotion-cache-wfksaw e12zf7d53"
                    style="
                    background-image:url('data:image/png;base64,{card_ac}');
                    height: 600px;
                    width: 600px;
                    background-position: bottom;
                    background-repeat: no-repeat;
                    background-size: cover;
                    margin-bottom: -1000px;
                    margin-top: -350px;
                    margin-left:65px;
                    border-radius: 10px;
                    box-shadow: 0 5px 6px rgba(0,0,0.3,0.4);">
                    <div class="overlay">
                        <div style="
                            color: white;
                            font-size: 60px;
                            font-weight: 900;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                            padding-left: 25px;
                            padding-right: 25px;
                            margin-top : 350px; 
                            margin-bottom : -10px;">
                            Asset
                        </div>
                        <div style="
                            color: white;
                            font-size: 60px;
                            font-weight: 900;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                            padding-left: 25px;
                            padding-right: 25px;
                            margin-top : -30px;">
                            Campaign
                        </div>
                        <div style="
                            color: white;
                            font-size: 15px;
                            font-weight: 100;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                            padding-left: 25px;
                            padding-right: 25px;
                            margin-top : -10px;">
                            Program kampanye keselamatan yang menggabungkan edukasi, kuis, dan apresiasi bagi peserta terbaik guna mendorong budaya K3 yang lebih aktif.
                    </div>
                </div>
                """, unsafe_allow_html=True) 
            if st.button("", key="ac", use_container_width=True):
                st.switch_page("pages/ac.py")
