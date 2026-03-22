import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import urllib.parse

# --- 1. CONFIGURAÇÃO E TEMA DARK (UX INDUSTRIAL) ---
st.set_page_config(
    page_title="Gestão NR 13 - F.A Engenharia", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Estilização: Tema Dark, Marca d'água e Cards Profissionais
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; line-height: 1.4; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 15px; border-radius: 10px; background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (BANCO DE DADOS) ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame([
        {"Tag": "TA-001", "Tipo": "Vaso de Pressão Schulz", "Local": "Setor A", "Categoria": "V", "Fluido": "Ar Comprimido", "Status": "Em Dia", "Prox_Insp": "2025-06-10"},
        {"Tag": "VC-102", "Tipo": "Vaso de Pressão Mebrafe", "Local": "Setor B", "Categoria": "II", "Fluido": "Amônia", "Status": "Vencido", "Prox_Insp": "2025-06-20"}
    ])

if 'db_instrumentos' not in st.session_state:
    st.session_state['db_instrumentos'] = pd.DataFrame([
        {"Tag_Inst": "PSV-01", "Equipamento": "TA-001", "Tipo": "Válvula de Segurança", "Vencimento": "2024-08-22", "Status": "Vencido"}
    ])

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP E CONFIGURAÇÕES ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    with st.expander("Planta Cliente", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_cliente = st.text_input("E-mail Destinatário", "gerente.natto@email.com")
    
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Unidade: {setor_cl} | Engenheiro: {resp_cl}")
with col_c:
    st.markdown(f"""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD GRÁFICO (REMODELADO E ATRATIVO) ---
st.divider()
m1, m2, m3, m4 = st.columns(4)

ativos_vencidos = len(st.session_state['db_ativos'][st.session_state['db_ativos']['Status'] == "Vencido"])
inst_vencidos = len(st.session_state['db_instrumentos'][st.session_state['db_instrumentos']['Status'] == "Vencido"])

m1.metric("📦 Equipamentos", len(st.session_state['db_ativos']), border=True)
m2.metric("🗓️ Inspeções Vencidas", ativos_vencidos, border=True)
m3.metric("🌡️ Instrum. Vencidos", inst_vencidos, border=True)

# Cálculo de Conformidade ATRATIVO (Usando Gauge Chart)
conformidade = 88 # Exemplo
with m4:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = conformidade,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "✅ Conformidade NR 13 (%)", 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#00D1FF"}, # Azul FA Engenharia
            'bgcolor': "#161B22",
            'borderwidth': 2,
            'bordercolor': "#30363D",
            'steps': [
                {'range': [0, 60], 'color': '#EF553B'}, # Vermelho (Risco)
                {'range': [60, 90], 'color': '#FEC631'}, # Amarelo (Atenção)
                {'range': [90, 100], 'color': '#00CC96'} # Verde (Seguro)
            ],
        }
    ))
    fig_gauge.update_layout(paper_bgcolor="#161B22", plot_bgcolor="#161B22", font={'color': "white"}, height=200, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

g1, g2 = st.columns(2)
with g1:
    # Gráfico 1: Vencimento da Inspeção de Ativos
    fig_insp = px.pie(st.session_state['db_ativos'], names='Status', title="Conformidade de Ativos (Vencimento da Inspeção)", hole=.4, template="plotly_dark", color_discrete_sequence=['#EF553B', '#00CC96'])
    st.plotly_chart(fig_insp, use_container_width=True)

with g2:
    # Gráfico 2: Status de Instrumentos
    fig_inst = px.pie(st.session_state['db_instrumentos'], names='Status', title="Status de Instrumentos", hole=.4, template="plotly_dark", color_discrete_sequence=['#EF553B', '#00CC96'])
    st.plotly_chart(fig_inst, use_container_width=True)

# --- 6. FUNCIONALIDADES ---
tabs = st.tabs(["📊 Gestão de Ativos", "🌡️ Instrumentos", "📜 Histórico", "📁 Documentos"])

# Configuração de Dropdowns (Seleção)
config_drop = {
    "Status": st.column_config.SelectboxColumn("Status", options=["Em Dia", "Vencido", "Crítico", "Aguardando"]),
    "Categoria": st.column_config.SelectboxColumn("Categoria", options=["I", "II", "III", "IV", "V"]),
    "Fluido": st.column_config.SelectboxColumn("Fluido", options=["Ar Comprimido", "Amônia", "Vapor", "Água", "GLP"]),
    "Classe": st.column_config.SelectboxColumn("Classe", options=["A", "B", "C", "D"])
}

with tabs[0]:
    st.subheader("Base Técnica de Ativos (Edição com Seleção)")
    df_prev = st.session_state['db_ativos'].copy()
    edited_ativos = st.data_editor(st.session_state['db_ativos'], column_config=config_drop, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações Ativos"):
        tipo_acao, detalhe = "", ""
        if len(edited_ativos) < len(df_prev):
            tipo_acao, detalhe = "Deleção", "Remoção de equipamento da base"
        elif len(edited_ativos) > len(df_prev):
            tipo_acao, detalhe = "Adição", "Inclusão de novo equipamento"
        elif not edited_ativos.equals(df_prev):
            tipo_acao, detalhe = "Modificação", "Alteração técnica na planilha de ativos"
        
        if tipo_acao:
            st.session_state['db_ativos'] = edited_ativos
            log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": tipo_acao, "Ação": detalhe, "Responsável": resp_cl}])
            st.session_state['historico'] = pd.concat([log, st.session_state['historico']], ignore_index=True)
            st.success(f"Dados salvos: {detalhe}")

with tabs[1]:
    st.subheader("Base de Instrumentos (Edição com Seleção)")
    inst_antes = st.session_state['db_instrumentos'].copy()
    edited_inst = st.
