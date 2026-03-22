import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import io

# --- 1. CONFIGURAÇÃO E TEMA DARK (UX INDUSTRIAL) ---
st.set_page_config(
    page_title="Gestão NR 13 - F.A Engenharia", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Estilização Técnica (Branding Felipe Alves Consultoria e Serviços)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 15px; border-radius: 10px; background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (PERSISTÊNCIA) ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame([
        {"Tag": "TA-001", "Tipo": "Vaso de Pressão", "Local": "Porto de Trr", "Categoria": "V", "Fluido": "Ar Comprimido", "Classe": "A", "Status": "Em Dia", "Prox_Insp": "2025-06-10"},
        {"Tag": "VC-102", "Tipo": "Vaso de Pressão", "Local": "Porto de Trr", "Categoria": "II", "Fluido": "Amônia", "Classe": "A", "Status": "Vencido", "Prox_Insp": "2025-06-20"}
    ])

if 'db_instrumentos' not in st.session_state:
    st.session_state['db_instrumentos'] = pd.DataFrame([
        {"Tag_Inst": "PSV-01", "Equipamento": "TA-001", "Tipo": "Válvula", "Vencimento": "2024-08-22", "Status": "Vencido"}
    ])

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP E SMTP ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações Técnicas")
    with st.expander("Planta Cliente", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_cliente = st.text_input("E-mail do Cliente", "gerente.natto@email.com")
    
    with st.expander("Servidor de E-mail (SMTP)", expanded=False):
        smtp_user = st.text_input("Seu Gmail Profissional", "eng.alvescs@gmail.com")
        smtp_pass = st.text_input("Senha de Aplicativo Google", type="password")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Unidade: {setor_cl} | Engenheiro: {resp_cl}")
with col_c:
    st.markdown("""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD GRÁFICO ---
st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric("📦 Equipamentos", len(st.session
