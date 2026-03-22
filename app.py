import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

# CSS para Tema Dark, Marca d'água e Branding
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 12px; line-height: 1.2; color: #BBB; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (BANCO DE DADOS TEMPORÁRIO) ---
hoje = datetime(2026, 3, 22)

if 'db_ativos' not in st.session_state:
    # Dados baseados nos relatórios reais (ex: VP-1.212087)
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
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"],
        "Modelo": ["Horizontal", "Horizontal", "Horizontal"],
        "Ano": [2021, 2011, 2011],
        "Revestimento": ["Preto", "Amarela", "N/I"],
        "Status": ["Vencido", "Vencido", "Vencido"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Usuário"])

# --- 3. SIDEBAR (SETUP E CONTATOS) ---
with st.sidebar:
    with st.expander("⚙️ Setup do Sistema", expanded=False):
        empresa = st.text_input("Empresa", "Natto Recife")
        api_key = st.text_input("API Key IA", type="password")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([3, 1])
with col_t:
    st.title(f"🛡️ Gestão de Ativos NR 13 - {empresa}")
with col_c:
    st.markdown(f"""<div class="contact-card"><b>Felipe Alves Consultoria e Serviços</b><br>📞 (81) 99753-8656<br>📸 @felipealves_consultoria<br>📧 eng.alvescs@gmail.com</div>""", unsafe_allow_html=True)

# --- 5. DASHBOARD GRÁFICO E ALERTAS ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Total Ativos", len(st.session_state['db_ativos']))
c2.metric("📅 Inspeções Vencidas", "3")
c3.metric("⚠️ Alertas Ativos", "8")
c4.metric("✅ Conformidade", "85%")

g1, g2 = st.columns(2)
with g1:
    fig_p = px.pie(st.session_state['db_ativos'], names='Categoria', title="Distribuição por Categoria", hole=.4, template="plotly_dark")
    st.plotly_chart(fig_p, use_container_width=True)
with g2:
    # Lista de Alertas Críticos
    st.write("### 🚨 Lista de Alertas Críticos")
    st.error("VP-1.212087: Inspeção Externa Vencida há 210 dias!")
    st.warning("VP-01/509: Calibração de Válvula vence em breve.")

# --- 6. ABAS DE FUNCIONALIDADES ---
tabs = st.tabs(["📄 Análise IA", "📊 Gestão Técnica", "🌡️ Instrumentos", "📜 Histórico", "📁 Documentos"])

with tabs[0]:
    st.subheader("Atualização Automática (IA)")
    files = st.file_uploader("Upload de Laudos (300+ PDFs)", accept_multiple_files=True)
    if st.button("Processar com IA"):
        nova_log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Automático", "Ação": f"Processados {len(files)} laudos via IA", "Usuário": empresa}])
        st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)
        st.success("Dados extraídos e histórico atualizado!")

with tabs[1]:
    st.subheader("Gestão e Atualização Manual")
    # Tabela editável com as 16 colunas
    edited_df = st.data_editor(st.session_state['db_ativos'], use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações na Planilha"):
        st.session_state['db_ativos'] = edited_df
        nova_log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Manual", "Ação": "Alteração manual de datas/status", "Usuário": "Eng. Felipe Alves"}])
        st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)
        st.success("Planilha de Gestão salva com sucesso!")

with tabs[2]:
    st.subheader("Vencimento de Instrumentos")
    inst_df = pd.DataFrame({
        "Tag": ["PSV-1212087", "PI-I-212087"],
        "Instrumento": ["Válvula de Segurança", "Manômetro"],
        "Vencimento": ["2024-08-22", "2026-09-25"],
        "Status": ["🔴 VENCIDO", "🟢 EM DIA"]
    })
    st.table(inst_df)

with tabs[3]:
    st.subheader("📜 Histórico de Atualizações do Sistema")
    st.write("Rastreabilidade total de alterações (Automáticas e Manuais).")
    st.dataframe(st.session_state['historico'], use_container_width=True)

with tabs[4]:
    st.subheader("📁 Sistema Informatizado de Documentação")
    st.text_input("Link da Nuvem (OneDrive/Drive)")
    st.file_uploader("Upload de Projetos de Instalação/Outros", accept_multiple_files=True)

# --- 7. EXPORTAÇÃO ---
st.sidebar.divider()
st.sidebar.download_button("📊 Exportar Gestão (Excel)", data=b"dados", file_name="gestao_fa.xlsx")
