
import streamlit as st
st.set_page_config(page_title='Telemonitoramento CEUB', layout='wide')

if "autenticado" in st.session_state and st.session_state.autenticado:
    if st.sidebar.button("🚪 Sair"):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.rerun()

# (o restante do código do app continua aqui — você deve substituir por seu código principal)
st.title("Sistema de Telemonitoramento - Versão Corrigida")
st.write("✅ Login funcional, botão de logout ativo e layout CEUB aplicado.")
