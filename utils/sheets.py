import gspread
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime
import uuid

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

##Pelanggaran
def sheet_pelanggaran():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("SCT Database")
    worksheet = spreadsheet.worksheet("Pelanggaran")
    return worksheet

def submission_pelanggaran(values, photo_url=""):
    worksheet = sheet_pelanggaran()
    submission_id = "SCT-" + uuid.uuid4().hex[:8].upper()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    row = [
        submission_id,
        timestamp,
        str(values["Date"]),
        values["Nama Driver/Operator"],
        values["NIK"],
        values["Departemen"],
        values["Team Departemen"],
        values["Pelanggaran"],
        photo_url
    ]
    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )
    return submission_id

##Property Damage
def sheet_property_damage():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("SCT Database")
    worksheet = spreadsheet.worksheet("Property Damage")
    return worksheet

def submission_property_damage(values, photo_url=""):
    worksheet = sheet_property_damage()
    submission_id = "SCT-" + uuid.uuid4().hex[:8].upper()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    row = [
        submission_id,
        timestamp,
        str(values["Date"]),
        values["Nama Driver/Operator"],
        values["NIK"],
        values["Departemen"],
        values["Team Departemen"],
        values["Property Damage"],
        photo_url
    ]
    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )
    return submission_id

##Civil Service
def sheet_cs():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("SCT Database")
    worksheet = spreadsheet.worksheet("Civil Service")
    return worksheet

def submission_cs(values):
    worksheet = sheet_cs()
    submission_id = "SCT-" + uuid.uuid4().hex[:8].upper()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    row = [
        submission_id,
        timestamp,
        values["Periode"],
        values["Total Driver Mixer Truck"],
        values["Total Driver Dump Truck"],
        values["Total Driver Light Truck"],
        values["Total Operator Wheel Loader"],
        values["Total Operator Excavator"],
        values["Total Operator Forklift"],
        values["Total Operator Concrete Pump"],
        values["Manpower Batching Plant Tim"],
        values["Manpower Acytelin Tim"],
        values["Manpower Civil Tim"],
        values["Manpower Stone Crusher Tim"],
        values["Training Batching Plant Tim"],
        values["Training Acytelin Tim"],
        values["Training Civil Tim"],
        values["Training Stone Crusher Tim"],
        values["P2H Batching Plant Tim"],
        values["P2H Acytelin Tim"],
        values["P2H Civil Tim"],
        values["P2H Stone Crusher Tim"]
        ]
    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )
    return submission_id

##Jetty
def sheet_jetty():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("SCT Database")
    worksheet = spreadsheet.worksheet("Jetty")
    return worksheet

def submission_jetty(values):
    worksheet = sheet_jetty()
    submission_id = "SCT-" + uuid.uuid4().hex[:8].upper()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    row = [
        submission_id,
        timestamp,
        values["Periode"],
        values["Total Driver Trailer"],
        values["Total Operator Wheel Loader"],
        values["Total Operator Mobile Crane"],
        values["Total Operator Crawler Crane"],
        values["Total Rigger Darat"],
        values["Total Rigger Laut"],
        values["Total Operator Forklift"],
        values["Total Operator Ponton Crane"],
        values["Total Operator Crane Truck"],
        values["Total Operator Vacuum Truck"],
        values["Total Operator Reach Stacker"],
        values["Total Driver Light Truck"],
        values["Total Operator Ship Unloader"],
        values["Manpower Tim Crane Type"],
        values["Manpower Tim Wheel Type"],
        values["Training Tim Crane Type"],
        values["Training Tim Wheel Type"],
        values["P2H Tim Crane Type"],
        values["P2H Tim Wheel Type"]
        ]
    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )
    return submission_id

##FMT
def sheet_fmt():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("SCT Database")
    worksheet = spreadsheet.worksheet("FMT")
    return worksheet

def submission_fmt(values):
    worksheet = sheet_fmt()
    submission_id = "SCT-" + uuid.uuid4().hex[:8].upper()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    row = [
        submission_id,
        timestamp,
        values["Periode"],
        values["Total Driver Dump Truck"],
        values["Total Operator Excavator"],
        values["Total Operator Bulldozer"],
        values["Total Operator Compactor"],
        values["Total Operator Motor Grader"],
        values["Total Driver Light Truck"],
        values["Total Operator Mobile Crane"],
        values["Total Rigger"],
        values["Manpower Karimun Pool"],
        values["Manpower Soligi Pool"],
        values["Manpower Dispatch Fleet Management"],
        values["Manpower Lifting Pool"],
        values["Training Karimun Pool"],
        values["Training Soligi Pool"],
        values["Training Dispatch Fleet Management"],
        values["Training Lifting Pool"],
        values["P2H Karimun Pool"],
        values["P2H Soligi Pool"],
        values["P2H Dispatch Fleet Management"],
        values["P2H Lifting Pool"]
        ]
    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )
    return submission_id

##HRGA
def sheet_hrga():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("SCT Database")
    worksheet = spreadsheet.worksheet("HRGA")
    return worksheet

def submission_hrga(values):
    worksheet = sheet_hrga()
    submission_id = "SCT-" + uuid.uuid4().hex[:8].upper()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    row = [
        submission_id,
        timestamp,
        values["Periode"],
        values["Total Driver Bus"],
        values["Total Driver Manhaul"],
        values["Manpower GA Transportasi"],
        values["Training GA Transportasi"],
        values["P2H GA Transportasi"]
        ]
    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )
    return submission_id

def sheet_individual():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("SCT Database")
    worksheet = spreadsheet.worksheet("Data Individu")
    return worksheet
def submission_individual(values):
    worksheet = sheet_individual()
    submission_id = "SCT-" + uuid.uuid4().hex[:8].upper()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    row = [
        submission_id,
        timestamp,
        values["Periode"],
        values["Nama Driver/Operator"],
        values["NIK"],
        values["Jabatan"],
        values["Departemen"],
        values["Team Departemen"]   
    ]
    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )
    return submission_id