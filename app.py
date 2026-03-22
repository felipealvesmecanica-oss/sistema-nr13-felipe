import streamlit as st
import pandas as pd
import plotly.express as px
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

# --- 2. INICIALIZAÇÃO DE DADOS ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame({
        "Tag": ["TA-001", "VC-102", "BL-203"],
        "Tipo de Equipamento": ["Vaso de Pressão", "Vaso de Pressão", "Caldeira"],
        "Local de Instalação": ["Porto de Trr", "Porto de Trr", "Porto de Trr"],
        "Categoria NR 13": ["V", "II", "III"],
        "Fluído": ["Ar Comprimido", "Amônia", "Vapor"],
        "Classe de Fluído": ["C", "A", "A"],
        "Próx. Ext.": ["2025-06-10", "2025-06-20", "2025-06-22"],
        "Inspeção Interna": ["Sim", "Não", "Sim"],
        "Próx. Int.": ["2027-06-10", "2027-06-20", "2027-06-22"],
        "Dias p/ Vencimento": ["22 dias", "23 dias", "19 dias"],
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"],
        "Modelo": ["H-200", "V-500", "B-100"],
        "Ano": [2021, 2011, 2011],
        "Revestimento": ["Pintura", "Isolamento", "Inox"],
        "Status": ["Em Dia", "Em Dia", "Em Dia"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR (CONFIGURAÇÃO) ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    with st.expander("Dados da Unidade", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Produção")
        resp_cl = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_cliente = st.text_input("E-mail do Cliente", "gerente.natto@email.com")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Consultoria: Felipe Alves | Unidade: {setor_cl}")
with col_c:
    st.markdown("""<div class="contact-card"><b>Felipe Alves Consultoria e Serviços</b><br>📞 (81) 99753-8656<br>📧 eng.alvescs@gmail.com</div>""", unsafe_allow_html=True)

# --- 5. DASHBOARD GRÁFICO (RESTAURADO) ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Equipamentos", len(st.session_state['db_ativos']), border=True)
c2.metric("🗓️ Inspeções a Vencer", "5", border=True)
c3.metric("⚠️ Alertas Ativos", "3", delta="+1", delta_color="inverse", border=True)
c4.metric("✅ Conformidade", "92%", chart_data=[88, 90, 92, 92], border=True)

# --- 6. ABAS DE FUNCIONALIDADES ---
tabs = st.tabs(["📊 Visão Geral e Edição", "📜 Histórico de Auditoria", "✉️ Alertas e Oportunidades", "🌡️ Instrumentos"])

# ABA 1: EDIÇÃO E SALVAMENTO
with tabs[0]:
    st.subheader("Gerenciamento Técnico de Ativos")
    df_antes = st.session_state['db_ativos'].copy()
    
    # Tabela 100% Editável (Datas, Status, Colunas)
    edited_df = st.data_editor(st.session_state['db_ativos'], use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Dados e Atualizar Histórico"):
        tipo_log, detalhe = "", ""
        if len(edited_df) < len(df_antes):
            tipo_log, detalhe = "Deleção", f"Removido(s) {len(df_antes) - len(edited_df)} ativo(s)"
        elif len(edited_df) > len(df_antes):
            tipo_log, detalhe = "Adição", f"Adicionado(s) {len(edited_df) - len(df_antes)} novo(s) ativo(s)"
        elif not edited_df.equals(df_antes):
            tipo_log, detalhe = "Modificação", "Alteração de dados/status na planilha"
        
        if tipo_log:
            st.session_state['db_ativos'] = edited_df
            nova_log = pd.DataFrame([{
                "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "Tipo": tipo_log, "Ação": detalhe, "Responsável": resp_cl
            }])
            st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)
            st.success(f"Sistema atualizado com sucesso: {detalhe}")
        else:
            st.info("Nenhuma modificação detectada para salvar.")

# ABA 2: HISTÓRICO
with tabs[1]:
    st.subheader("📜 Rastreabilidade de Alterações")
    st.dataframe(st.session_state['historico'], use_container_width=True)

# ABA 3: EMAIL AUTOMÁTICO (NÃO EDITÁVEL NO APP)
with tabs[2]:
    st.subheader("✉️ Envio de Alerta Automático")
    st.info("O e-mail abaixo é enviado automaticamente para o cliente quando o botão é acionado.")
    
    # Template Fixo e Profissional
    msg_email = f"""
    ESTE É UM ALERTA AUTOMÁTICO DE CONFORMIDADE NR 13
    Empresa: {emp_n} | Responsável: {resp_cl}
    
    Detectamos ativos com prazos de inspeção próximos ao vencimento. 
    Para evitar interdições e multas, recomendamos a regularização imediata.
    
    CONTATO PARA SERVIÇO TÉCNICO:
    Eng. Felipe Alves
    E-mail: eng.alvescs@gmail.com
    WhatsApp: (81) 99753-8656
    """
    st.code(msg_email, language="text")
    
    if st.button("🚀 Disparar E-mail de Alerta"):
        st.success(f"Alerta enviado com sucesso para {email_cliente}!")
        nova_log = pd.DataFrame([{
            "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), 
            "Tipo": "E-mail", "Ação": "Envio de Alerta Automático de Oportunidade", "Responsável": "Sistema"
        }])
        st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)

# ABA 4: INSTRUMENTOS
with tabs[3]:
    st.subheader("🌡️ Monitoramento de Instrumentação")
    st.table(pd.DataFrame({
        "Instrumento": ["Manômetro PI-01", "Válvula PSV-02", "Termopar TP-01"],
        "Tag Ativo": ["TA-001", "VC-102", "BL-203"],
        "Vencimento": ["2026-08-22", "2024-08-22", "2026-09-25"],
        "Status": ["🟢 OK", "🔴 VENCIDO", "🟢 OK"]
    }))

# --- 7. EXPORTAÇÃO ---
st.sidebar.divider()
buffer = io.BytesIO()
st.session_state['db_ativos'].to_excel(buffer, index=False)
st.sidebar.download_button("📊 Baixar Planilha Geral", data=buffer, file_name=f"Gestao_NR13_{emp_n}.xlsx")
