import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import urllib.parse

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL (DARK MODE) ---
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
    .contact-card { text-align: right; font-size: 13px; line-height: 1.4; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 10px; border-radius: 10px; background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (16 COLUNAS TÉCNICAS) ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame({
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"],
        "Tipo de Equipamento": ["Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão"],
        "Local de Instalação": ["Oficina", "Sala de Máquinas", "Sala de Máquinas"],
        "Categoria NR 13": ["V", "II", "III"],
        "Fluído": ["Ar Comprimido", "Amônia", "Amônia"],
        "Classe de Fluído": ["C", "A", "A"],
        "Inspeção Externa": ["2023-08-23", "2023-04-18", "2023-08-27"],
        "Próxima Externa": ["2025-08-24", "2025-04-18", "2025-08-27"],
        "Inspeção Interna": ["2023-08-23", "2023-04-18", "2023-08-27"],
        "Próxima Interna": ["2025-08-24", "2027-04-08", "2027-08-17"],
        "Dias p/ Vencimento": ["🔴 VENCIDO", "🔴 VENCIDO", "🔴 VENCIDO"],
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"],
        "Modelo": ["Horizontal", "Horizontal", "Horizontal"],
        "Ano de Fabricação": [2021, 2011, 2011],
        "Revestimento": ["Pintura Epóxi", "Isolamento Térmico", "N/I"],
        "Status": ["🔴 Crítico", "🔴 Crítico", "🔴 Crítico"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP DO CLIENTE ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    with st.expander("Configuração da Planta", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_dest = st.text_input("E-mail para Alertas", "eng.alvescs@gmail.com")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Unidade: {setor_cl} | Gestão Técnica Centralizada")

with col_c:
    st.markdown("""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# ---
