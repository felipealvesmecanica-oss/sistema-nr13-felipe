import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import urllib.parse

# --- 1. CONFIGURAÇÃO E TEMA DARK (FOCO EM UX INDUSTRIAL) ---
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

# --- 2. INICIALIZAÇÃO DO BANCO DE DADOS (PERSISTÊNCIA EM SESSÃO) ---
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
        "Dias p/ Vencimento": ["🔴 VENCIDO", "🔴 VENCIDO", "🔴 VENCIDO"],
        "Fabricante": ["Schulz", "Mebrafe", "Mebrafe"],
        "Modelo": ["Horizontal", "Horizontal", "Horizontal"],
        "Ano de Fabricação": [2021, 2011, 2011],
        "Revestimento": ["Pintura Epóxi", "Isolamento Térmico", "N/I"],
        "Status": ["🔴 Crítico", "🔴 Crítico", "🔴 Crítico"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP DO CLIENTE ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    with st.expander("Dados da Unidade", expanded=False):
        emp_nome = st.text_input("Empresa", "Natto Recife")
        setor_unidade = st.text_input("Setor", "Utilidades")
        resp_tecnico = st.text_input("Responsável Técnico", "Eng. Felipe Alves")
        email_alerta = st.text_input("E-mail para Alertas", "eng.alvescs@gmail.com")
    st.divider()
    st.caption("Felipe Alves Consultoria e Serviços")

# --- 4. CABEÇALHO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_nome}")
    st.caption(f"Status: Operacional | Unidade: {setor_unidade}")

with col_c:
    st.markdown("""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD EXECUTIVO (MÉTRICAS TÉCNICAS) ---
st.divider()
c1, c2, c3, c4 = st.columns(4)

c1.metric(label="📦 Ativos Cadastrados", value=len(st.session_state['db_ativos']), border=True)
c2.metric(label="🗓️ Inspeções a Vencer", value="18", delta="-3", delta_color="normal", border=True)
c3.metric(label="⚠️ Alertas Críticos", value="8", delta="+2", delta_color="inverse", border=True)
c4.metric(label="✅ Conformidade", value="88%", delta="3.5%", chart_data=[80, 85, 84, 88], border=True)

# --- 6. FUNCIONALIDADES (ABAS) ---
tabs = st.tabs(["📊 Gestão de Ativos", "📜 Histórico de Auditoria", "✉️ Oportunidades", "🌡️ Instrumentos"])

# ABA: GESTÃO TÉCNICA
with tabs[0]:
    st.subheader("Edição Técnica da Base de Ativos")
    df_antes = st.session_state['db_ativos'].copy()
    
    # Editor de dados completo (16 colunas)
    edited_df = st.data_editor(st.session_state['db_ativos'], use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações e Registrar no Histórico"):
        tipo_log, detalhe_log = "", ""
        
        # Lógica de Auditoria (Modificação, Adição ou Deleção)
        if len(edited_df) < len(df_antes):
            tipo_log, detalhe_log = "Deleção", f"Removido(s) {len(df_antes) - len(edited_df)} ativo(s)"
        elif len(edited_df) > len(df_antes):
            tipo_log, detalhe_log = "Adição", f"Adicionado(s) {len(edited_df) - len(df_antes)} novo(s) ativo(s)"
        elif not edited_df.equals(df_antes):
            tipo_log, detalhe_log = "Modificação", "Alteração técnica em dados de inspeção/status"
            
        if tipo_log:
            st.session_state['db_ativos'] = edited_df
            novo_reg = pd.DataFrame([{
                "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "Tipo": tipo_log, 
                "Ação": detalhe_log, 
                "Responsável": resp_tecnico
            }])
            st.session_state['historico'] = pd.concat([novo_reg, st.session_state['historico']], ignore_index=True)
            st.success(f"Sistema atualizado: {detalhe_log}")
        else:
            st.info("Nenhuma modificação detectada na planilha.")

# ABA: HISTÓRICO
with tabs[1]:
    st.subheader("📜 Rastreabilidade de Alterações")
    st.dataframe(st.session_state['historico'], use_container_width=True)

# ABA: OPORTUNIDADES (WHATSAPP E E-MAIL)
with tabs[2]:
    st.subheader("✉️ Notificação de Serviços")
    st.warning("⚠️ Detectado: Ativos operando fora do prazo legal. Risco iminente de multa.")
    
    # WhatsApp Direto
    zap_url = urllib.parse.quote(f"Olá Felipe, notei que na {emp_nome} existem ativos NR 13 vencidos. Preciso de um orçamento de regularização.")
    st.markdown(f'<a href="https://wa.me/5581997538656?text={zap_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 Solicitar Regularização via WhatsApp</button></a>', unsafe_allow_html=True)
    
    st.divider()
    # E-mail de Oportunidade
    email_body = f"""Prezado(a) {resp_tecnico},
    
Identificamos que a unidade {emp_nome} possui equipamentos com inspeções vencidas. 
A Felipe Alves Consultoria e Serviços pode realizar a regularização imediata.

Contato: (81) 99753-8656
Atenciosamente, Eng. Felipe Alves."""
    st.text_area("Prévia do E-mail Automático:", email_body, height=180)

# ABA: INSTRUMENTOS
with tabs[3]:
    st.subheader("🌡️ Monitoramento de Instrumentação")
    inst_data = pd.DataFrame({
        "Instrumento": ["Válvula de Segurança PSV-01", "Manômetro PI-10"],
        "TAG Ativo": ["VP-1.212087", "VP-1.212087"],
        "Vencimento": ["22/08/2024", "22/08/2024"],
        "Status": ["🔴 VENCIDO", "🔴 VENCIDO"]
    })
    st.table(inst_data)

# --- 7. EXPORTAÇÃO ---
st.sidebar.divider()
buffer = io.BytesIO()
st.session_state['db_ativos'].to_excel(buffer, index=False)
st.sidebar.download_button("📊 Baixar Planilha Geral (Excel)", data=buffer, file_name=f"Gestao_NR13_{emp_nome}.xlsx")
