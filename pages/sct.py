import base64

import altair as alt
import pandas as pd
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from utils.sheets import submission_property_damage, submission_pelanggaran, submission_cs, submission_fmt, submission_hrga, submission_jetty, submission_individual
from openpyxl import load_workbook
from pathlib import Path

st.set_page_config(layout="wide", 
                   initial_sidebar_state=None, 
                   page_title="Safety Champion Traffic", 
                   page_icon="🚦")

a,b = st.columns([0.2,3], gap="small")

report_sheets = {
    "Civil Service": "Report_CS",
    "Fleet Management": "Report_FMT",
    "Jetty": "Report_Jetty",
    "HR&GA": "Report_HRGA",
}

import gspread
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)

gc = gspread.authorize(creds)

client = gspread.authorize(creds)
spreadsheet = client.open("SCT Database")
ws_tabelpelanggaran = spreadsheet.worksheet("Dashboard Pelanggaran")
ws_tabelPD = spreadsheet.worksheet("Dashboard Property Damage")
ws_sumPelanggaran = spreadsheet.worksheet("Summary Pelanggaran")
ws_sumPD = spreadsheet.worksheet("Summary Property Damage")
ws_individual = spreadsheet.worksheet("Data Individu")
ws_gallery = spreadsheet.worksheet("Gallery")


@st.cache_data(ttl=60)
def get_report_data(department):

    sheet_name = report_sheets[department]

    sh = gc.open_by_key("19Y5zC5TpPvocxCf6veYGcD3tzfi8rv9c4Njrk_VwBsM")
    ws = sh.worksheet(sheet_name)

    data = ws.get_all_records()

    return pd.DataFrame(data)

with a:
    st.markdown("""
    <style>
    [data-testid="stBaseButton-secondary"] {
        background-color: rgba(0, 0, 0, 0);
        border: none;
        display: flex;
        horizontal-align: center;
        vertical-align: center;
        align-items: center
        font-size: 2rem;
    }
    </style>""", unsafe_allow_html=True)
    if st.button("⮜", key="go_home"):
        st.switch_page("pages/home.py")
