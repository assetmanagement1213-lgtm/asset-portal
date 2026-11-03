import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    [data-testid="stHeader"] {
            background-color: rgba(0, 0, 0, 0);}
    .stApp {
            background-color: #0d47a1;
        }
    </style>
    """, unsafe_allow_html=True)

st.write('<div style="color: white; font-size: 20px; text-align: left; padding-bottom: 20px;">' \
         'ASSET MANAGEMENT</div>', unsafe_allow_html=True)

html("""
<!DOCTYPE html>
<html>
    <head>
        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"
            />
        <style>
            body{
                margin:0;
                background:#0d47a1;
            }
            .swiper{
                width:1800px;
                height:700px;
            }
            .swiper-slide{
                background:white;
                display:flex;
                border-radius:10px;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                font-family:Arial;
            }
            .title{
                font-size:30px;
                font-weight:bold;
            }
            .desc{
                color:gray;
                margin-top:10px;
            }
            button{
                margin-top:25px;
                padding:10px 30px;
                border:none;
                border-radius:5px;
                background:#1565c0;
                color:white;
                cursor:pointer;
            }
            .swiper-button-next,
            .swiper-button-prev{
                width:50px;
                height:50px;
                background:white;
            }
        </style>
    </head>
    <body>
        <div class="swiper">
        <div class="swiper-button-prev"></div>
        <div class="swiper-button-next"></div>
            <div class="swiper-wrapper">             
                <div class="swiper-slide">
                    <div class="title">
                        🚦 Safety Champion Traffic
                    </div>

                    <div class="desc">
                        Driver & Operator Assessment
                    </div>
                </div>

                <div class="swiper-slide">
                    <div class="title">
                        🎨 Asset Campaign
                    </div>

                    <div class="desc">
                        Poster & Safety Campaign
                    </div>
                </div>
            </div>
        <div class="swiper-pagination"></div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            new Swiper(".swiper",{
                loop:true,
                navigation:{
                    nextEl:".swiper-button-next",
                    prevEl:".swiper-button-prev"
                },
                pagination:{
                    el:".swiper-pagination",
                    clickable:true
                },
                    autoplay:{
                    delay:2500
                }
            })
        </script>
    </body>
</html>

""",height=700)