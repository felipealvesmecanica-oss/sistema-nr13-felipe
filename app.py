import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import urllib.parse # Para o link do WhatsApp

# --- 1. CONFIGURAÇÃO E TEMA DARK ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; line-height: 1.4; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. PERSISTÊNCIA DE DADOS E HISTÓRICO ---
hoje = datetime(2026, 3, 22)

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
        "Dias p/ Vencimento Externa": ["🔴 VENCIDO", "🔴 VENCIDO", "🔴 VENCIDO"],
        "Dias p/ Vencimento Interna": ["🔴 VENCIDO", "473 dias", "604 dias"],
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"],
        "Modelo": ["Horizontal", "Horizontal", "Horizontal"],
        "Ano de Fabricação": [2021, 2011, 2011],
        "Revestimento": ["Pintura", "Isolamento", "N/I"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    with st.expander("Dados da Planta", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável", "Eng. Felipe Alves")
        email_dest = st.text_input("E-mail Alertas", "eng.alvescs@gmail.com")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Felipe Alves Consultoria e Serviços | Setor: {setor_cl}")

with col_c:
    st.markdown("""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD E ALERTAS ---
st.divider()
g1, g2 = st.columns([2, 1])
with g1:
    fig = px.pie(st.session_state['db_ativos'], names='Categoria NR 13', title="Distribuição por Categoria", hole=.4, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("💡 Oportunidades de Serviço")
    st.warning("⚠️ Detectado: Ativos com inspeção vencida. Risco de multa e interdição técnica.")
    # Link direto para WhatsApp
    texto_zap = urllib.parse.quote(f"Olá Felipe, vi no sistema que a {emp_n} tem equipamentos vencidos. Preciso de um orçamento para regularização.")
    st.markdown(f'<a href="https://wa.me/5581997538656?text={texto_zap}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">💬 Chamar no WhatsApp agora</button></a>', unsafe_allow_html=True)

# --- 6. FUNCIONALIDADES ---
tabs = st.tabs(["📊 Gestão Técnica", "📜 Histórico de Auditoria", "✉️ Enviar Oportunidade"])

with tabs[0]:
    st.subheader("Edição Manual da Base de Dados")
    df_temp = st.session_state['db_ativos'].copy()
    edited_df = st.data_editor(st.session_state['db_ativos'], use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações na Planilha"):
        if not edited_df.equals(df_temp):
            st.session_state['db_ativos'] = edited_df
            nova_log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Manual", "Ação": "Modificação/Deleção de dados técnicos", "Responsável": resp_cl}])
            st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)
            st.success("Alterações salvas e registradas no histórico!")
        else:
            st.info("Nenhuma modificação detectada.")

with tabs[1]:
    st.subheader("📜 Histórico de Atualizações")
    st.dataframe(st.session_state['historico'], use_container_width=True)

with tabs[2]:
    st.subheader("✉️ Enviar Relatório de Oportunidades")
    
    # Correção do KeyError: Usando 'Categoria NR 13' em vez de 'Categoria'
    cat_exemplo = st.session_state['db_ativos']['Categoria NR 13'].iloc[0]
    
    email_msg = f"""
    Assunto: 🛡️ Oportunidade de Conformidade Detectada - {emp_n}
    
    Prezado(a) {resp_cl},
    
    O sistema da Felipe Alves Consultoria e Serviços identificou que sua planta possui equipamentos operando fora dos requisitos da NR 13 (Categoria {cat_exemplo}).
    
    🚨 RISCO DETECTADO:
    - Vencimentos de inspe
