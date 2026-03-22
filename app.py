import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# --- 1. CONFIGURAÇÃO E TEMA DARK ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (BANCO DE DADOS) ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame([
        {"Tag": "TA-001", "Tipo": "Vaso de Pressão", "Local": "Porto de Trr", "Categoria": "V", "Fluido": "Ar Comprimido", "Classe": "C", "Prox_Ext": "2025-06-10", "Status": "Em Dia"},
        {"Tag": "VC-102", "Tipo": "Vaso de Pressão", "Local": "Porto de Trr", "Categoria": "II", "Fluido": "Amônia", "Classe": "A", "Prox_Ext": "2025-06-20", "Status": "Vencido"}
    ])

if 'db_instrumentos' not in st.session_state:
    st.session_state['db_instrumentos'] = pd.DataFrame([
        {"Tag_Inst": "PSV-01", "Equipamento": "TA-001", "Tipo": "Válvula", "Vencimento": "2024-08-22", "Status": "Vencido"}
    ])

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP E SMTP ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações do Sistema")
    with st.expander("Configuração de Planta", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_cliente = st.text_input("E-mail Destinatário", "cliente@email.com")
    
    with st.expander("Configuração de E-mail (SMTP)", expanded=False):
        st.caption("Para envio real, use o SMTP do Gmail.")
        smtp_user = st.text_input("Seu E-mail (Gmail)", "eng.alvescs@gmail.com")
        smtp_pass = st.text_input("Senha de Aplicativo", type="password")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Unidade: {setor_cl} | Engenheiro: {resp_cl}")
with col_c:
    st.markdown(f"""<div class="contact-card"><b>Felipe Alves Consultoria e Serviços</b><br>📞 (81) 99753-8656<br>📧 eng.alvescs@gmail.com</div>""", unsafe_allow_html=True)

# --- 5. DASHBOARD GRÁFICO ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Equipamentos", len(st.session_state['db_ativos']), border=True)
c2.metric("🗓️ Inspeções Vencidas", "1", border=True)
c3.metric("⚠️ Alertas Críticos", "2", delta_color="inverse", border=True)
c4.metric("✅ Conformidade", "92%", chart_data=[85, 88, 92, 92], border=True)

g1, g2 = st.columns(2)
with g1:
    fig_p = px.pie(st.session_state['db_ativos'], names='Status', title="Status de Conform