with b:
    st.markdown(f"""
    <div style="
        color: #173b79;
        font-size: 50px;
        font-weight: 900;
        margin-left: -40px;">
        Safety Champion Traffic
    </div>""", unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:ital,opsz,wght@0,17..18,400..700;1,17..18,400..700&display=swap');

html, body, [class*="css"] {
    font-family: 'Google Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none}
    [data-testid="collapsedControl"] {display: none}
    [data-testid="stHeader"] {
            background-color: rgba(0, 0, 0, 0);}
    [class="st-emotion-cache-8atqhb ew64v8o0"] {
        width: 250px;
        border-radius: 0px;
    }
    [class="nav nav-pills mb-auto nav-justified"] {
        width: 250px;
        border-radius: 0px;
    }
    </style>""", unsafe_allow_html=True)
# background-color: #173b79
department_team = {
        "Civil Service": [
            "Batching Plant Tim 施工管理部 - 搅拌站",
            "Acytelin Tim 阿赛泰林团队",
            "Civil Tim 民事团队",
            "Stone Crusher Tim 碎石机团队"
        ],
        "Fleet Management": [
            "Karimun Pool 卡里姆恩池",
            "Soligi Pool 索利吉泳池",
            "Dispatch Fleet Management 调度舰队管理",
            "Lifting Pool 举重池"
        ],
        "HR&GA": [
            "GA Transportasi 后勤交通科"
        ],
        "Jetty Operational Center": [
            "Tim Crane Type 塔式起重机类型",
            "Tim Wheel Type 团队轮类型"
        ]
    }

df_pelanggaran = pd.DataFrame(ws_tabelpelanggaran.get_all_records())
df_pd = pd.DataFrame(ws_tabelPD.get_all_records())
df_individu = pd.DataFrame(ws_individual.get_all_records())
df_gallery = pd.DataFrame(ws_gallery.get_all_records())
urutan_bulan = [
    "Januari", "Februari", "Maret", "April",
    "Mei", "Juni", "Juli", "Agustus",
    "September", "Oktober", "November", "Desember"
]
urutan_departemen = [
    "Jetty",
    "Fleet Management",
    "Civil Service",
    "HR&GA", "Total Pelanggaran"]
urutan_departemen_pd = [
    "Jetty",
    "Fleet Management",
    "Civil Service",
    "HR&GA", "Total Property Damage"]

###df_pelanggaran
df_pelanggaran["Bulan"] = pd.Categorical(
    df_pelanggaran["Bulan"],
    categories=urutan_bulan,
    ordered=True)
df_pelanggaran["Pelanggaran"] = pd.to_numeric(
    df_pelanggaran["Pelanggaran"],
    errors="coerce")
df_pivot_pelanggaran = df_pelanggaran.pivot_table(
    index="Departemen",
    columns="Bulan",
    values="Pelanggaran",
    aggfunc="sum",
    observed=False)
df_pivot_pelanggaran = df_pivot_pelanggaran.reindex(columns=urutan_bulan)
df_pivot_pelanggaran = df_pivot_pelanggaran.reindex(urutan_departemen)

##data property damage
df_pd["Bulan"] = pd.Categorical(
    df_pd["Bulan"],
    categories=urutan_bulan,
    ordered=True)
df_pd["Property Damage"] = pd.to_numeric(
    df_pd["Property Damage"],
    errors="coerce")
df_pivot_pd = df_pd.pivot_table(
    index="Departemen",
    columns="Bulan",
    values="Property Damage",
    aggfunc="sum",
    observed=False)
df_pivot_pd = df_pivot_pd.reindex(columns=urutan_bulan)
df_pivot_pd = df_pivot_pd.reindex(urutan_departemen_pd)

tabs = st.tabs(["Dashboard","Report","Gallery", "Submission"])
with tabs[3]:
    st.subheader("New Submission")
    col1, col2 = st.columns([1.3, 6], gap="small")
    with col1:
        submission_selected = option_menu(
                menu_title=None,
                options=["Pelanggaran", "Property Damage", "Analisis Data Pelanggaran", "Analisis Data Property Damage", "Penilaian Individu", "Report Departemen"],
                styles={
                    "icon": {"font-size": "15px"},
                    "font": {"font-size": "15px", "font-weight": "500"},
                    "container": {
                        "margin-bottom": "-80px",
                        "padding-bottom": "-20px",
                        "background-color": "#ffffff",
                        "height": "60vh",
                    },
                    "nav-link": {
                        "font-size": "15px",
                        "font-weight": "500",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {
                        "background-color": "#173b79",
                        "color": "white",
                        "font-weight": "600"
                    }
                }
            )
        if submission_selected == "Report Departemen":
            report_selected = option_menu(
                menu_title=None,
                default_index=0,
                options=[
                    "Civil Service",
                    "Jetty",
                    "Fleet Management",
                    "HRGA"
                ],
                icons=[
                    "chevron-right",
                    "chevron-right",
                    "chevron-right",
                    "chevron-right",
                    "chevron-right",
                    "chevron-right"
                ],
                styles={
                    "icon": {
                        "font-size": "11px"
                    },
                    "container": {
                        "margin-top": "-10px",
                        "margin-left": "25px",
                        "padding": "-10px 0px 0px 15px",
                        "background-color": "#ffffff",
                        "width": "200px",
                    },
                    "nav-link": {
                        "font-size": "13px",
                        "font-weight": "500",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {
                        "background-color": "#173b79",
                        "color": "white",
                        "font-weight": "600"
                    }
                }
            )

    with col2:
        if submission_selected == "Pelanggaran":
            st.subheader("Form Pelanggaran")
            values = {}
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                values["Date"] = st.date_input(
                    "Date *")
                values["Nama Driver/Operator"] = st.text_input(
                    "Nama Driver/Operator *")
                values["NIK"] = st.text_input(
                    "NIK *")
                values["Pelanggaran"] = st.text_area(
                    "Pelanggaran *",
                    height=150)
            with col2:
                values["Departemen"] = st.selectbox(
                    "Departemen *",
                    list(department_team.keys()))
                values["Team Departemen"] = st.selectbox(
                    "Team Departemen *",
                    department_team[values["Departemen"]])
            st.divider()
            col_submit1, col_submit2 = st.columns([5, 1])
            with col_submit2:
                submit = st.button(
                    "Submit",
                    use_container_width=True,
                    type="primary")
            if submit:
                if (
                    values["Nama Driver/Operator"] == ""
                    or values["NIK"] == ""
                    or values["Pelanggaran"] == ""
                ):
                    st.error("Mohon lengkapi seluruh data.")

                else:
                    submission_id = submission_pelanggaran(values)
                    st.success(
                        f"Submission berhasil! ID: {submission_id}"
                    )

        elif submission_selected == "Property Damage":
            st.subheader("Form Property Damage")
            values = {}
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                values["Date"] = st.date_input(
                    "Date *")
                values["Nama Driver/Operator"] = st.text_input(
                    "Nama Driver/Operator *")
                values["NIK"] = st.text_input(
                    "NIK *")
                values["Property Damage"] = st.text_area(
                    "Property Damage *",
                    height=150)
            with col2:
                values["Departemen"] = st.selectbox(
                    "Departemen *",
                    list(department_team.keys()))
                values["Team Departemen"] = st.selectbox(
                    "Team Departemen *",
                    department_team[values["Departemen"]])
            st.divider()
            col_submit1, col_submit2 = st.columns([5, 1])
            with col_submit2:
                submit = st.button(
                    "Submit",
                    use_container_width=True,
                    type="primary")
            if submit:
                if (
                    values["Nama Driver/Operator"] == ""
                    or values["NIK"] == ""
                    or values["Property Damage"] == ""):
                    st.error("Mohon lengkapi seluruh data.")
                else:
                    submission_id = submission_property_damage(values)
                    st.success(
                        f"Submission berhasil! ID: {submission_id}"
                    )

        elif submission_selected == "Penilaian Individu":
                    values = {}
                    values["Periode"] = st.selectbox("Periode *", options=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], width=200)
                    a,b,c = st.columns(3, gap = "small")
                    with a :
                        values ["Nama Driver/Operator"] = st.text_input("Nama Driver/Operator")
                    with b:
                        values["NIK"] = st.text_input("Masukkan NIK Driver/Operator")
                        values["Jabatan"] = st.text_input("Masukkan Jabatan Driver/Operator")
                    with c:
                        values["Departemen"] = st.selectbox(
                            "Departemen *",
                            list(department_team.keys()))
                        values["Team Departemen"] = st.selectbox(
                            "Team Departemen *",
                            department_team[values["Departemen"]])
                    st.divider()
                    col_submit1, col_submit2 = st.columns([5, 1])
                    with col_submit2:
                        submit = st.button(
                            "Submit",
                            use_container_width=True,
                            type="primary")
                    if submit:
                        if (
                            values["Periode"] == ""
                            or values["Nama Driver/Operator"] == ""
                            or values["NIK"] == ""
                            or values["Departemen"] == ""):
                            st.error("Mohon lengkapi seluruh data.")
                        else:
                            submission_id = submission_individual(values)
                            st.success(
                                f"Submission berhasil! ID: {submission_id}"
                            )

        
        elif submission_selected == "Analisis Data Pelanggaran":
                    st.subheader("Data Pelanggaran")
                    st.dataframe(df_pivot_pelanggaran, width="stretch")
                    st.subheader("Interpretasi Data Pelanggaran")
                    bulan_selected = st.selectbox("Bulan", options=urutan_bulan, key="bulan_pelanggaran", width=200)
                    df_filtered = df_pelanggaran[df_pelanggaran["Bulan"] == bulan_selected]
                    with st.expander("Departemen Jetty"):
                        df_jetty = df_filtered[df_filtered["Departemen"] == "Jetty"]
                        if not df_jetty.empty:
                            data_jetty = df_jetty.iloc[0]

                            jetty_tren_default = data_jetty["Tren Keseluruhan"]
                            jetty_risiko_default = data_jetty["Status Risiko"]
                            jetty_analisis_default = data_jetty["Analisis"]

                            jetty_tren_default = (
                                "" if pd.isna(jetty_tren_default) else str(jetty_tren_default)
                            )
                            jetty_risiko_default = (
                                "" if pd.isna(jetty_risiko_default) else str(jetty_risiko_default)
                            )
                            jetty_analisis_default = (
                                "" if pd.isna(jetty_analisis_default) else str(jetty_analisis_default)
                            )
                        else:
                            jetty_tren_default = ""
                            jetty_risiko_default = ""
                            jetty_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            jetty_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=jetty_tren_default,
                                key=f"tren_jetty_{bulan_selected}",
                                height=120
                            )
                        with b:
                            jetty_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=jetty_risiko_default,
                                key=f"risiko_jetty_{bulan_selected}",
                                height=120
                            )
                        with c:
                            jetty_analisis_input = st.text_area(
                                "**Analisis**",
                                value=jetty_analisis_default,
                                key=f"analisis_jetty_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_jetty_{bulan_selected}"):
                            records = ws_tabelpelanggaran.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Jetty"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelpelanggaran.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        jetty_risiko_input,
                                        jetty_tren_input,
                                        jetty_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Departemen Fleet Management"):
                        df_fmt = df_filtered[df_filtered["Departemen"] == "Fleet Management"]
                        if not df_fmt.empty:
                            data_fmt = df_fmt.iloc[0]

                            fmt_tren_default = data_fmt["Tren Keseluruhan"]
                            fmt_risiko_default = data_fmt["Status Risiko"]
                            fmt_analisis_default = data_fmt["Analisis"]

                            fmt_tren_default = (
                                "" if pd.isna(fmt_tren_default) else str(fmt_tren_default)
                            )
                            fmt_risiko_default = (
                                "" if pd.isna(fmt_risiko_default) else str(fmt_risiko_default)
                            )
                            fmt_analisis_default = (
                                "" if pd.isna(fmt_analisis_default) else str(fmt_analisis_default)
                            )
                        else:
                            fmt_tren_default = ""
                            fmt_risiko_default = ""
                            fmt_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            fmt_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=fmt_tren_default,
                                key=f"tren_fmt_{bulan_selected}",
                                height=120
                            )
                        with b:
                            fmt_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=fmt_risiko_default,
                                key=f"risiko_fmt_{bulan_selected}",
                                height=120
                            )
                        with c:
                            fmt_analisis_input = st.text_area(
                                "**Analisis**",
                                value=fmt_analisis_default,
                                key=f"analisis_fmt_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_fmt_{bulan_selected}"):
                            records = ws_tabelpelanggaran.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Fleet Management"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelpelanggaran.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        fmt_risiko_input,
                                        fmt_tren_input,
                                        fmt_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Departemen Civil Service"):
                        df_cs = df_filtered[df_filtered["Departemen"] == "Civil Service"]
                        if not df_cs.empty:
                            data_cs = df_cs.iloc[0]

                            cs_tren_default = data_cs["Tren Keseluruhan"]
                            cs_risiko_default = data_cs["Status Risiko"]
                            cs_analisis_default = data_cs["Analisis"]

                            cs_tren_default = (
                                "" if pd.isna(cs_tren_default) else str(cs_tren_default)
                            )
                            cs_risiko_default = (
                                "" if pd.isna(cs_risiko_default) else str(cs_risiko_default)
                            )
                            cs_analisis_default = (
                                "" if pd.isna(cs_analisis_default) else str(cs_analisis_default)
                            )
                        else:
                            cs_tren_default = ""
                            cs_risiko_default = ""
                            cs_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            cs_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=cs_tren_default,
                                key=f"tren_cs_{bulan_selected}",
                                height=120
                            )
                        with b:
                            cs_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=cs_risiko_default,
                                key=f"risiko_cs_{bulan_selected}",
                                height=120
                            )
                        with c:
                            cs_analisis_input = st.text_area(
                                "**Analisis**",
                                value=cs_analisis_default,
                                key=f"analisis_cs_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_cs_{bulan_selected}"):
                            records = ws_tabelpelanggaran.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Civil Service"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelpelanggaran.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        cs_risiko_input,
                                        cs_tren_input,
                                        cs_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Departemen HR&GA"):
                        df_hrga = df_filtered[df_filtered["Departemen"] == "HR&GA"]
                        if not df_hrga.empty:
                            data_hrga = df_hrga.iloc[0]

                            hrga_tren_default = data_hrga["Tren Keseluruhan"]
                            hrga_risiko_default = data_hrga["Status Risiko"]
                            hrga_analisis_default = data_hrga["Analisis"]

                            hrga_tren_default = (
                                "" if pd.isna(hrga_tren_default) else str(hrga_tren_default)
                            )
                            hrga_risiko_default = (
                                "" if pd.isna(hrga_risiko_default) else str(hrga_risiko_default)
                            )
                            hrga_analisis_default = (
                                "" if pd.isna(hrga_analisis_default) else str(hrga_analisis_default)
                            )
                        else:
                            hrga_tren_default = ""
                            hrga_risiko_default = ""
                            hrga_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            hrga_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=hrga_tren_default,
                                key=f"tren_hrga_{bulan_selected}",
                                height=120
                            )
                        with b:
                            hrga_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=hrga_risiko_default,
                                key=f"risiko_hrga_{bulan_selected}",
                                height=120
                            )
                        with c:
                            hrga_analisis_input = st.text_area(
                                "**Analisis**",
                                value=hrga_analisis_default,
                                key=f"analisis_hrga_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_hrga_{bulan_selected}"):
                            records = ws_tabelpelanggaran.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "HR&GA"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelpelanggaran.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        hrga_risiko_input,
                                        hrga_tren_input,
                                        hrga_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Total Pelanggaran"):
                        df_total_pelanggaran = df_filtered[df_filtered["Departemen"] == "Total Pelanggaran"]
                        if not df_total_pelanggaran.empty:
                            data_total_pelanggaran = df_total_pelanggaran.iloc[0]

                            pelanggaran_tren_default = data_total_pelanggaran["Tren Keseluruhan"]
                            pelanggaran_risiko_default = data_total_pelanggaran["Status Risiko"]
                            pelanggaran_analisis_default = data_total_pelanggaran["Analisis"]

                            pelanggaran_tren_default = (
                                "" if pd.isna(pelanggaran_tren_default) else str(pelanggaran_tren_default)
                            )
                            pelanggaran_risiko_default = (
                                "" if pd.isna(pelanggaran_risiko_default) else str(pelanggaran_risiko_default)
                            )
                            pelanggaran_analisis_default = (
                                "" if pd.isna(pelanggaran_analisis_default) else str(pelanggaran_analisis_default)
                            )
                        else:
                            pelanggaran_tren_default = ""
                            pelanggaran_risiko_default = ""
                            pelanggaran_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            pelanggaran_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=pelanggaran_tren_default,
                                key=f"tren_pelanggaran_{bulan_selected}",
                                height=120
                            )
                        with b:
                            pelanggaran_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=pelanggaran_risiko_default,
                                key=f"risiko_pelanggaran_{bulan_selected}",
                                height=120
                            )
                        with c:
                            pelanggaran_analisis_input = st.text_area(
                                "**Analisis**",
                                value=pelanggaran_analisis_default,
                                key=f"analisis_pelanggaran_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_pelanggaran_{bulan_selected}"):
                            records = ws_tabelpelanggaran.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Total Pelanggaran"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelpelanggaran.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        pelanggaran_risiko_input,
                                        pelanggaran_tren_input,
                                        pelanggaran_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
        
        elif submission_selected == "Analisis Data Property Damage":
                    st.subheader("Data Property Damage")
                    st.dataframe(df_pivot_pd, width="stretch")
                    st.subheader("Interpretasi Data Property Damage")
                    bulan_selected = st.selectbox("Bulan", options=urutan_bulan, key="bulan_pd", width=200)
                    df_filtered_pd = df_pd[df_pd["Bulan"] == bulan_selected]
                    with st.expander("Departemen Jetty"):
                        df_pd_jetty = df_filtered_pd[df_filtered_pd["Departemen"] == "Jetty"]
                        if not df_pd_jetty.empty:
                            data_pd_jetty = df_pd_jetty.iloc[0]

                            pd_jetty_tren_default = data_pd_jetty["Tren Keseluruhan"]
                            pd_jetty_risiko_default = data_pd_jetty["Status Risiko"]
                            pd_jetty_analisis_default = data_pd_jetty["Analisis"]

                            pd_jetty_tren_default = (
                                "" if pd.isna(pd_jetty_tren_default) else str(pd_jetty_tren_default)
                            )
                            pd_jetty_risiko_default = (
                                "" if pd.isna(pd_jetty_risiko_default) else str(pd_jetty_risiko_default)
                            )
                            pd_jetty_analisis_default = (
                                "" if pd.isna(pd_jetty_analisis_default) else str(pd_jetty_analisis_default)
                            )
                        else:
                            pd_jetty_tren_default = ""
                            pd_jetty_risiko_default = ""
                            pd_jetty_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            pd_jetty_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=pd_jetty_tren_default,
                                key=f"pd_tren_jetty_{bulan_selected}",
                                height=120
                            )
                        with b:
                            pd_jetty_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=pd_jetty_risiko_default,
                                key=f"pd_risiko_jetty_{bulan_selected}",
                                height=120
                            )
                        with c:
                            pd_jetty_analisis_input = st.text_area(
                                "**Analisis**",
                                value=pd_jetty_analisis_default,
                                key=f"pd_analisis_jetty_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_pd_jetty_{bulan_selected}"):
                            records = ws_tabelPD.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Jetty"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelPD.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        pd_jetty_risiko_input,
                                        pd_jetty_tren_input,
                                        pd_jetty_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Departemen Fleet Management"):
                        df_pd_fmt = df_filtered_pd[df_filtered_pd["Departemen"] == "Fleet Management"]
                        if not df_pd_fmt.empty:
                            data_pd_fmt = df_pd_fmt.iloc[0]

                            pd_fmt_tren_default = data_pd_fmt["Tren Keseluruhan"]
                            pd_fmt_risiko_default = data_pd_fmt["Status Risiko"]
                            pd_fmt_analisis_default = data_pd_fmt["Analisis"]

                            pd_fmt_tren_default = (
                                "" if pd.isna(pd_fmt_tren_default) else str(pd_fmt_tren_default)
                            )
                            pd_fmt_risiko_default = (
                                "" if pd.isna(pd_fmt_risiko_default) else str(pd_fmt_risiko_default)
                            )
                            pd_fmt_analisis_default = (
                                "" if pd.isna(pd_fmt_analisis_default) else str(pd_fmt_analisis_default)
                            )
                        else:
                            pd_fmt_tren_default = ""
                            pd_fmt_risiko_default = ""
                            pd_fmt_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            pd_fmt_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=pd_fmt_tren_default,
                                key=f"pd_tren_fmt_{bulan_selected}",
                                height=120
                            )
                        with b:
                            pd_fmt_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=pd_fmt_risiko_default,
                                key=f"pd_risiko_fmt_{bulan_selected}",
                                height=120
                            )
                        with c:
                            pd_fmt_analisis_input = st.text_area(
                                "**Analisis**",
                                value=pd_fmt_analisis_default,
                                key=f"pd_analisis_fmt_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_pd_fmt_{bulan_selected}"):
                            records = ws_tabelPD.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Fleet Management"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelPD.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        pd_fmt_risiko_input,
                                        pd_fmt_tren_input,
                                        pd_fmt_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Departemen Civil Service"):
                        df_pd_cs = df_filtered_pd[df_filtered_pd["Departemen"] == "Civil Service"]
                        if not df_pd_cs.empty:
                            data_pd_cs = df_pd_cs.iloc[0]

                            pd_cs_tren_default = data_pd_cs["Tren Keseluruhan"]
                            pd_cs_risiko_default = data_pd_cs["Status Risiko"]
                            pd_cs_analisis_default = data_pd_cs["Analisis"]

                            pd_cs_tren_default = (
                                "" if pd.isna(pd_cs_tren_default) else str(pd_cs_tren_default)
                            )
                            pd_cs_risiko_default = (
                                "" if pd.isna(pd_cs_risiko_default) else str(pd_cs_risiko_default)
                            )
                            pd_cs_analisis_default = (
                                "" if pd.isna(pd_cs_analisis_default) else str(pd_cs_analisis_default)
                            )
                        else:
                            pd_cs_tren_default = ""
                            pd_cs_risiko_default = ""
                            pd_cs_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            pd_cs_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=pd_cs_tren_default,
                                key=f"tren_pd_cs_{bulan_selected}",
                                height=120
                            )
                        with b:
                            pd_cs_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=pd_cs_risiko_default,
                                key=f"risiko_pd_cs_{bulan_selected}",
                                height=120
                            )
                        with c:
                            pd_cs_analisis_input = st.text_area(
                                "**Analisis**",
                                value=pd_cs_analisis_default,
                                key=f"analisis_pd_cs_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_pd_cs_{bulan_selected}"):
                            records = ws_tabelPD.get_all_records()
                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Civil Service"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelPD.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        pd_cs_risiko_input,
                                        pd_cs_tren_input,
                                        pd_cs_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Departemen HR&GA"):
                        df_pd_hrga = df_filtered_pd[df_filtered_pd["Departemen"] == "HR&GA"]
                        if not df_pd_hrga.empty:
                            data_pd_hrga = df_pd_hrga.iloc[0]

                            pd_hrga_tren_default = data_pd_hrga["Tren Keseluruhan"]
                            pd_hrga_risiko_default = data_pd_hrga["Status Risiko"]
                            pd_hrga_analisis_default = data_pd_hrga["Analisis"]

                            pd_hrga_tren_default = (
                                "" if pd.isna(pd_hrga_tren_default) else str(pd_hrga_tren_default)
                            )
                            pd_hrga_risiko_default = (
                                "" if pd.isna(pd_hrga_risiko_default) else str(pd_hrga_risiko_default)
                            )
                            pd_hrga_analisis_default = (
                                "" if pd.isna(pd_hrga_analisis_default) else str(pd_hrga_analisis_default)
                            )
                        else:
                            pd_hrga_tren_default = ""
                            pd_hrga_risiko_default = ""
                            pd_hrga_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            pd_hrga_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=pd_hrga_tren_default,
                                key=f"tren_pd_hrga_{bulan_selected}",
                                height=120
                            )
                        with b:
                            pd_hrga_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=pd_hrga_risiko_default,
                                key=f"risiko_pd_hrga_{bulan_selected}",
                                height=120
                            )
                        with c:
                            pd_hrga_analisis_input = st.text_area(
                                "**Analisis**",
                                value=pd_hrga_analisis_default,
                                key=f"analisis_pd_hrga_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_pd_hrga_{bulan_selected}"):
                            records = ws_tabelPD.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "HR&GA"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelPD.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        pd_hrga_risiko_input,
                                        pd_hrga_tren_input,
                                        pd_hrga_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
                    with st.expander("Total Property Damage"):
                        df_total_pd = df_filtered_pd[df_filtered_pd["Departemen"] == "Total Property Damage"]
                        if not df_total_pd.empty:
                            data_total_pd = df_total_pd.iloc[0]

                            pd_tren_default = data_total_pd["Tren Keseluruhan"]
                            pd_risiko_default = data_total_pd["Status Risiko"]
                            pd_analisis_default = data_total_pd["Analisis"]

                            pd_tren_default = (
                                "" if pd.isna(pd_tren_default) else str(pd_tren_default)
                            )
                            pd_risiko_default = (
                                "" if pd.isna(pd_risiko_default) else str(pd_risiko_default)
                            )
                            pd_analisis_default = (
                                "" if pd.isna(pd_analisis_default) else str(pd_analisis_default)
                            )
                        else:
                            pd_tren_default = ""
                            pd_risiko_default = ""
                            pd_analisis_default = ""
                        a, b, c = st.columns([2,1,4], gap="small")
                        with a:
                            pd_tren_input = st.text_area(
                                "**Tren Keseluruhan**",
                                value=pd_tren_default,
                                key=f"tren_pd_{bulan_selected}",
                                height=120
                            )
                        with b:
                            pd_risiko_input = st.text_area(
                                "**Status Risiko**",
                                value=pd_risiko_default,
                                key=f"risiko_pd_{bulan_selected}",
                                height=120
                            )
                        with c:
                            pd_analisis_input = st.text_area(
                                "**Analisis**",
                                value=pd_analisis_default,
                                key=f"analisis_pd_{bulan_selected}",
                                height=120
                            )
                        if st.button("Update", key=f"btn_pd_{bulan_selected}"):
                            records = ws_tabelPD.get_all_records()

                            row_number = next(
                                (
                                    i + 2
                                    for i, row in enumerate(records)
                                    if row["Departemen"] == "Total Property Damage"
                                    and row["Bulan"] == bulan_selected
                                ),
                                None
                            )
                            if row_number is None:
                                st.error("Data departemen dan bulan tidak ditemukan.")
                            else:
                                ws_tabelPD.update(
                                    range_name=f"D{row_number}:F{row_number}",
                                    values=[[
                                        pd_risiko_input,
                                        pd_tren_input,
                                        pd_analisis_input
                                    ]]
                                )

                                st.success("Interpretasi berhasil diperbarui!")
        

        else:
            if report_selected == "Civil Service":
                st.subheader("Form Report Departemen Civil Service")
                values = {}
                values["Periode"] = st.selectbox(
                        "Periode *", options=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], width=200)
                col1, col1a, col2, col3 = st.columns(4, gap="medium")
                with col1:
                    st.subheader("Manpower")
                    values["Total Driver Mixer Truck"] = st.number_input(
                        "Total Driver Mixer Truck *",
                        min_value=0,
                        step=1)
                    values["Total Driver Dump Truck"] = st.number_input(
                        "Total Driver Dump Truck *",
                        min_value=0,
                        step=1)
                    values["Total Driver Light Truck"] = st.number_input(
                        "Total Driver Light Truck *",
                        min_value=0,
                        step=1)
                    values["Total Operator Wheel Loader"] = st.number_input(
                        "Total Operator Wheel Loader *",
                        min_value=0,
                        step=1)
                    values["Total Operator Excavator"] = st.number_input(
                        "Total Operator Excavator *",
                        min_value=0,
                        step=1)
                    values["Total Operator Forklift"] = st.number_input(
                        "Total Operator Forklift *",
                        min_value=0,
                        step=1)
                    values["Total Operator Concrete Pump"] = st.number_input(
                        "Total Operator Concrete Pump *",
                        min_value=0,
                        step=1)
                with col1a:
                    st.subheader(" ")
                    values["Manpower Batching Plant Tim"] = st.number_input(
                        "Manpower Baching Plant Tim *",
                        min_value=0,
                        step=1)
                    values["Manpower Acytelin Tim"] = st.number_input(
                        "Manpower Acytelin Tim *",
                        min_value=0,
                        step=1)
                    values["Manpower Civil Tim"] = st.number_input(
                        "Manpower Civil Tim *",
                        min_value=0,
                        step=1)
                    values["Manpower Stone Crusher Tim"] = st.number_input(
                        "Manpower Stone Crusher Tim *",
                        min_value=0,
                        step=1)
                with col2:
                    st.subheader("Training Preventif")
                    values["Training Batching Plant Tim"] = st.number_input(
                        "Training Batching Plant Tim *",
                        min_value=0,
                        step=1)
                    values["Training Acytelin Tim"] = st.number_input(
                        "Training Acytelin Tim *",
                        min_value=0,
                        step=1)
                    values["Training Civil Tim"] = st.number_input(
                        "Training Civil Tim *",
                        min_value=0,
                        step=1)
                    values["Training Stone Crusher Tim"] = st.number_input(
                        "Training Stone Crusher Tim *",
                        min_value=0,
                        step=1)
                with col3:
                    st.subheader("Kepatuhan Prosedur")
                    values["P2H Batching Plant Tim"] = st.number_input(
                        "P2H Batching Plant Tim *",
                        min_value=0,
                        step=1)
                    values["P2H Acytelin Tim"] = st.number_input(
                        "P2H Acytelin Tim *",
                        min_value=0,
                        step=1)
                    values["P2H Civil Tim"] = st.number_input(
                        "P2H Civil Tim *",
                        min_value=0,
                        step=1)
                    values["P2H Stone Crusher Tim"] = st.number_input(
                        "P2H Stone Crusher Tim *",
                        min_value=0,
                        step=1)
                st.divider()
                col_submit1, col_submit2 = st.columns([5, 1])
                with col_submit2:
                    submit = st.button(
                        "Submit",
                        use_container_width=True,
                        type="primary")
                if submit:
                    if (
                        values["Periode"] == ""
                        or values["Total Driver Mixer Truck"] == ""
                        or values["Total Driver Dump Truck"] == ""
                        or values["Total Driver Light Truck"] == ""
                        or values["Total Operator Wheel Loader"] == ""
                        or values["Total Operator Excavator"] == ""
                        or values["Total Operator Forklift"] == ""
                        or values["Total Operator Concrete Pump"] == ""
                        or values["Manpower Batching Plant Tim"] == ""
                        or values["Manpower Acytelin Tim"] == ""
                        or values["Manpower Civil Tim"] == ""
                        or values["Manpower Stone Crusher Tim"] == ""
                        or values["Training Batching Plant Tim"] == ""
                        or values["Training Acytelin Tim"] == ""
                        or values["Training Civil Tim"] == ""
                        or values["Training Stone Crusher Tim"] == ""
                        or values["P2H Batching Plant Tim"] == ""
                        or values["P2H Acytelin Tim"] == ""
                        or values["P2H Civil Tim"] == ""
                        or values["P2H Stone Crusher Tim"] == ""
                        ):
                        st.error("Mohon lengkapi seluruh data.")
                    else:
                        submission_id = submission_cs(values)
                        st.success(
                            f"Submission berhasil! ID: {submission_id}"
                        )
            elif report_selected == "Jetty":
                st.subheader("Form Report Departemen Jetty")
                values = {}
                values["Periode"] = st.selectbox(
                        "Periode *", options=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], width=200)
                col1, col1a, col2, col3 = st.columns(4, gap="medium")
                with col1:
                    st.subheader("Manpower")
                    values["Total Driver Trailer"] = st.number_input(
                        "Total Driver Trailer *",
                        min_value=0,
                        step=1)
                    values["Total Operator Wheel Loader"] = st.number_input(
                        "Total Operator Wheel Loader *",
                        min_value=0,
                        step=1)
                    values["Total Operator Mobile Crane"] = st.number_input(
                        "Total Operator Mobile Crane *",
                        min_value=0,
                        step=1)
                    values["Total Operator Crawler Crane"] = st.number_input(
                        "Total Operator Crawler Crane *",
                        min_value=0,
                        step=1)
                    values["Total Rigger Darat"] = st.number_input(
                        "Total Rigger Darat *",
                        min_value=0,
                        step=1)
                    values["Total Rigger Laut"] = st.number_input(
                        "Total Rigger Laut *",
                        min_value=0,
                        step=1)
                    values["Total Operator Forklift"] = st.number_input(
                        "Total Operator Forklift *",
                        min_value=0,
                        step=1)
                    values["Total Operator Ponton Crane"] = st.number_input(
                        "Total Operator Ponton Crane *",
                        min_value=0,
                        step=1)
                    values["Total Operator Crane Truck"] = st.number_input(
                        "Total Operator Crane Truck *",
                        min_value=0,
                        step=1)
                    values["Total Operator Vacuum Truck"] = st.number_input(
                        "Total Operator Vacuum Truck *",
                        min_value=0,
                        step=1)
                    values["Total Operator Reach Stacker"] = st.number_input(
                        "Total Operator Reach Stacker *",
                        min_value=0,
                        step=1)
                    values["Total Driver Light Truck"] = st.number_input(
                        "Total Driver Light Truck *",
                        min_value=0,
                        step=1)
                    values["Total Operator Ship Unloader"] = st.number_input(
                        "Total Operator Ship Unloader *",
                        min_value=0,
                        step=1)
                with col1a:
                    st.subheader(" ")
                    values["Manpower Tim Crane Type"] = st.number_input(
                        "Manpower Tim Crane Type *",
                        min_value=0,
                        step=1)
                    values["Manpower Tim Wheel Type"] = st.number_input(
                        "Manpower Tim Wheel Type *",
                        min_value=0,
                        step=1)
                with col2:
                    st.subheader("Training Preventif")
                    values["Training Tim Crane Type"] = st.number_input(
                        "Training Tim Crane Type *",
                        min_value=0,
                        step=1)
                    values["Training Tim Wheel Type"] = st.number_input(
                        "Training Tim Wheel Type *",
                        min_value=0,
                        step=1)
                with col3:
                    st.subheader("Kepatuhan Prosedur")
                    values["P2H Tim Crane Type"] = st.number_input(
                        "P2H Tim Crane Type *",
                        min_value=0,
                        step=1)
                    values["P2H Tim Wheel Type"] = st.number_input(
                        "P2H Tim Wheel Type *",
                        min_value=0,
                        step=1)
                st.divider()
                col_submit1, col_submit2 = st.columns([5, 1])
                with col_submit2:
                    submit = st.button(
                        "Submit",
                        use_container_width=True,
                        type="primary")
                if submit:
                    if (
                        values["Periode"] == ""
                        or values["Total Driver Trailer"] == ""
                        or values["Total Operator Wheel Loader"] == ""
                        or values["Total Operator Mobile Crane"] == ""
                        or values["Total Operator Crawler Crane"] == ""
                        or values["Total Rigger Darat"] == ""
                        or values["Total Rigger Laut"] == ""
                        or values["Total Operator Forklift"] == ""
                        or values["Total Operator Ponton Crane"] == ""
                        or values["Total Operator Crane Truck"] == ""
                        or values["Total Operator Vacuum Truck"] == ""
                        or values["Total Operator Reach Stacker"] == ""
                        or values["Total Driver Light Truck"] == ""
                        or values["Total Operator Ship Unloader"] == ""
                        or values["Manpower Tim Crane Type"] == ""
                        or values["Manpower Tim Wheel Type"] == ""
                        or values["Training Tim Crane Type"] == ""
                        or values["Training Tim Wheel Type"] == ""
                        or values["P2H Tim Crane Type"] == ""
                        or values["P2H Tim Wheel Type"] == ""
                        ):
                        st.error("Mohon lengkapi seluruh data.")
                    else:
                        submission_id = submission_jetty(values)
                        st.success(
                            f"Submission berhasil! ID: {submission_id}" )
                                   
            elif report_selected == "Fleet Management":
                st.subheader("Form Report Departemen Fleet Management")
                values = {}
                values["Periode"] = st.selectbox(
                        "Periode *", options=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], width=200)
                col1, col1a, col2, col3 = st.columns(4, gap="medium")
                with col1:
                    st.subheader("Manpower")
                    values["Total Driver Dump Truck"] = st.number_input(
                        "Total Driver Dump Truck *",
                        min_value=0,
                        step=1)
                    values["Total Operator Excavator"] = st.number_input(
                        "Total Operator Excavator *",
                        min_value=0,
                        step=1)
                    values["Total Operator Bulldozer"] = st.number_input(
                        "Total Operator Bulldozer *",
                        min_value=0,
                        step=1)
                    values["Total Operator Compactor"] = st.number_input(
                        "Total Operator Compactor *",
                        min_value=0,
                        step=1)
                    values["Total Operator Motor Grader"] = st.number_input(
                        "Total Operator Motor Grader *",
                        min_value=0,
                        step=1)
                    values["Total Driver Light Truck"] = st.number_input(
                        "Total Driver Light Truck *",
                        min_value=0,
                        step=1)
                    values["Total Operator Mobile Crane"] = st.number_input(
                        "Total Operator Mobile Crane *",
                        min_value=0,
                        step=1)
                    values["Total Rigger"] = st.number_input(
                        "Total Rigger *",
                        min_value=0,
                        step=1)
                with col1a:
                    st.subheader("  ")
                    values["Manpower Karimun Pool"] = st.number_input(
                        "Manpower Karimun Pool *",
                        min_value=0,
                        step=1)
                    values["Manpower Soligi Pool"] = st.number_input(
                        "Manpower Soligi Pool *",
                        min_value=0,
                        step=1)
                    values["Manpower Dispatch Fleet Management"] = st.number_input(
                        "Manpower Dispatch Fleet Management *",
                        min_value=0,
                        step=1)
                    values["Manpower Lifting Pool"] = st.number_input(
                        "Manpower Lifting Pool *",
                        min_value=0,
                        step=1)
                with col2:
                    st.subheader("Training Preventif")
                    values["Training Karimun Pool"] = st.number_input(
                        "Training Karimun Pool *",
                        min_value=0,
                        step=1)
                    values["Training Soligi Pool"] = st.number_input(
                        "Training Soligi Pool *",
                        min_value=0,
                        step=1)
                    values["Training Dispatch Fleet Management"] = st.number_input(
                        "Training Dispatch Fleet Management *",
                        min_value=0,
                        step=1)
                    values["Training Lifting Pool"] = st.number_input(
                        "Training Lifting Pool *",
                        min_value=0,
                        step=1)
                with col3:
                    st.subheader("Kepatuhan Prosedural")
                    values["P2H Karimun Pool"] = st.number_input(
                        "P2H Karimun Pool *",
                        min_value=0,
                        step=1)
                    values["P2H Soligi Pool"] = st.number_input(
                        "P2H Soligi Pool *",
                        min_value=0,
                        step=1)
                    values["P2H Dispatch Fleet Management"] = st.number_input(
                        "P2H Dispatch Fleet Management *",
                        min_value=0,
                        step=1)
                    values["P2H Lifting Pool"] = st.number_input(
                        "P2H Lifting Pool *",
                        min_value=0,
                        step=1)

                st.divider()
                col_submit1, col_submit2 = st.columns([5, 1])
                with col_submit2:
                    submit = st.button(
                        "Submit",
                        use_container_width=True,
                        type="primary")
                if submit:
                    if (
                        values["Periode"] == ""
                        or values["Total Driver Dump Truck"] == ""
                        or values["Total Operator Excavator"] == ""
                        or values["Total Operator Bulldozer"] == ""
                        or values["Total Operator Compactor"] == ""
                        or values["Total Operator Motor Grader"] == ""
                        or values["Total Driver Light Truck"] == ""
                        or values["Total Operator Mobile Crane"] ==""
                        or values["Total Rigger"] == ""
                        or values["Manpower Karimun Pool"] == ""
                        or values["Manpower Soligi Pool"] == ""
                        or values["Manpower Dispatch Fleet Management"] == ""
                        or values["Manpower Lifting Pool"] == ""
                        or values["Training Karimun Pool"] == ""
                        or values["Training Soligi Pool"] == ""
                        or values["Training Dispatch Fleet Management"] == ""
                        or values["Training Lifting Pool"] == ""
                        or values["P2H Karimun Pool"] == ""
                        or values["P2H Soligi Pool"] == ""
                        or values["P2H Dispatch Fleet Management"] == ""
                        or values["P2H Lifting Pool"] == ""
                        ):
                        st.error("Mohon lengkapi seluruh data.")
                    else:
                        submission_id = submission_fmt(values)
                        st.success(
                            f"Submission berhasil! ID: {submission_id}" )
            else:
                st.subheader("Form Report Departemen HR&GA")
                values = {}
                values["Periode"] = st.selectbox(
                        "Periode *", options=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], width=200)
                col1, col1a, col2, col3 = st.columns(4, gap="medium")
                with col1:
                    st.subheader("Manpower")
                    values["Total Driver Bus"] = st.number_input(
                        "Total Driver Bus *",
                        min_value=0,
                        step=1)
                    values["Total Driver Manhaul"] = st.number_input(
                        "Total Driver Manhaul *",
                        min_value=0,
                        step=1)
                with col1a:
                    st.subheader(" ")
                    values["Manpower GA Transportasi"] = st.number_input(
                        "Manpower GA Transportasi *",
                        min_value=0,
                        step=1)
                with col2:
                    st.subheader("Training Preventif")
                    values["Training GA Transportasi"] = st.number_input(
                        "Training GA Transportasi *",
                        min_value=0,
                        step=1)
                with col3:
                    st.subheader("Kepatuhan Prosedur")
                    values["P2H GA Transportasi"] = st.number_input(
                        "P2H GA Transportasi *",
                        min_value=0,
                        step=1)
                st.divider()
                col_submit1, col_submit2 = st.columns([5, 1])
                with col_submit2:
                    submit = st.button(
                        "Submit",
                        use_container_width=True,
                        type="primary")
                if submit:
                    if (
                        values["Periode"] == ""
                        or values["Total Driver Bus"] == ""
                        or values["Total Driver Manhaul"] == ""
                        or values["Manpower GA Transportasi"] == ""
                        or values["Training GA Transportasi"] == ""
                        or values["P2H GA Transportasi"] == ""
                        ):
                        st.error("Mohon lengkapi seluruh data.")
                    else:
                        submission_id = submission_hrga(values)
                        st.success(
                            f"Submission berhasil! ID: {submission_id}" )

with tabs[1]:
    col1, col2 = st.columns([1.3, 6], gap="small")
    with col1:
        department = st.selectbox(
            "Departemen",
            [
                "Civil Service",
                "Fleet Management",
                "Jetty",
                "HR&GA"
            ]
        )
        period = st.selectbox(
            "Periode",
            [
                "Januari",
                "Februari",
                "Maret",
                "April",
                "Mei",
                "Juni",
                "Juli",
                "Agustus",
                "September",
                "Oktober",
                "November",
                "Desember"
            ]
        )
        df_report = get_report_data(department)
        selected = df_report[
            (df_report["Departemen"] == department) &
            (df_report["Periode"] == period)
        ]
        if selected.empty:
            st.warning(
                f"Data report {department} - {period} belum tersedia."
            )
            st.stop()

        report_data = selected.iloc[0]

        civil_service_mapping = {
            "Periode": "E9",
            "Timestamp Submission": "G51",
            "Driver Mixer Truck": "J11",
            "Driver Dump Truck": "J16",
            "Driver Light Truck": "J17",
            "Operator Wheel Loader": "J12",
            "Operator Excavator": "J13",
            "Operator Forklift":"J14",
            "Operator Concrete Pump": "J15",
            "Manpower Batching Plant": "E21",
            "Manpower Acytelin": "E23",
            "Manpower Civil": "E25",
            "Manpower Stone Crusher": "E27",
            "Training Batching Plant": "H21",
            "Training Acytelin": "H23",
            "Training Civil": "H25",
            "Training Stone Crusher": "E27",
            "P2H Batching Plant": "P21",
            "P2H Acytelin": "P23",
            "P2H Civil": "P25",
            "P2H Stone Crusher": "P27",
            "Pelanggaran Batching Plant": "I21",
            "Pelanggaran Acytelin": "I23",
            "Pelanggaran Civil": "I25",
            "Pelanggaran Stone Crusher": "I27",
            "Insiden Batching Plant": "L21",
            "Insiden Acytelin": "L23",
            "Insiden Civil": "L25",
            "Insiden Stone Crusher": "L27",
        }
        fmt_mapping = {
            "Periode": "E9",
            "Timestamp Submission": "G52",
            "Driver Dump Truck": "H12",
            "Operator Excavator": "H13",
            "Operator Bulldozer": "H14",
            "Operator Compactor": "H15",
            "Operator Motor Grader": "H16",
            "Driver Light Truck":"H17",
            "Operator Mobile Crane":"H18",
            "Rigger": "H19",
            "Manpower Karimun Pool": "E23",
            "Manpower Soligi Pool": "E25",
            "Manpower Dispatch": "E27",
            "Manpower Lifting Pool": "E29",
            "Training Karimun Pool": "H23",
            "Training Soligi Pool": "H25",
            "Training Dispatch": "H27",
            "Training Lifting Pool": "H29",
            "P2H Karimun Pool": "O23",
            "P2H Soligi Pool": "O25",
            "P2H Dispatch": "O27",
            "P2H Lifting Pool": "O29",
            "Pelanggaran Karimun Pool": "I23",
            "Pelanggaran Soligi Pool": "I25",
            "Pelanggaran Dispatch": "I27",
            "Pelanggaran Lifting Pool": "I29",
            "Insiden Karimun Pool": "L23",
            "Insiden Soligi Pool": "L25",
            "Insiden Dispatch": "L27",
            "Insiden Lifting Pool": "L29",
        }
        hrga_mapping = {
            "Periode": "E9",
            "Timestamp Submission": "L41",
            "Driver Bus": "H13",
            "Driver Manhaul": "H12",
            "Manpower GA Transportasi": "E17",
            "Training GA": "H17",
            "P2H GA ": "N17",
            "Pelanggaran GA Transportasi": "I17",
            "Insiden GA Transportasi": "K17",
        }
        jetty_mapping = {
            "Periode": "F9",
            "Timestamp Submission": "G52",
            "Driver Trailer": "I12",
            "Operator Wheel Loader": "I13",
            "Operator Mobile Crane": "I14",
            "Operator Crawler Crane": "I15",
            "Rigger Darat": "I16",
            "Rigger Laut":"I17",
            "Operator Forklift":"I18",
            "Operator Ponton Crane":"I19",
            "Operator Crane Truck":"I20",
            "Operator Vacuum Truck" :"I21",
            "Operator Reach Stacker" : "I22",
            "Driver Light Truck" : "I23",
            "Operator Ship Unloader" :"I24",
            "Manpower Crane Type": "F28",
            "Manpower Wheel Type": "F30",
            "Training Crane Type": "I28",
            "Training Wheel Type": "I30",
            "P2H Crane Type": "P28",
            "P2H Wheel Type": "P30",
            "Pelanggaran Crane Type": "J28",
            "Pelanggaran Wheel Type": "J30",
            "Insiden Crane Type": "M28",
            "Insiden Wheel Type": "M30",
        }
        templates = {
            "Civil Service": "template/Civil_Service.xlsx",
            "Fleet Management": "template/Fleet_Management.xlsx",
            "Jetty": "template/Jetty.xlsx",
            "HR&GA": "template/HRGA.xlsx",
        }
        mappings = {
            "Civil Service": civil_service_mapping,
            "Fleet Management": fmt_mapping,
            "Jetty": jetty_mapping,
            "HR&GA": hrga_mapping,
        }
        template = templates[department]
        mapping = mappings[department]
        def generate_report(template_path, output_path, report_data, mapping):
            wb = load_workbook(template_path)
            ws = wb.active
            for column_name, cell in mapping.items():
                if column_name in report_data.index:
                    value = report_data[column_name]
                    if pd.isna(value):
                        value = 0
                    ws[cell] = value
            wb.save(output_path)
        if st.button("Generate Report", type="primary"):

            selected = df_report[
                (df_report["Departemen"] == department) &
                (df_report["Periode"] == period)
            ]

            if selected.empty:

                st.warning(
                    f"Data {department} - {period} belum tersedia."
                )

            else:

                report_data = selected.iloc[0]

                template = templates[department]
                mapping = mappings[department]

                output_dir = Path("reports") / department.replace(" ", "_")
                output_dir.mkdir(parents=True, exist_ok=True)

                output_path = (
                    output_dir /
                    f"SCT-{department}-{period}.xlsx"
                )

                generate_report(
                    template,
                    output_path,
                    report_data,
                    mapping
                )

                st.toast("Report berhasil dibuat!", icon="✅")

                with open(output_path, "rb") as file:

                    st.download_button(
                        "Download Report",
                        data=file,
                        file_name=output_path.name,
                        key="download_report",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        icon=":material/download:"
                    )
    with col2:

        if "report_folder" not in st.session_state:
            st.session_state.report_folder = None

        REPORT_DIR = Path("reports")

        report_folders = {
            "Civil Service": REPORT_DIR / "Civil_Service",
            "Fleet Management": REPORT_DIR / "Fleet_Management",
            "Jetty": REPORT_DIR / "Jetty",
            "HR&GA": REPORT_DIR / "HR&GA",
        }

        if st.session_state.report_folder is None:

            st.subheader("📁 SCT Reports")

            cols = st.columns(2, gap="medium")

            for i, (dept_name, folder) in enumerate(report_folders.items()):

                with cols[i % 2]:

                    files = (
                        list(folder.glob("*.xlsx"))
                        if folder.exists()
                        else []
                    )

                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #D9DDE5;
                            padding: 20px;
                            margin-bottom: 12px;
                            background: white;">
                            <div style="font-size: 32px;">📁</div>
                            <div style="
                                font-size: 17px;
                                font-weight: 600;
                                margin-top: 8px;
                            ">{dept_name}
                            </div>
                            <div style="
                                color: #777;
                                font-size: 13px;
                                margin-top: 4px;
                            ">{len(files)} report
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Open Folder",
                        key=f"open_{dept_name}",
                        use_container_width=True
                    ):
                        st.session_state.report_folder = dept_name
                        st.rerun()
        else:

            selected_folder = st.session_state.report_folder
            folder = report_folders[selected_folder]

            col1x, col2x = st.columns([1, 8])

            with col1x:

                if st.button("← Back", key="back_report_folder"):
                    st.session_state.report_folder = None
                    st.rerun()

            with col2x:

                st.subheader(f"📁 {selected_folder}")

            files = sorted(
                folder.glob("*.xlsx"),
                key=lambda x: x.name
            )

            if not files:

                st.info("Belum ada report di folder ini.")

            else:

                for file in files:

                    col_file, col_download = st.columns(
                        [7, 1],
                        vertical_alignment="center"
                    )

                    with col_file:

                        st.markdown(
                            f"""
                            <div style="
                                border-bottom: 1px solid #E5E7EB;
                                padding: 12px 4px;
                            ">
                                <span style="font-size: 20px;">📄</span>
                                <span style="
                                    margin-left: 10px;
                                    font-size: 14px;
                                ">
                                    {file.name}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col_download:

                        with open(file, "rb") as f:

                            st.download_button(
                                "Download",
                                data=f,
                                file_name=file.name,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_{selected_folder}_{file.name}",
                                use_container_width=True
                            )

with tabs[0]:
    st.subheader("Dashboard Report Departemen")
    col1, col2 = st.columns(2, gap="small")
    df_sumPelanggaran = pd.DataFrame(ws_sumPelanggaran.get_all_records())
    df_sumPD = pd.DataFrame(ws_sumPD.get_all_records())
    bulan = [
        "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus",
        "September", "Oktober", "November", "Desember"
    ]
    bulan_tersedia = [b for b in bulan if b in df_sumPelanggaran.columns]
    bulan_PD_tersedia = [b for b in bulan if b in df_sumPD.columns]
    df_long = df_sumPelanggaran.melt(
        id_vars="Departemen",
        value_vars=bulan_tersedia,
        var_name="Bulan",
        value_name="Pelanggaran")
    df_long["Pelanggaran"] = pd.to_numeric(
        df_long["Pelanggaran"], errors="coerce")
    df_long = df_long.dropna(subset=["Pelanggaran"])
    df_long["Bulan"] = pd.Categorical(
        df_long["Bulan"],
        categories=bulan_tersedia,
        ordered=True)
    chart = alt.Chart(df_long).encode(
        x=alt.X(
            "Bulan:N",
            sort=bulan_tersedia,
            axis=alt.Axis(labelAngle=0)),
        y=alt.Y(
            "Pelanggaran:Q",
            title="Jumlah Pelanggaran",
            scale=alt.Scale(zero=True)),
        color=alt.Color(
            "Departemen:N",
            title="Departemen"),
        tooltip=[
            alt.Tooltip("Departemen:N"),
            alt.Tooltip("Bulan:N"),
            alt.Tooltip("Pelanggaran:Q")
        ])
    lines = chart.mark_line(strokeWidth=2)
    points = chart.mark_circle(size=35, filled=True)
    labels = chart.mark_text(
        dy=-10,
        fontSize=11,
        fontWeight="bold").encode(
        text=alt.Text("Pelanggaran:Q", format=".0f"))
    df_long_PD = df_sumPD.melt(
            id_vars="Departemen",
            value_vars=bulan_tersedia,
            var_name="Bulan",
            value_name="Property Damage")
    df_long_PD["Property Damage"] = pd.to_numeric(
        df_long_PD["Property Damage"], errors="coerce")
    df_long_PD = df_long_PD.dropna(subset=["Property Damage"])
    df_long_PD["Bulan"] = pd.Categorical(
        df_long_PD["Bulan"],
        categories=bulan_PD_tersedia,
        ordered=True)
    chart_PD = alt.Chart(df_long_PD).encode(
        x=alt.X(
            "Bulan:N",
            sort=bulan_PD_tersedia,
            axis=alt.Axis(labelAngle=0)),
        y=alt.Y(
            "Property Damage:Q",
            title="Jumlah Property Damage",
            scale=alt.Scale(zero=True)),
        color=alt.Color(
            "Departemen:N",
            title="Departemen"),
        tooltip=[
            alt.Tooltip("Departemen:N"),
            alt.Tooltip("Bulan:N"),
            alt.Tooltip("Property Damage:Q")
        ])
    lines_PD = chart_PD.mark_line(strokeWidth=2)
    points_PD = chart_PD.mark_circle(size=35, filled=True)
    labels_PD = chart_PD.mark_text(
        dy=-10,
        fontSize=11,
        fontWeight="bold").encode(
        text=alt.Text("Property Damage:Q", format=".0f"))

    with col1:
        with st.container(border=True):
            st.markdown(
                f"""
                <style>
                    .grafik h4 {{
                        margin: 0;
                        font-weight: 200;
                        color: black;
                        text-align: center;
                    }}
                </style>
                <div class="grafik">
                    <h4>Pelanggaran</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.altair_chart(
                lines + points+labels,
                use_container_width=True)
        with st.expander("Data Pelanggaran"):
            st.write(df_sumPelanggaran)
        

    with col2:
        with st.container(border=True):
            st.markdown(
                f"""
                <style>
                    .grafik h4 {{
                        margin: 0;
                        font-weight: 200;
                        color: black;
                        text-align: center;
                    }}
                </style>
                <div class="grafik">
                    <h4>Property Damage</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.altair_chart(
                lines_PD + points_PD+labels_PD,
                use_container_width=True)
        with st.expander("Data Property Damage"):
            st.write(df_sumPD)

    st.subheader("Interpretasi")
    bulan_selected = st.selectbox(
        "Periode",
        options=urutan_bulan, width = 200,
        key="dashboard_periode")

    departemen_list = [
        "Civil Service",
        "Jetty",
        "Fleet Management",
        "HR&GA"]

    df_interpretasi_pelanggaran = df_pelanggaran[
        df_pelanggaran["Bulan"] == bulan_selected].copy()
    df_interpretasi_PD = df_pd[df_pd["Bulan"] == bulan_selected].copy()
    
    cola, colb = st.columns(2, gap="small")
    with cola:
        with st.container(border=True):
            df_total = df_interpretasi_pelanggaran[
                (df_interpretasi_pelanggaran["Departemen"].astype(str).str.strip() == "Total Pelanggaran")
                & (df_interpretasi_pelanggaran["Bulan"] == bulan_selected)
            ]

            if df_total.empty:
                st.info("Interpretasi total belum tersedia.")
            else:
                row_total = df_total.iloc[-1]

                st.markdown("### Interpretasi Total Pelanggaran")

                st.caption("Tren Keseluruhan")
                st.write(row_total["Tren Keseluruhan"] or "Belum diinput")

                st.caption("Status Risiko")
                st.write(row_total["Status Risiko"] or "Belum diinput")

                st.caption("Analisis")
                st.write(row_total["Analisis"] or "Belum diinput")

            for start in range(0, len(departemen_list), 2):
                cols = st.columns(2)

                for offset, col in enumerate(cols):
                    pos = start + offset

                    if pos >= len(departemen_list):
                        break

                    dept = departemen_list[pos]

                    with cols[offset]:
                        with st.container(border=True):
                            st.markdown(f"#### {dept}")

                            data = df_interpretasi_pelanggaran[
                                df_interpretasi_pelanggaran["Departemen"] == dept
                            ]

                            if data.empty:
                                st.info("Interpretasi belum tersedia.")
                                continue

                            row = data.iloc[-1]

                            for label, column in [
                                ("Tren Keseluruhan", "Tren Keseluruhan"),
                                ("Status Risiko", "Status Risiko"),
                                ("Analisis", "Analisis"),
                            ]:
                                value = row.get(column, "")

                                if pd.isna(value) or not str(value).strip():
                                    value = "Belum diinput"

                                st.caption(label)
                                st.write(value)

    with colb:
        with st.container(border=True):
            df_total_pd = df_interpretasi_PD[
                (df_interpretasi_PD["Departemen"].astype(str).str.strip() == "Total Property Damage")
                & (df_interpretasi_PD["Bulan"] == bulan_selected)
            ]

            if df_total_pd.empty:
                st.info("Interpretasi total belum tersedia.")
            else:
                row_total = df_total_pd.iloc[-1]

                st.markdown("### Interpretasi Total Property Damage")

                st.caption("Tren Keseluruhan")
                st.write(row_total["Tren Keseluruhan"] or "Belum diinput")

                st.caption("Status Risiko")
                st.write(row_total["Status Risiko"] or "Belum diinput")

                st.caption("Analisis")
                st.write(row_total["Analisis"] or "Belum diinput")

            for start in range(0, len(departemen_list), 2):
                cols = st.columns(2)

                for offset, col in enumerate(cols):
                    pos = start + offset

                    if pos >= len(departemen_list):
                        break

                    dept = departemen_list[pos]

                    with cols[offset]:
                        with st.container(border=True):
                            st.markdown(f"#### {dept}")

                            data = df_interpretasi_PD[
                                df_interpretasi_PD["Departemen"] == dept
                            ]

                            if data.empty:
                                st.info("Interpretasi belum tersedia.")
                                continue

                            row = data.iloc[-1]

                            for label, column in [
                                ("Tren Keseluruhan", "Tren Keseluruhan"),
                                ("Status Risiko", "Status Risiko"),
                                ("Analisis", "Analisis"),
                            ]:
                                value = row.get(column, "")

                                if pd.isna(value) or not str(value).strip():
                                    value = "Belum diinput"

                                st.caption(label)
                                st.write(value)
    st.divider()
    st.subheader("Data Pemenang Safety Champion Traffic Individu")
    st.caption("Rekap hasil penilaian kandidat berdasarkan periode.")
    bulan_individu = st.selectbox(
            "Periode",
            options=urutan_bulan, width = 200,
            key="dashboard_periode_individu")

    df_individu["Periode"] = (
        df_individu["Periode"].astype(str).str.strip()
    )

    df_individu = df_individu[
        df_individu["Periode"].str.casefold()
        == bulan_individu.casefold()
    ].copy()

    def format_check(value):
        if pd.isna(value):
            return "⬜"

        if isinstance(value, bool):
            return "✅" if value else "❌"

        value = str(value).strip().casefold()

        nilai_true = {"true", "1", "yes", "ya", "☑", "✓", "✔"}
        nilai_false = {"false", "0", "no", "tidak", "☐", "✗", "✘", ""}

        if value in nilai_true:
            return "✅"

        if value in nilai_false:
            return "❌"

        return value

    kolom_checklist = [
        "Pelanggaran",
        "Property Damage",
        "Training",
        "P2H"]
    kolom_tampil = [
        "Nama",
        "NIK",
        "Jabatan",
        "Departemen",
        *kolom_checklist]
    kolom_tersedia = [
        col for col in kolom_tampil
        if col in df_individu.columns
    ]
    if df_individu.empty:
        st.info(
            f"Belum ada data penilaian individu untuk {bulan_individu}."
        )
    else:
        for col in kolom_checklist:
            if col in df_individu.columns:
                df_individu[col] = df_individu[col].apply(format_check)
        df_tampil = df_individu[kolom_tersedia].copy()
        st.dataframe(
            df_tampil,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Nama": st.column_config.TextColumn("Nama"),
                "NIK": st.column_config.TextColumn("NIK"),
                "Jabatan": st.column_config.TextColumn("Jabatan"),
                "Departemen": st.column_config.TextColumn("Departemen"),
                "Pelanggaran": st.column_config.TextColumn("Pelanggaran"),
                "Property Damage": st.column_config.TextColumn(
                    "Property Damage"
                ),
                "Training": st.column_config.TextColumn("Training"),
                "P2H": st.column_config.TextColumn("P2H"),
            })
        st.caption(
            f"Menampilkan {len(df_tampil)} kandidat pada periode "
            f"{bulan_individu}."
        )

with tabs[2]:
    _, col_filter = st.columns([6, 1], gap="small")

    with col_filter:
        periode_filter = st.selectbox("Periode",
                    [
                        "Januari",
                        "Februari",
                        "Maret",
                        "April",
                        "Mei",
                        "Juni",
                        "Juli",
                        "Agustus",
                        "September",
                        "Oktober",
                        "November",
                        "Desember"
                    ], key="periode_filter"
                )
    df_gallery_filtered = df_gallery[
        df_gallery["Periode"].isin([periode_filter])
    ]
    st.markdown("""
            <style>
            .square-img {
                width: 100%;
                aspect-ratio: 1 / 1;
                overflow: hidden;
                border-radius: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }

            .square-img img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: 0.3s ease-in-out;
            }

            .square-img img:hover {
                transform: scale(1.05);
            }

            .img-caption {
                text-align: center;
                font-size: 12px;
                margin-top: 8px;
                color: #444;
            }
            </style>
            """, unsafe_allow_html=True)
    cols_per_row = 3
    rows = df_gallery_filtered.to_dict("records")

    for i in range(0, len(rows), cols_per_row):
        cols = st.columns(cols_per_row)

        for col, row in zip(cols, rows[i:i+cols_per_row]):
            url = row.get("url_clean", "")
            with col:
                if not url:
                    continue

                try:
                    response = requests.get(url, stream=True, timeout=10)
                    content_type = response.headers.get("Content-Type", "")

                    caption = row.get("Caption", "")

                    if "image" in content_type:
                        img_base64 = base64.b64encode(response.content).decode()
                        st.markdown(f"""
                        <div class="square-img">
                            <img src="data:image/jpeg;base64,{img_base64}">
                        </div>
                        """, unsafe_allow_html=True)
                        caption_text = f"**{caption}**"
                        st.markdown(caption_text)

                    else:
                        st.warning("Gagal memuat gambar.")
                        st.write(url)

                except Exception as e:

                    st.error(f"Gagal load gambar: {e}")