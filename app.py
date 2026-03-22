import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import urllib.parse

# --- 1. CONFIGURAÇÃO E TEMA DARK ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

# Estilização: Tema Dark, Marca d'água e Branding
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; line-height: 1.4; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 10px; border-radius: 10px; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (PERSISTÊNCIA) ---
hoje = datetime(2026, 3, 22)

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
        "Revestimento": ["Pintura", "Isolamento", "N/I"],
        "Status": ["🔴 Crítico", "🔴 Crítico", "🔴 Crítico"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    with st.expander("Dados da Empresa Cliente", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável", "Eng. Felipe Alves")
        email_dest = st.text_input("E-mail Alertas", "eng.alvescs@gmail.com")
        api_ia = st.text_input("Chave API IA", type="password")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Felipe Alves Consultoria e Serviços | Responsável: {resp_cl}")

with col_c:
    st.markdown(f"""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD EXECUTIVO AVANÇADO ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Ativos Cadastrados", len(st.session_state['db_ativos']), "12 novos", border=True)
c2.metric("🗓️ Inspeções a Vencer", "18", "-3", delta_color="normal", border=True)
c3.metric("⚠️ Alertas Críticos", "8", "+2", delta_color="inverse", border=True)
c4.metric("✅ Conformidade NR 13", "88%", "3.5%", chart_data=[80, 85, 84, 88], chart_type="area", border=True)

# --- 6. FUNCIONALIDADES (ABAS) ---
tabs = st.tabs(["📊 Gestão Técnica", "📜 Histórico de Auditoria", "🔧 Recomendações", "🌡️ Instrumentos", "📁 Documentos"])

with tabs[0]:
    st.subheader("Edição Manual e Salvamento")
    df_antes = st.session_state['db_ativos'].copy()
    
    # Editor de dados (Tabela de 16 colunas)
    edited_df = st.data_editor(st.session_state['db_ativos'], use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Dados e Atualizar Histórico"):
        tipo_acao = ""
        detalhe = ""
        
        if len(edited_df) < len(df_antes):
            tipo_acao, detalhe = "Deleção", f"Removido(s) {len(df_antes) - len(edited_df)} item(ns)"
        elif len(edited_df) > len(df_antes):
            tipo_acao, detalhe = "Adição", f"Adicionado(s) {len(edited_df) - len(df_antes)} novo(s) item(ns)"
        elif not edited_df.equals(df_antes):
            tipo_acao, detalhe = "Modificação", "Alteração técnica de dados na planilha"
            
        if tipo_acao:
            st.session_state['db_ativos'] = edited_df
            nova_log = pd.DataFrame([{"Data/Hora":
