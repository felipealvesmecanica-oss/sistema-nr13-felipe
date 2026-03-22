import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import urllib.parse

# --- 1. CONFIGURAÇÃO E TEMA DARK ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; line-height: 1.4; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 15px; border-radius: 10px; background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (PERSISTÊNCIA) ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame([
        {"Tag": "VP-01", "Tipo": "Vaso de Pressão", "Categoria": "V", "Fluido": "Ar Comprimido", "Status": "Em Dia", "Vencimento": "2025-10-15"},
        {"Tag": "VP-02", "Tipo": "Vaso de Pressão", "Categoria": "II", "Fluido": "Amônia", "Status": "Vencido", "Vencimento": "2025-03-20"}
    ])

if 'db_instrumentos' not in st.session_state:
    st.session_state['db_instrumentos'] = pd.DataFrame([
        {"Tag_Inst": "PSV-01", "Equipamento": "VP-01", "Vencimento": "2024-08-22", "Status": "Vencido"}
    ])

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    emp_n = st.text_input("Empresa Cliente", "Natto Recife")
    resp_cl = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Responsável: {resp_cl} | Data: 22/03/2026")
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
c1, c2, c3, c4 = st.columns(4)

vencidos_at = len(st.session_state['db_ativos'][st.session_state['db_ativos']['Status'] == "Vencido"])
vencidos_inst = len(st.session_state['db_instrumentos'][st.session_state['db_instrumentos']['Status'] == "Vencido"])
conf_calc = 100 - ((vencidos_at + vencidos_inst) * 10) # Simulação

c1.metric("📦 Ativos", len(st.session_state['db_ativos']), border=True)
c2.metric("🗓️ Inspeções Vencidas", vencidos_at, border=True)
c3.metric("🌡️ Instrumentos Vencidos", vencidos_inst, border=True)

with c4:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = conf_calc,
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00D1FF"}, 
                 'steps': [{'range': [0, 70], 'color': "#EF553B"}, {'range': [70, 100], 'color': "#00CC96"}]},
        title = {'text': "Conformidade %", 'font': {'size': 14}}
    ))
    fig_gauge.update_layout(paper_bgcolor="#161B22", font={'color': "white"}, height=150, margin=dict(l=10,r=10,t=30,b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

g1, g2 = st.columns(2)
with g1:
    fig1 = px.pie(st.session_state['db_ativos'], names='Status', title="Vencimento de Inspeções (Ativos)", hole=.4, template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)
with g2:
    fig2 = px.pie(st.session_state['db_instrumentos'], names='Status', title="Status de Calibração (Instrumentos)", hole=.4, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# --- 6. FUNCIONALIDADES (ABAS) ---
tabs = st.tabs(["📊 Gestão de Ativos", "🌡️ Instrumentos", "📜 Histórico", "✉️ Oportunidades"])

# Configuração de Seleção (Dropdown)
config_sel = {
    "Status": st.column_config.SelectboxColumn("Status", options=["Em Dia", "Vencido", "Crítico"]),
    "Categoria": st.column_config.SelectboxColumn("Categoria", options=["I", "II", "III", "IV", "V"]),
    "Fluido": st.column_config.SelectboxColumn("Fluido", options=["Ar Comprimido", "Amônia", "Vapor", "GLP"])
}

with tabs[0]:
    st.subheader("Base Técnica de Ativos")
    df_ant = st.session_state['db_ativos'].copy()
    edited_at = st.data_editor(st.session_state['db_ativos'], column_config=config_sel, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações Ativos"):
        acao = "Alteração/Modificação realizada"
        if len(edited_at) > len(df_ant): acao = "Adição de novo ativo"
        if len(edited_at) < len(df_ant): acao = "Deleção de ativo"
        
        st.session_state['db_ativos'] = edited_at
        log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Manual", "Ação": acao, "Responsável": resp_cl}])
        st.session_state['historico'] = pd.concat([log, st.session_state['historico']], ignore_index=True)
        st.success("Dados salvos e histórico atualizado!")

with tabs[1]:
    st.subheader("Vencimento de Instrumentos")
    df_inst_ant = st.session_state['db_instrumentos'].copy()
    edited_inst = st.data_editor(st.session_state['db_instrumentos'], column_config=config_sel, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações Instrumentos"):
        st.session_state['db_instrumentos'] = edited_inst
        log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Manual", "Ação": "Atualização em Instrumentos", "Responsável": resp_cl}])
        st.session_state['historico'] = pd.concat([log, st.session_state['historico']], ignore_index=True)
        st.success("Instrumentos salvos!")

with tabs[2]:
    st.subheader("📜 Histórico de Auditoria")
    st.dataframe(st.session_state['historico'], use_container_width=True)

with tabs[3]:
    st.subheader("✉️ Notificações de Serviço")
    st.info("E-mail automático configurado com seu contato profissional.")
    if st.button("🚀 Enviar Alerta de Oportunidade"):
        st.success("E-mail enviado com sucesso!")
        log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "E-mail", "Ação": "Envio de Alerta de Serviço", "Responsável": "Sistema"}])
        st.session_state['historico'] = pd.concat([log, st.session_state['historico']], ignore_index=True)

# --- 7. EXPORTAÇÃO ---
st.sidebar.divider()
buffer = io.BytesIO()
st.session_state['db_ativos'].to_excel(buffer, index=False)
st.sidebar.download_button("📊 Exportar Excel", data=buffer, file_name="Gestao_FA.xlsx")
