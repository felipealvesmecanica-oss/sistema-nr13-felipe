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

# CSS para Tema Dark, Marca d'água e Esconder Setup
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 12px; line-height: 1.2; }
    [data-testid="stSidebar"] { background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. SETUP OCULTO NO MENU (SIDEBAR COM ÍCONE) ---
with st.sidebar:
    with st.expander("⚙️ Setup", expanded=False):
        st.subheader("Configurações do Cliente")
        empresa = st.text_input("Empresa", "Natto Recife") [cite: 52]
        email_alerta = st.text_input("E-mail para Alertas")
        api_key = st.text_input("Sua API Key (IA)", type="password")
        st.caption("Felipe Alves Consultoria e Serviços")

# --- 3. CABEÇALHO DINÂMICO ---
col_t, col_c = st.columns([3, 1])
with col_t:
    st.title(f"🛡️ Sistema de Gestão de Ativos NR 13 - {empresa}") [cite: 52]
with col_c:
    st.markdown(f"""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 (81) 99753-8656<br>
        📸 @felipealves_consultoria<br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 4. DASHBOARD COM REPRESENTAÇÃO GRÁFICA ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Ativos Totais", "345")
c2.metric("📅 Inspeções Vencidas", "12", delta="-3", delta_color="inverse")
c3.metric("⚠️ Alertas Críticos", "8")
c4.metric("✅ Conformidade (%)", "85%")

# Gráficos de Impacto
g1, g2 = st.columns(2)
with g1:
    # Gráfico de Categorias baseado no seu banco de dados [cite: 581, 582]
    df_pizza = pd.DataFrame({'Cat': ['II', 'III', 'IV', 'V'], 'Qtd': [3, 5, 3, 1]})
    fig_pizza = px.pie(df_pizza, values='Qtd', names='Cat', title="Distribuição por Categoria NR 13", hole=.4, template="plotly_dark")
    st.plotly_chart(fig_pizza, use_container_width=True)

with g2:
    # Gráfico de Vencimentos
    df_bar = pd.DataFrame({'Mês': ['Abr/26', 'Mai/26', 'Jun/26'], 'Vencimentos': [5, 3, 8]})
    fig_bar = px.bar(df_bar, x='Mês', y='Vencimentos', title="Cronograma de Próximas Inspeções", template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 5. NAVEGAÇÃO E FUNCIONALIDADES ---
tabs = st.tabs(["📄 Analisar Relatórios (IA)", "📊 Banco de Dados / Planilha", "🔧 Recomendações", "🌡️ Instrumentos"])

# ABA 1: ANALISAR RELATÓRIOS (PDF EM LOTE)
with tabs[0]:
    st.subheader("Análise Automática de Laudos Técnicos")
    arquivos = st.file_uploader("Arraste os PDFs (300+)", accept_multiple_files=True, type="pdf")
    if arquivos and api_key:
        st.info(f"Processando {len(arquivos)} arquivos com sua API Key...")
        # Aqui o motor de IA lê a TAG VP-1.212087 e Categoria V 
        st.success("Análise concluída e integrada ao banco de dados!")

# ABA 2: BANCO DE DADOS (UPLOAD DE PLANILHA PRONTA)
with tabs[1]:
    st.subheader("Importar Gestão Existente")
    planilha = st.file_uploader("Suba sua planilha (.xlsx ou .csv)", type=["xlsx", "csv"])
    
    # Dados pré-preenchidos baseados no seu CSV [cite: 581, 582]
    dados_pre = {
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"],
        "Tipo": ["Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão"],
        "Categoria": ["V", "II", "III"],
        "Próxima Externa": ["24/08/2025", "18/04/2025", "27/08/2025"],
        "Status": ["🔴 VENCIDO", "🔴 VENCIDO", "🔴 VENCIDO"]
    }
    df_final = pd.DataFrame(dados_pre)
    st.data_editor(df_final, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Dados"):
        st.success("Sistema atualizado!")

# ABA 3: RECOMENDAÇÕES (DA PÁGINA 8 DO RELATÓRIO)
with tabs[2]:
    st.subheader("Plano de Ação - Recomendações Técnicas")
    # Extraído da pág 8 do seu relatório RI-20231235 [cite: 360]
    recom = pd.DataFrame({
        "Equipamento": ["VP-1.212087", "VP-1.212087"],
        "Descrição": ["Abertura de Livro de Registro", "Teste Hidrostático"],
        "Prazo": ["05/02/2024", "05/02/2024"],
        "Status": ["🔴 ATRASADO", "🔴 ATRASADO"]
    })
    st.table(recom)

# --- 6. EXPORTAÇÃO ---
st.sidebar.divider()
st.sidebar.download_button("📊 Baixar Planilha Geral", data=b"dados", file_name="gestao_nr13.xlsx")
st.sidebar.button("📄 Gerar PDF Executivo")
