import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="Gestão NR 13 - F.A Engenharia", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.05; z-index: -1; font-size: 40px; font-weight: bold; color: #FFFFFF; }
    .contact-card { text-align: right; font-size: 13px; line-height: 1.4; color: #00D1FF; border-left: 2px solid #00D1FF; padding-left: 10px; }
    </style>
    <div class="watermark">Felipe Alves Consultoria e Serviços</div>
    """, unsafe_allow_html=True)

# --- 2. PERSISTÊNCIA DE DADOS ---
if 'db_ativos' not in st.session_state:
    st.session_state['db_ativos'] = pd.DataFrame({
        "Tag": ["VP-1.212087", "VP-01/509", "VP-02/1902"],
        "Tipo": ["Vaso de Pressão", "Vaso de Pressão", "Vaso de Pressão"],
        "Categoria": ["V", "II", "III"],
        "Prox. Externa": ["2025-08-24", "2025-04-18", "2025-08-27"],
        "Status": ["🔴 Crítico", "🔴 Crítico", "🔴 Crítico"]
    })

if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Data/Hora", "Tipo", "Ação", "Responsável"])

# --- 3. SIDEBAR: SETUP ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações de Planta")
    with st.expander("Dados da Empresa", expanded=False):
        emp_n = st.text_input("Empresa", "Natto Recife")
        setor_cl = st.text_input("Setor", "Utilidades")
        resp_cl = st.text_input("Responsável", "Eng. Felipe Alves")
        email_dest = st.text_input("E-mail para Alertas", "eng.alvescs@gmail.com")

# --- 4. CABEÇALHO COM CONTATO DESTACADO ---
col_t, col_c = st.columns([2.5, 1.5])
with col_t:
    st.title(f"🛡️ Gestão NR 13 - {emp_n}")
    st.caption(f"Felipe Alves Consultoria e Serviços | {setor_cl}")

with col_c:
    st.markdown(f"""
    <div class="contact-card">
        <b>Felipe Alves Consultoria e Serviços</b><br>
        📍 Engenharia e Segurança NR 13<br>
        📞 <b>(81) 99753-8656</b><br>
        📧 eng.alvescs@gmail.com
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD E OPORTUNIDADES ---
st.divider()
g1, g2 = st.columns([2, 1])
with g1:
    fig = px.pie(st.session_state['db_ativos'], names='Status', title="Conformidade da Planta", hole=.4, template="plotly_dark", color_discrete_sequence=['#FF4B4B', '#00D1FF'])
    st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("💡 Oportunidades")
    st.warning("⚠️ Detectado: 3 ativos com inspeção vencida. Risco de multa e interdição.")
    st.info("💡 Sugestão: Realizar teste hidrostático e calibração de válvulas no próximo parada.")

# --- 6. FUNCIONALIDADES ---
tabs = st.tabs(["📊 Gestão e Edição", "📜 Histórico de Auditoria", "✉️ Solicitar Serviço / Alerta"])

with tabs[0]:
    st.subheader("Edição Manual da Base de Dados")
    df_temp = st.session_state['db_ativos'].copy()
    edited_df = st.data_editor(st.session_state['db_ativos'], use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações"):
        # Lógica para detectar o que mudou
        if not edited_df.equals(df_temp):
            st.session_state['db_ativos'] = edited_df
            nova_log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "Manual", "Ação": "Atualização/Deleção de Ativos", "Responsável": resp_cl}])
            st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)
            st.success("Alterações salvas e registradas no histórico!")
        else:
            st.info("Nenhuma modificação detectada.")

with tabs[1]:
    st.subheader("📜 Histórico de Atualizações")
    st.dataframe(st.session_state['historico'], use_container_width=True)

with tabs[2]:
    st.subheader("✉️ Enviar Relatório de Oportunidades")
    
    # Template de E-mail Atrativo
    email_template = f"""
    Assunto: 🛡️ Oportunidade de Conformidade Detectada - {emp_n}
    
    Prezado(a) {resp_cl},
    
    O sistema de gestão da Felipe Alves Consultoria e Serviços identificou que sua planta possui equipamentos operando fora dos requisitos da NR 13.
    
    🚨 ITENS CRÍTICOS:
    - Vencimentos detectados em equipamentos Categoria {st.session_state['db_ativos']['Categoria'].iloc[0]}.
    - Risco de multas e paradas não programadas.
    
    ✅ SOLUÇÃO IMEDIATA:
    Podemos realizar a regularização técnica, testes e laudos necessários para garantir a segurança da sua operação.
    
    Clique no link abaixo para aprovar o plano de ação ou fale diretamente conosco:
    📞 Telefone/WhatsApp: (81) 99753-8656
    
    Atenciosamente,
    Eng. Felipe Alves
    """
    st.text_area("Mensagem Personalizada:", email_template, height=300)
    
    if st.button("🚀 Disparar E-mail de Serviço"):
        st.success(f"E-mail de oportunidade enviado para {email_dest}!")
        nova_log = pd.DataFrame([{"Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "Tipo": "E-mail", "Ação": "Envio de Proposta de Serviço", "Responsável": "Sistema"}])
        st.session_state['historico'] = pd.concat([nova_log, st.session_state['historico']], ignore_index=True)
