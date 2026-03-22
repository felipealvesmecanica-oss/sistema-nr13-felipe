import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- 1. CONFIGURAÇÕES VISUAIS E IDENTIDADE DO SOFTWARE ---
st.set_page_config(page_title="Gestão NR 13 - Inteligência em Ativos", layout="wide")

# CSS Avançado: Marca d'água, Paleta de Cores e Estilo Técnico (UX/UI)
st.markdown("""
    <style>
    /* Fundo técnico e Marca d'água discreta */
    .reportview-container {
        background: url("https://www.transparenttextures.com/patterns/cubes.png");
    }
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        opacity: 0.1;
        z-index: -1;
        font-size: 50px;
        font-weight: bold;
        color: #003366; /* Azul FA */
    }
    /* Estilo do Cabeçalho de Contato */
    .contact-info {
        text-align: right;
        font-size: 14px;
        color: #555;
    }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. CABEÇALHO PROFISSIONAL E DADOS DE CONTATO ---
col_logo, col_contact = st.columns([2, 1])
with col_logo:
    st.title("🛡️ Portal de Gestão de Ativos NR 13")
    st.caption("Um sistema inteligente desenvolvido por Felipe Alves Consultoria e Serviços")

with col_contact:
    # Nome do cliente é inserido no Dashboard após o Setup
    st.markdown("""
    <div class="contact-info">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 (81) 9XXXX-XXXX<br>
        📸 @felipealves_consultoria<br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 3. ÁREA DE SETUP ÚNICO DO CLIENTE (Side Bar) ---
with st.sidebar.expander("⚙️ Configuração da Planta (Setup Único)", expanded=True):
    st.write("Preencha estes dados uma única vez para personalizar sua instância.")
    cliente_empresa = st.text_input("Nome da Empresa Cliente (Ex: Natto)", "Minha Empresa LTDA")
    cliente_setor = st.text_input("Setor/Planta")
    cliente_responsavel = st.text_input("Responsável pela Gestão")
    cliente_email = st.text_input("E-mail para Alertas Automáticos")
    st.divider()
    # O motor de IA é agnóstico e configurado pelo cliente
    cliente_api_ia = st.text_input("Motor de IA (Insira sua API Key - Gemini/OpenAI/etc.)", type="password")
    st.sidebar.caption("Sua API Key é usada apenas para o processamento de laudos desta sessão.")

# --- 4. DATA LOGIC (BASEADO EM 21/03/2026) ---
hoje = datetime(2026, 3, 21)

# --- 5. DASHBOARD EXECUTIVO (MOBILE & WEB RESPONSIVO) ---
st.divider()
st.header(f"📊 Dashboard Técnico - {cliente_empresa}")

# Cards de Resumo (UX/UI de alto impacto)
c1, c2, c3, c4 = st.columns(4)
# Ícone representando o total de equipamentos
c1.metric("Total Ativos", "345", help="Ícone representando o total de equipamentos")
c2.metric("Inspeções a Vencer (90 dias)", "18")
c3.metric("⚠️ Alertas Ativos (Vencidos)", "8", delta_color="inverse")
c4.metric("Conformidade NR 13 (%)", "85%")

# --- 6. NAVEGAÇÃO POR ABAS CONFORME MOCKUP ---
tab_inventario, tab_recomenda, tab_instru, tab_nuvem = st.tabs([
    "📋 Inventário Técnico", 
    "🔧 Recomendações (Pano de Ação)", 
    "🌡️ Instrumentos", 
    "☁️ Arquivos e Nuvem"
])

# --- ABA: INVENTÁRIO (TABELA TÉCNICA COM FILTROS) ---
with tab_inventario:
    st.write("### Base de Dados Informatizada")
    
    # Exemplo de dados baseados no seu arquivo RI-20231235 e CSVs (Sincronizado com 2026)
    dados = {
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"],
        "Tipo de Equipamento": ["Vaso de Pressão Schulz", "Vaso de Pressão Mebrafe", "Vaso de Pressão Mebrafe"],
        "Local de Instalação": ["Oficina", "Sala de Máquinas", "Sala de Máquinas"],
        "Categoria NR 13": ["V", "II", "III"], # Conforme dados do relatório
        "Fluído": ["Ar Comprimido", "Amônia", "Amônia"],
        "Classe de Fluído": ["C", "A", "A"],
        "Próxima Externa": ["2025-08-24", "2025-04-18", "2025-08-27"], # Baseado nos prazos do relatório
        "Próxima Interna": ["2027-08-14", "2027-04-08", "2027-08-17"],
        "Dias p/ Vencimento Externa": ["🔴 VENCIDO (-210 dias)", "🔴 VENCIDO (-337 dias)", "🔴 VENCIDO (-206 dias)"],
        "Dias p/ Vencimento Interna": ["75 dias", "45 dias", "70 dias"],
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"],
        "Modelo": ["Model X", "Model B1", "Model B2"],
        "Ano de Fabricação": [2021, 2011, 2011],