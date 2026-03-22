import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import io

# --- 1. CONFIGURAÇÃO E TEMA DARK ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 10px; border-radius: 10px; background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame([
        {"Tag": "TA-001", "Tipo": "Vaso de Pressão", "Local": "Porto de Trr", "Categoria": "V", "Fluido": "Ar Comprimido", "Classe": "C", "Status": "Em Dia", "Próxima Inspeção": "2025-06-10"},
        {"Tag": "VC-102", "Tipo": "Vaso de Pressão", "Local": "Porto de Trr", "Categoria": "II", "Fluido": "Amônia", "Classe": "A", "Status": "Vencido", "Próxima Inspeção": "2025-06-20"}
    ])

if 'db_instrumentos' not in st.session_state:
    st.session_state['db_instrumentos'] = pd.DataFrame([
        {"Tag_Inst": "PSV-01", "Equipamento": "TA-001", "Tipo": "Válvula", "Vencimento": "2024-08-22", "Status": "Vencido"}
    ])

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP E SMTP ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    with st.expander("Planta Cliente", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_cliente = st.text_input("E-mail Destinatário", "cliente@email.com")
    
    with st.expander("Servidor de E-mail (SMTP)", expanded=False):
        smtp_user = st.text_input("Seu E-mail (Gmail)", "eng.alvescs@gmail.com")
        smtp_pass = st.text_input("Senha de Aplicativo", type="password")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Unidade: {setor_cl} | Engenheiro Responsável: {resp_cl}")
with col_c:
    st.markdown(f"""<div class="contact-card"><b>Felipe Alves Consultoria e Serviços</b><br>📞 (81) 99753-8656<br>📧 eng.alvescs@gmail.com</div>""", unsafe_allow_html=True)

# --- 5. DASHBOARD GRÁFICO ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Equipamentos", len(st.session_state['db_ativos']), border=True)
c2.metric("🗓️ Vencidos", len(st.session_state['db_ativos'][st.session_state['db_ativos']['Status'] == "Vencido"]), border=True)
c3.metric("🌡️ Instrumentos", len(st.session_state['db_instrumentos']), border=True)
c4.metric("✅ Conformidade", "92%", border=True)

g1, g2 = st.columns(2)
with g1:
    fig_p = px.pie(st.session_state['db_ativos'], names='Status', title="Status de Conformidade Ativos", hole=.4, template="plotly_dark")
    st.plotly_chart(fig_p, use_container_width=True)
with g2:
    fig_i = px.pie(st.session_state['db_instrumentos'], names='Status', title="Status Instrumentos", hole=.4, template="plotly_dark", color_discrete_sequence=['#EF553B', '#00CC96'])
    st.plotly_chart(fig_i, use_container_width=True)

# --- 6. FUNCIONALIDADES ---
tabs = st.tabs(["📊 Gestão de Ativos", "🌡️ Instrumentos", "📜 Histórico", "✉️ Envio de Alertas"])

# Configuração de Dropdowns (Seleção)
config_selecao = {
    "Status": st.column_config.SelectboxColumn("Status", options=["Em Dia", "Vencido", "Crítico", "Aguardando"]),
    "Categoria": st.column_config.SelectboxColumn("Categoria", options=["I", "II", "III", "IV", "V"]),
    "Fluido": st.column_config.SelectboxColumn("Fluido", options=["Ar Comprimido", "Amônia", "Vapor", "Água", "GLP"]),
    "Classe": st.column_config.SelectboxColumn("Classe", options=["A", "B", "C", "D"])
}

with tabs[0]:
    st.subheader("Base Técnica de Ativos")
    df_antes = st.session_state['db_ativos'].copy()
    edited_ativos = st.data_editor(st.session_state['db_ativos'], column_config=config_selecao, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações Ativos"):
        tipo_log, detalhe = "", ""
        if len(edited_ativos) < len(df_antes):
            tipo_log, detalhe = "Deleção", "Remoção de equipamento da base"
        elif len(edited_ativos) > len(df_antes):
            tipo_log, detalhe = "Adição", "Inclusão de novo equipamento"
        elif not edited_ativos.equals(df_antes):
            tipo_log, detalhe = "Modificação
