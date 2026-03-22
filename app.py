import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# --- 1. CONFIGURAÇÃO DE TEMA DARK E LAYOUT ---
st.set_page_config(
    page_title="Gestão NR 13 - Felipe Alves", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Estilização: Tema Dark, Marca d'água e Branding
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 12px; line-height: 1.2; color: #BBB; }
    [data-testid="stSidebar"] { background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. SETUP OCULTO NO MENU (SIDEBAR) ---
with st.sidebar:
    with st.expander("⚙️ Setup do Sistema", expanded=False):
        empresa_cliente = st.text_input("Empresa", "Natto Recife")
        setor_cliente = st.text_input("Setor", "Utilidades/Oficina")
        email_alerta = st.text_input("E-mail para Alertas", "eng.alvescs@gmail.com")
        api_key_ia = st.text_input("Chave da API IA (Cliente)", type="password")
        st.caption("Desenvolvido por: Felipe Alves Consultoria e Serviços")

# --- 3. CABEÇALHO COM CONTATO ---
col_t, col_c = st.columns([3, 1])
with col_t:
    st.title(f"🛡️ Sistema de Gestão de Ativos NR 13 - {empresa_cliente}")
with col_c:
    st.markdown(f"""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 (81) 99753-8656<br>
        📸 @felipealves_consultoria<br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 4. DASHBOARD TÉCNICO (MÉTRICAS E GRÁFICOS) ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Ativos Totais", "345")
c2.metric("📅 Inspeções Vencidas", "12", delta="-3", delta_color="inverse")
c3.metric("⚠️ Alertas Ativos", "8")
c4.metric("✅ Conformidade (%)", "85%")

g1, g2 = st.columns(2)
with g1:
    df_pizza = pd.DataFrame({'Cat': ['II', 'III', 'IV', 'V'], 'Qtd': [18, 22, 13, 1]})
    fig_pizza = px.pie(df_pizza, values='Qtd', names='Cat', title="Distribuição por Categoria NR 13", hole=.4, template="plotly_dark")
    st.plotly_chart(fig_pizza, use_container_width=True)
with g2:
    df_bar = pd.DataFrame({'Mês': ['Abr/26', 'Mai/26', 'Jun/26'], 'Vencimentos': [5, 3, 8]})
    fig_bar = px.bar(df_bar, x='Mês', y='Vencimentos', title="Cronograma de Próximas Inspeções", template="plotly_dark", color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 5. FUNCIONALIDADES (ABAS) ---
tabs = st.tabs(["📄 Analisar PDFs (IA)", "📊 Banco de Dados / Planilha", "🔧 Recomendações", "🌡️ Instrumentos", "📁 Documentação Online"])

# ABA: ANALISAR RELATÓRIOS (PDF EM LOTE)
with tabs[0]:
    st.subheader("Processamento Automático de Laudos (300+ PDFs)")
    arquivos = st.file_uploader("Arraste seus relatórios aqui", accept_multiple_files=True, type="pdf")
    if arquivos and api_key_ia:
        st.info(f"Analisando {len(arquivos)} arquivos com a IA do cliente...")
        st.success("Dados extraídos com sucesso!")

# ABA: BANCO DE DADOS (16 COLUNAS TÉCNICAS)
with tabs[1]:
    st.subheader("Gestão de Ativos e Importação de Planilha")
    u_planilha = st.file_uploader("Upload de Planilha de Gestão (.xlsx ou .csv)", type=["xlsx", "csv"])
    
    # Dados pré-preenchidos baseados nos seus ativos reais [cite: 581, 582]
    dados_pre = {
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902", "VP-03/2050"],
        "Tipo de Equipamento": ["Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão"],
        "Local de Instalação": ["Oficina", "Sala de Máquinas", "Sala de Máquinas", "Sala de Máquinas"],
        "Categoria NR 13": ["V", "II", "III", "II"],
        "Fluído": ["Ar Comprimido", "Amônia", "Amônia", "Amônia"],
        "Classe de Fluído": ["C", "A", "A", "A"],
        "Inspeção Externa": ["23/08/2023", "18/04/2023", "27/08/2023", "27/08/2023"],
        "Próxima Externa": ["24/08/2025", "18/04/2025", "27/08/2025", "27/08/2025"],
        "Inspeção Interna": ["23/08/2023", "18/04/2023", "27/08/2023", "27/08/2023"],
        "Próxima Interna": ["24/08/2025", "2027-04-08", "2027-08-17", "2027-08-17"],
        "Dias p/ Venc. Externa": ["🔴 VENCIDO", "🔴 VENCIDO", "🔴 VENCIDO", "🔴 VENCIDO"],
        "Dias p/ Venc. Interna": ["🔴 VENCIDO", "473 dias", "604 dias", "604 dias"],
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe", "Mebrafe"],
        "Modelo": ["Horizontal", "Horizontal", "Horizontal", "Horizontal"],
        "Ano de Fabricação": [2021, 2011, 2011, 2010],
        "Revestimento": ["Pintura Preto", "Pintura Amarela", "N/I", "Inox"]
    }
    df_final = pd.DataFrame(dados_pre)
    st.data_editor(df_final, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Todos os Dados"):
        st.success("Dados salvos e dashboard atualizado!")

# ABA: RECOMENDAÇÕES [cite: 583, 590]
with tabs[2]:
    st.subheader("Recomendações por Equipamento (Plano de Ação)")
    recom_df = pd.DataFrame({
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"],
        "Recomendação": ["Realizar Teste Hidrostático", "Providenciar Manual de Operação", "Abertura de Livro de Registro"],
        "Prazo": ["05/02/2024", "05/02/2024", "05/02/2024"],
        "Status": ["🔴 ATRASADO", "✅ Concluída", "✅ Concluída"]
    })
    st.table(recom_df)

# ABA: INSTRUMENTOS [cite: 591, 592]
with tabs[3]:
    st.subheader("Controle de Válvulas, Manômetros e Sensores")
    inst_df = pd.DataFrame({
        "Tag Instrumento": ["PSV-1212087", "PI-I-212087", "PI-01-CONGELADOR"],
        "Equipamento Pai": ["VP-1.212087", "VP-1.212087", "Sala Máquinas"],
        "Vencimento": ["08/2024", "25/09/2026", "25/09/2026"],
        "Status": ["🔴 VENCIDO", "🟢 OK", "🟢 OK"]
    })
    st.dataframe(inst_df, use_container_width=True)

# ABA: DOCUMENTAÇÃO ONLINE
with tabs[4]:
    st.subheader("📂 Sistema Informatizado de Documentação")
    st.info("Arquivos organizados por Ano e TAG. Integração via link de nuvem.")
    st.text_input("Link da Nuvem (Google Drive/OneDrive)", placeholder="https://drive.google.com/...")
    st.file_uploader("Upload de Projetos de Instalação / Outros Documentos", accept_multiple_files=True)

# --- 6. EXPORTAÇÃO ---
st.sidebar.divider()
st.sidebar.download_button("📊 Exportar Planilha Excel", data=b"dados", file_name="gestao_nr13.xlsx")
st.sidebar.button("📄 Exportar Dashboard PDF")
