import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Gym Venom Pro", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
    [data-testid="stHeader"] {display:none !important;}
    .stApp { background-color: #0E1117; }
    html, body, p, h1, h2, h3, h4, span, label, .stMarkdown { color: #FFFFFF !important; }
    input, .stSelectbox div[data-baseweb="select"], .stSelectbox select { 
        background-color: #262730 !important; color: #FFFFFF !important; border-color: #4a4a4a !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    hr { border-color: #4a4a4a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS ---
DB_NAME = "database_gym.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS socios (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE, fecha_inicio TEXT, 
        fecha_fin TEXT, monto_pagado REAL, ultima_asistencia TEXT)""")
    cursor.execute("CREATE TABLE IF NOT EXISTS finanzas (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, concepto TEXT, monto REAL, fecha TEXT)")
    conn.commit(); conn.close()

init_db()

def get_data():
    conn = sqlite3.connect(DB_NAME)
    soc = pd.read_sql_query("SELECT * FROM socios", conn)
    fin = pd.read_sql_query("SELECT * FROM finanzas", conn)
    conn.close()
    return soc, fin

df_soc, df_fin = get_data()
hoy = datetime.now()
hoy_str = hoy.strftime("%d/%m/%Y %H:%M")

# --- 3. CABECERA ---
st.title("🏋️‍♂️ GYM VENOM - CONTROL")

# --- 4. REGISTRO FRONTAL ---
with st.expander("➕ REGISTRAR PAGO / NUEVO SOCIO", expanded=False):
    with st.form("nuevo_pago", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        f_nom = c1.text_input("Nombre del Socio").upper()
        f_monto = c2.number_input("Monto Bs", min_value=0.0, value=150.0)
        f_tipo = c3.selectbox("Plan", ["Mensual", "Semanal", "Diario"])
        if st.form_submit_button("REGISTRAR"):
            if f_nom:
                dias = 30 if f_tipo == "Mensual" else (7 if f_tipo == "Semanal" else 1)
                f_vence = (hoy + timedelta(days=dias)).strftime("%Y-%m-%d")
                conn = sqlite3.connect(DB_NAME)
                conn.execute("INSERT OR REPLACE INTO socios (nombre, fecha_inicio, fecha_fin, monto_pagado) VALUES (?,?,?,?)", 
                             (f_nom, hoy.strftime("%Y-%m-%d"), f_vence, f_monto))
                conn.execute("INSERT INTO finanzas (tipo, concepto, monto, fecha) VALUES (?,?,?,?)", 
                             ("INGRESO", f"PAGO {f_tipo}: {f_nom}", f_monto, hoy_str))
                conn.commit(); conn.close(); st.rerun()

st.divider()

# --- 5. TABS PRINCIPALES ---
t1, t2 = st.tabs(["👥 SOCIOS", "💰 CAJA"])

with t1:
    if not df_soc.empty:
        for _, row in df_soc.iterrows():
            vence_dt = datetime.strptime(row['fecha_fin'], "%Y-%m-%d")
            restan = (vence_dt - hoy).days + 1
            color = "green" if restan > 3 else ("orange" if restan >= 0 else "red")
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
            col1.write(f"**{row['nombre']}**")
            col2.write(f":{color}[Vence en: {restan} días]")
            col3.write(f"Vence: {vence_dt.strftime('%d/%m')}")
            if col4.button("🗑️", key=f"del_{row['id']}"):
                conn = sqlite3.connect(DB_NAME); conn.execute("DELETE FROM socios WHERE id=?", (row['id'],))
                conn.commit(); conn.close(); st.rerun()
            st.write("---")

with t2:
    st.subheader("Balance General")
    ins = df_fin['monto'].sum()
    st.metric("Total en Caja", f"{ins:.2f} Bs")
    st.dataframe(df_fin, hide_index=True, use_container_width=True)