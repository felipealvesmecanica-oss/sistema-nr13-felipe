import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import io

# --- 1. CONFIGURAÇÃO E TEMA DARK (FOCO EM AUDITORIA) ---
st.set_page_config(
    page_title="Gestão NR 13 - F.A Engenharia", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Estilização Técnica (Branding Felipe Alves Consultoria e Serviços)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    div[data-testid="metric-container"] { border: 1px solid #30363D; padding: 15px; border-radius: 10px; background-color: #161B22; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE DADOS (BANCO DE DADOS EM SESSÃO) ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame([
        {"Tag": "TA-001", "Tipo": "Vaso de Pressão", "Local": "Setor A", "Categoria": "V", "Fluido": "Ar Comprimido", "Classe": "C", "Status": "Em Dia", "Prox_Insp": "2025-06-10"},
        {"Tag": "VC-102", "Tipo": "Vaso de Pressão", "Local": "Setor B", "Categoria": "II", "Fluido": "Amônia", "Classe": "A", "Status": "Vencido", "Prox_Insp": "2025-06-20"}
    ])

if 'db_instrumentos' not in st.session_state:
    st.session_state['db_instrumentos'] = pd.DataFrame([
        {"Tag_Inst": "PSV-01", "Equipamento": "TA-001", "Tipo": "Válvula", "Vencimento": "2024-08-22", "Status": "Vencido"}
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
        email_cliente = st.text_input("E-mail Destinatário", "cliente@email.com")
    
    with st.expander("Servidor de E-mail (SMTP)", expanded=False):
        smtp_user = st.text_input("Seu E-mail (Gmail)", "eng.alvescs@gmail.com")
        smtp_pass = st.text_input("Senha de Aplicativo Google", type="password")

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

# --- 5. DASHBOARD GRÁFICO (RESTAURADO E CORRIGIDO) ---
st.divider()
m1, m2, m3, m4 = st.columns(4)

# Correção da linha 72 (parênteses fechados corretamente)
m1.metric("📦 Equipamentos", len(st.session_state['db_ativos']), border=True)
m2.metric("🗓️ Vencidos", len(st.session_state['db_ativos'][st.session_state['db_ativos']['Status'] == "Vencido"]), border=True)
m3.metric("🌡️ Instrumentos", len(st.session_state['db_instrumentos']), border=True)
m4.metric("✅ Conformidade", "92%", chart_data=[88, 90, 92, 92], border=True)

g1, g2 = st.columns(2)
with g1:
    fig_p = px.pie(st.session_state['db_ativos'], names='Status', title="Conformidade de Ativos", hole=.4, template="plotly_dark")
    st.plotly_chart(fig_p, use_container_width=True)
with g2:
    fig_i = px.pie(st.session_state['db_instrumentos'], names='Status', title="Status de Instrumentos", hole=.4, template="plotly_dark", color_discrete_sequence=['#EF553B', '#00CC96'])
    st.plotly_chart(fig_i, use_container_width=True)

# --- 6. FUNCIONALIDADES ---
tabs = st.tabs(["📊 Gestão de Ativos", "🌡️ Instrumentos", "📜 Histórico", "✉️ Enviar Alertas"])

# Configuração de Dropdowns (Seleção) para impedir erros de digitação
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
    df_inst_prev = st.session_state['db_instrumentos'].copy()
    edited_inst = st.data_editor(st.session_state['db_instrumentos'], column_config=config_drop, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações Instrumentos"):
        if not edited_inst.equals(df_inst_prev):
            st.session_state['db_instrumentos'] = edited_inst
            log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Manual", "Ação": "Atualização em Instrumentos", "Responsável": resp_cl}])
            st.session_state['historico'] = pd.concat([log, st.session_state['historico']], ignore_index=True)
            st.success("Instrumentos atualizados!")

with tabs[2]:
    st.subheader("📜 Histórico de Auditoria (Rastreabilidade Total)")
    st.dataframe(st.session_state['historico'], use_container_width=True)

with tabs[3]:
    st.subheader("✉️ Envio de Alertas Automáticos")
    if st.button("🚀 Disparar E-mail de Oportunidade"):
        if smtp_user and smtp_pass:
            try:
                msg_body = f"""Prezado Cliente,
                
A Felipe Alves Consultoria e Serviços identificou itens de não-conformidade na unidade {emp_n}. 
Existem equipamentos operando fora do prazo normativo da NR 13.

Para regularização imediata:
📞 WhatsApp: (81) 99753-8656
📧 E-mail: eng.alvescs@gmail.com

Atenciosamente, 
Eng. Felipe Alves"""
                
                msg = MIMEText(msg_body)
                msg['Subject'] = f"🛡️ Alerta de Segurança NR 13 - {emp_n}"
                msg['From'] = smtp_user
                msg['To'] = email_cliente
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(smtp_user, smtp_pass)
                    server.sendmail(smtp_user, email_cliente, msg.as_string())
                
                log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "E-mail", "Ação": "Envio de Alerta de Oportunidade", "Responsável": "Sistema"}])
                st.session_state['historico'] = pd.concat([log, st.session_state['historico']], ignore_index=True)
                st.success(f"E-mail enviado para {email_cliente}!")
            except Exception as e:
                st.error(f"Erro no envio: {e}")
        else:
            st.warning("Configure o E-mail e a Senha de Aplicativo no menu lateral para enviar alertas.")

# --- 7. EXPORTAÇÃO ---
st.sidebar.divider()
buf = io.BytesIO()
st.session_state['db_ativos'].to_excel(buf, index=False)
st.sidebar.download_button("📊 Baixar Excel Geral", data=buf, file_name=f"Gestao_NR13_{emp_n}.xlsx")
