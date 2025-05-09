import streamlit as st
st.set_page_config(page_title="Telemonitoramento CEUB", layout="wide")

# Botão de logout
if "autenticado" in st.session_state and st.session_state.autenticado:
    if st.sidebar.button("🚪 Sair"):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.rerun()

import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import base64
import os

# --- Autenticação simples ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Login - Telemonitoramento CEUB")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in ["admin", "paciente"] and senha == "1234":
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.success("✅ Login realizado com sucesso!")
            st.stop()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

perfil = st.session_state.get('usuario', 'Paciente')

if 'registros' not in st.session_state:
    st.session_state.registros = []

# Menu de navegação
menu_prof = ["Cadastro de Paciente", "Registro Clínico", "Painel de Monitoramento", "Gráficos de Evolução", "Gerar Relatório PDF"]
menu_pac = ["Autoavaliação", "Meus Registros"]
menu = st.sidebar.radio("Menu", menu_prof if perfil == "admin" else menu_pac)

if perfil == "admin":
    if menu == "Cadastro de Paciente":
        st.title("Cadastro de Paciente")
        with st.form("form_cad"):
            nome = st.text_input("Nome")
            data = st.date_input("Data", value=datetime.today())
            sintomas = st.text_area("Sintomas")
            pa = st.text_input("PA")
            glicemia = st.number_input("Glicemia")
            fc = st.number_input("FC")
            spo2 = st.number_input("SpO2")
            temperatura = st.number_input("Temperatura")
            adesao = st.selectbox("Adesão", ["Sim", "Não"])
            proxima = st.date_input("Próxima visita sugerida")
            if st.form_submit_button("✅ Salvar Dados do Paciente"):
                st.session_state.registros.append({
                    "Paciente": nome, "Data": data, "Sintomas": sintomas,
                    "Pressão": pa, "Glicemia": glicemia, "Frequência": fc,
                    "Saturação": spo2, "Temperatura": temperatura,
                    "Adesão": adesao, "Próxima Visita": proxima
                })
                st.success("✅ Registro salvo!")
    elif menu == "Gerar Relatório PDF":
        if not st.session_state.registros:
            st.warning("Nenhum dado registrado.")
        else:
            df = pd.DataFrame(st.session_state.registros)
            paciente = st.selectbox("Escolha o paciente", df["Paciente"].unique())
            dados = df[df["Paciente"] == paciente]
            if st.button("📄 Gerar PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Relatório de {paciente}", ln=True)
                for _, row in dados.iterrows():
                    pdf.cell(200, 10, txt=f"Data: {row['Data']} - PA: {row['Pressão']} - Glicemia: {row['Glicemia']}", ln=True)
                    pdf.multi_cell(200, 10, txt=f"Sintomas: {row['Sintomas']}\n\n")
                pdf_bytes = pdf.output(dest="S").encode("latin1")
                b64 = base64.b64encode(pdf_bytes).decode()
                st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_{paciente}.pdf">📥 Baixar PDF</a>', unsafe_allow_html=True)

elif perfil == "paciente":
    if menu == "Autoavaliação":
        st.title("📋 Autoavaliação")
        with st.form("form_auto"):
            nome = st.text_input("Seu nome")
            data = st.date_input("Data", value=datetime.today())
            sintomas = st.text_area("Sintomas")
            pa = st.text_input("PA")
            glicemia = st.number_input("Glicemia")
            fc = st.number_input("FC")
            spo2 = st.number_input("SpO2")
            temperatura = st.number_input("Temperatura")
            if st.form_submit_button("✅ Enviar"):
                st.session_state.registros.append({
                    "Paciente": nome, "Data": data, "Sintomas": sintomas,
                    "Pressão": pa, "Glicemia": glicemia, "Frequência": fc,
                    "Saturação": spo2, "Temperatura": temperatura,
                    "Adesão": "Não informado", "Próxima Visita": ""
                })
                st.success("✅ Autoavaliação enviada!")
