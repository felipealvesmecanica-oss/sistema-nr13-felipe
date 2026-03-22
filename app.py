import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# --- 1. CONFIGURAÇÃO E TEMA DARK ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 12px; line-height: 1.2; color: #BBB; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS E HISTÓRICO ---
hoje = datetime(2026, 3, 22)

if 'db_ativos' not in st.session_state:
    # Banco de dados inicial com 16 colunas
    st.session_state['db_ativos'] = pd.DataFrame({
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"],
        "Tipo": ["Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão"],
        "Local": ["Oficina", "Sala de Máquinas", "Sala de Máquinas"],
        "Categoria": ["V", "II", "III"],
        "Fluído": ["Ar Comprimido", "Amônia", "Amônia"],
        "Classe": ["C", "A", "A"],
        "Insp. Externa": ["2023-08-23", "2023-04-18", "2023-08-27"],
        "Prox. Externa": ["2025-08-24", "2025-04-18", "2025-08-27"],
        "Insp. Interna": ["2023-08-23", "2023-04-18", "2023-08-27"],
        "Prox. Interna": ["2025-08-24", "2027-04-08", "2027-08-17"],
        "Dias p/ Vencimento": ["VENCIDO", "VENCIDO", "VENCIDO"],
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"],
        "Modelo": ["Horizontal", "Horizontal", "Horizontal"],
        "Ano": [2021, 2011, 2011],
        "Revestimento": ["Pintura", "Isolamento", "N/I"],
        "Status": ["🔴 Crítico", "🔴 Crítico", "🔴 Crítico"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    with st.expander("Dados da Empresa", expanded=False):
        emp_nome = st.text_input("Empresa", "Natto Recife")
        setor_cliente = st.text_input("Setor", "Utilidades")
        resp_cliente = st.text_input("Responsável Gestão", "Eng. Felipe Alves")
        email_alerta = st.text_input("E-mail para Alertas", "eng.alvescs@gmail.com")
        api_key_ia = st.text_input("Chave API IA", type="password")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([3, 1])
with col_t:
    st.title(f"🛡️ Gestão de Ativos NR 13 - {emp_nome}")
    st.info(f"Setor: {setor_cliente} | Responsável: {resp_cliente}")
with col_c:
    st.markdown(f"""<div class="contact-card"><b>Felipe Alves Consultoria e Serviços</b><br>📞 (81) 99753-8656<br>📸 @felipeal
