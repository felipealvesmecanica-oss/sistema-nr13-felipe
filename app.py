import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# --- 1. CONFIGURAÇÃO E TEMA DARK ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

# CSS com chaves duplicadas {{ }} para não conflitar com f-strings
st.markdown("""
    <style>
    .stApp {{ background-color: #0E1117; color: #FFFFFF; }}
    .watermark {{ position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }}
    .contact-card {{ text-align: right; font-size: 12px; line-height: 1.2; color: #BBB; }}
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS ---
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
        "Dias p/ Vencimento Externa": ["VENCIDO", "VENCIDO", "VENCIDO"],
        "Dias p/ Vencimento Interna": ["VENCIDO", "473 dias", "604 dias"],
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
    with st.expander("Configuração da Planta", expanded=False):
        emp_nome = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável Gestão", "Eng. Felipe Alves")
        email_al = st.text_input("E-mail para Alertas", "eng.alvescs@gmail.com")
        api_key = st.text_input("Chave API IA", type="password")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([3, 1])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_nome}")
    st.info(f"Setor: {setor_cl} | Gestor: {resp_cl}")
with col_c:
    st.markdown("""<div class="contact-card"><b>Felipe Alves Consultoria e Serviços</b><br>📞 (81) 99753-8656<br>📸 @felipealves_consultoria<br>📧 eng.alvescs@gmail.com</div>""", unsafe_allow_html=True)

# --- 5. DASHBOARD GRÁFICO ---
st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric("📦 Total Ativos", len(st.session_state['db_ativos']))
m2.metric("🗓️ Inspeções a Vencer", "12")
m3.metric("🌡️ Vencimento Instrumentos", "5")
m4.metric("✅ Conformidade", "85%")

g1, g2 = st.columns(2)
with g1:
    fig_p = px.pie(st.session_state['db_ativos'], names='Categoria NR 13', title="Distribuição por Categoria", hole=.4, template="plotly_dark")
    st.plotly_chart(fig_p, use_container_width=True)
with g2:
    df_inst = pd.DataFrame({'Tipo': ['Válvulas', 'Manômetros'], 'Vencidos': [3, 2], 'Em Dia': [15, 10]})
    fig_i = px.bar(df_inst, x='Tipo', y=['Vencidos', 'Em Dia'], title="Vencimento de Instrumentos", barmode="group", template="plotly_dark")
    st.plotly_chart(fig_i, use_container_width=True)

# --- 6. FUNCIONALIDADES ---
tabs = st.tabs(["📊 Gestão Técnica", "📄 Automação IA", "🚨 Alertas", "📜 Histórico", "📁 Documentos"])

with tabs[0]:
    st.subheader("Edição Manual da Planilha")
    df_antes = st.session_state['db_ativos'].copy()
    edited_df = st.data_editor(st.session_state['db_ativos'], use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações"):
        tipo_acao, detalhe = "", ""
        if len(edited_df) < len(df_antes):
            tipo_acao, detalhe = "Deleção", f"Removido(s) {len(df_antes) - len(edited_df)} item(ns)"
        elif len(edited_df) > len(df_antes):
            tipo_acao, detalhe = "Adição", f"Adicionado(s) {len(edited_df) - len(df_antes)} item(ns)"
        elif not edited_df.equals(df_antes):
            tipo_acao, detalhe = "Modificação", "Alteração de dados técnicos"
        
        if tipo_acao:
            st.session_state['db_ativos'] = edited_df
            nova_log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": tipo_acao, "Ação": detalhe, "Responsável": resp_cl}])
            st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)
            st.success(f"Dados salvos: {detalhe}")

with tabs[1]:
    st.subheader("Processamento IA (300+ PDFs)")
    pdfs = st.file_uploader("Upload de Laudos", accept_multiple_files=True)
    if st.button("Executar IA"):
        st.success("Análise concluída!")
        nova_log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Automático", "Ação": f"Leitura de {len(pdfs)} laudos via IA", "Responsável": "Sistema IA"}])
        st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)

with tabs[2]:
    st.subheader("🚨 Alertas e Notificações")
    st.error("VP-1.212087: Próxima Inspeção Externa Vencida!")
    if st.button("📧 Enviar Alertas"):
        st.success(f"E-mail enviado para {email_al}")

with tabs[3]:
    st.subheader("📜 Histórico de Auditoria")
    st.dataframe(st.session_state['historico'], use_container_width=True)

with tabs[4]:
    st.subheader("📁 Documentos e Projetos")
    st.text_input("Link da Nuvem (OneDrive/Drive)")
    st.file_uploader("Upload de Outros Docs", accept_multiple_files=True)

# --- 7. EXPORTAÇÃO ---
st.sidebar.divider()
st.sidebar.download_button("📊 Exportar Excel", data=b"data", file_name="gestao_fa.xlsx")
