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

# Estilização Técnica Profissional
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; line-height: 1.4; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 10px; border-radius: 10px; background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DO BANCO DE DADOS (16 COLUNAS) ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame({
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"],
        "Tipo de Equipamento": ["Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão"],
        "Local de Instalação": ["Oficina", "Sala de Máquinas", "Sala de Máquinas"],
        "Categoria NR 13": ["V", "II", "III"],
        "Fluído": ["Ar Comprimido", "Amônia", "Amônia"],
        "Classe de Fluído": ["C", "A", "A"],
        "Inspeção Externa": ["23/08/2023", "18/04/2023", "27/08/2023"],
        "Próxima Externa": ["24/08/2025", "18/04/2025", "27/08/2025"],
        "Inspeção Interna": ["23/08/2023", "18/04/2023", "27/08/2023"],
        "Próxima Interna": ["24/08/2025", "2027-04-08", "2027-08-17"],
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
    st.markdown("### ⚙️ Painel de Configuração")
    with st.expander("Dados da Unidade", expanded=False):
        emp_nome = st.text_input("Nome da Empresa", "Natto Recife")
        setor_unidade = st.text_input("Setor", "Utilidades")
        resp_tecnico = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_alerta = st.text_input("E-mail para Alertas", "eng.alvescs@gmail.com")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_nome}")
    st.caption(f"Status do Sistema: Operacional | Unidade: {setor_unidade}")

with col_c:
    st.markdown("""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD EXECUTIVO (MÉTRICAS TÉCNICAS) ---
st.divider()
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    label="📦 Ativos Cadastrados", 
    value=len(st.session_state['db_ativos']), 
    delta="Base Atualizada", 
    border=True
)
c2.metric(
    label="🗓️ Inspeções a Vencer", 
    value="18", 
    delta="-3", 
    delta_color="normal", 
    border=True
)
c3.metric(
    label="⚠️ Alertas Críticos", 
    value="8", 
    delta="+2", 
    delta_color="inverse", 
    border=True
)
c4.metric(
    label="✅ Conformidade NR 13", 
    value="88%", 
    chart_data=[82, 85, 84, 88
