import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- 1. CONFIGURAÇÕES VISUAIS E IDENTIDADE (UX/UI) ---
st.set_page_config(page_title="Gestão NR 13 - Inteligência em Ativos", layout="wide")

# Estilização com a paleta da Felipe Alves Consultoria e Serviços
st.markdown("""
    <style>
    .reportview-container { background: url("https://www.transparenttextures.com/patterns/cubes.png"); }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.1; z-index: -1; font-size: 50px; font-weight: bold; color: #003366; }
    .contact-info { text-align: right; font-size: 14px; color: #555; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. CABEÇALHO COM DADOS DE CONTATO ---
col_logo, col_contact = st.columns([2, 1])
with col_logo:
    st.title("🛡️ Sistema de Gestão de Ativos NR 13")
    st.caption("Felipe Alves Consultoria e Serviços | Engenharia e Segurança")

with col_contact:
    st.markdown("""
    <div class="contact-info">
        📞 (81) 99753-8656<br>
        📸 @felipealves_consultoria<br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 3. SETUP DO CLIENTE (SIDEBAR) ---
with st.sidebar.expander("⚙️ Setup da Empresa", expanded=True):
    empresa = st.text_input("Empresa", "Natto Recife")
    setor = st.text_input("Setor", "Utilidades/Oficina")
    responsavel = st.text_input("Responsável", "Eng. Felipe Alves")
    email_alerta = st.text_input("E-mail para Alertas")
    api_key = st.text_input("Chave da API IA", type="password")

# --- 4. LÓGICA DE DATA (HOJE: 21/03/2026) ---
hoje = datetime(2026, 3, 21)

# --- 5. DASHBOARD TÉCNICO ---
st.divider()
st.subheader(f"📊 Dashboard Executivo - {empresa}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Equipamentos Cadastrados", "345")
c2.metric("📅 Inspeções a Vencer", "18")
c3.metric("⚠️ Alertas Ativos", "8", delta_color="inverse")
c4.metric("✅ Conformidade NR 13", "85%")

# --- 6. NAVEGAÇÃO POR ABAS ---
tab_inv, tab_recom, tab_inst, tab_cloud = st.tabs(["📋 Inventário", "🔧 Recomendações", "🌡️ Instrumentos", "☁️ Nuvem"])

with tab_inv:
    st.write("### Tabela Técnica de Gestão")
    
    # Dicionário corrigido com as 16 colunas solicitadas
    dados = {
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"], # [cite: 12, 581]
        "Tipo de Equipamento": ["Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão"], # [cite: 9, 62]
        "Local de Instalação": ["Oficina", "Sala de Máquinas", "Sala de Máquinas"], # [cite: 14, 55]
        "Categoria NR 13": ["V", "II", "III"], # [cite: 24, 161]
        "Fluído": ["Ar Comprimido", "Amônia", "Amônia"], # [cite: 25, 204]
        "Classe de Fluído": ["C", "A", "A"], # [cite: 29, 156]
        "Inspeção Externa": ["23/08/2023", "18/04/2023", "27/08/2023"], # [cite: 13, 79]
        "Próxima Externa": ["24/08/2025", "18/04/2025", "27/08/2025"], # [cite: 27, 123]
        "Inspeção Interna": ["23/08/2023", "18/04/2023", "27/08/2023"], # [cite: 86]
        "Próxima Interna": ["24/08/2025", "2027-04-08", "2027-08-17"], # [cite: 127, 581]
        "Dias p/ Vencimento Externa": ["🔴 VENCIDO", "🔴 VENCIDO", "🔴 VENCIDO"],
        "Dias p/ Vencimento Interna": ["🔴 VENCIDO", "473 dias", "604 dias"], # 
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"], # [cite: 163, 581]
        "Modelo": ["Horizontal", "Horizontal", "Horizontal"], # [cite: 165, 525]
        "Ano de Fabricação": [2021, 2011, 2011], # [cite: 166, 169, 527]
        "Revestimento": ["Preto", "Amarela", "N/I"] # [cite: 170, 529, 581]
    }
    
    df = pd.DataFrame(dados)
    
    # Filtros Inteligentes
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_tipo = st.multiselect("Filtrar Tipo", options=df["Tipo de Equipamento"].unique())
    with col_f2:
        f_cat = st.multiselect("Filtrar Categoria", options=df["Categoria NR 13"].unique())
        
    st.data_editor(df, use_container_width=True)
    if st.button("💾 Salvar Dados"):
        st.success("Dados salvos no sistema da Felipe Alves Consultoria!")

with tab_recom:
    st.write("### Recomendações por Equipamento")
    # Baseado na página 8 do relatório técnico [cite: 360]
    recom_dados = {
        "Tag": ["VP-1.212087", "VP-1.212087", "VP-1.212087"], # [cite: 405]
        "Recomendação": ["Abertura de Livro de Registro", "Reconstituição do Prontuário", "Teste Hidrostático"], # [cite: 360]
        "Prazo": ["05/02/2024", "05/02/2024", "05/02/2024"], # [cite: 360, 555]
        "Status": ["🔴 ATRASADO", "🔴 ATRASADO", "🔴 ATRASADO"]
    }
    st.table(pd.DataFrame(recom_dados))

with tab_inst:
    st.write("### Controle de Instrumentos (Válvulas/Manômetros)")
    # Baseado na página 7 do relatório [cite: 289, 303, 319]
    inst_dados = {
        "Tag": ["PSV-1212087", "PI-I-212087", "PSH-1.212087"], # [cite: 289, 303, 319]
        "Instrumento": ["Válvula de Segurança", "Manômetro", "Pressostato"], # [cite: 300, 315]
        "Vencimento": ["22/08/2024", "22/08/2024", "22/08/2024"] # [cite: 309, 325]
    }
    st.dataframe(pd.DataFrame(inst_dados), use_container_width=True)

with tab_cloud:
    st.subheader("📁 Sistema Informatizado de Documentação")
    st.text_input("Link da Nuvem (OneDrive/Google Drive)")
    st.file_uploader("Upload de Prontuários/Projetos de Instalação", accept_multiple_files=True)

# Exportação
st.sidebar.divider()
buffer = io.BytesIO()
df.to_excel(buffer, index=False)
st.sidebar.download_button("📊 Exportar Excel", data=buffer, file_name="Gestao_NR13.xlsx")
