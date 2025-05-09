
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
import base64
import os

st.set_page_config(page_title="Telemonitoramento CEUB", layout="wide")

USUARIOS_CSV = "usuarios.csv"
DADOS_CSV = "dados.csv"

def carregar_usuarios():
    if os.path.exists(USUARIOS_CSV):
        return pd.read_csv(USUARIOS_CSV)
    else:
        df = pd.DataFrame(columns=["usuario", "senha", "perfil"])
        df.to_csv(USUARIOS_CSV, index=False)
        return df

def salvar_usuario(usuario, senha, perfil):
    df = carregar_usuarios()
    if usuario in df["usuario"].values:
        return False
    df = pd.concat([df, pd.DataFrame([[usuario, senha, perfil]], columns=["usuario", "senha", "perfil"])]).reset_index(drop=True)
    df.to_csv(USUARIOS_CSV, index=False)
    return True

def carregar_dados():
    if os.path.exists(DADOS_CSV):
        return pd.read_csv(DADOS_CSV)
    else:
        df = pd.DataFrame(columns=["Paciente", "Data", "Sintomas", "Pressao", "Glicemia", "Frequencia", 
                                   "Saturacao", "Temperatura", "Adesao", "ProximaVisita"])
        df.to_csv(DADOS_CSV, index=False)
        return df

def salvar_dado(registro):
    df = carregar_dados()
    df = pd.concat([df, pd.DataFrame([registro])]).reset_index(drop=True)
    df.to_csv(DADOS_CSV, index=False)

def gerar_link_csv():
    with open(DADOS_CSV, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dados.csv">📥 Baixar CSV</a>'
    return href

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Login - Telemonitoramento CEUB")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuarios = carregar_usuarios()
        user = usuarios[(usuarios["usuario"] == usuario) & (usuarios["senha"] == senha)]
        if not user.empty:
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.session_state.perfil = user.iloc[0]["perfil"]
            st.success(f"✅ Bem-vindo, {usuario}!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    if st.button("Registrar Novo Usuário"):
        with st.form("form_cadastro"):
            new_user = st.text_input("Novo Usuário")
            new_pass = st.text_input("Nova Senha", type="password")
            perfil = st.selectbox("Perfil", ["admin", "paciente"])
            if st.form_submit_button("Cadastrar"):
                if salvar_usuario(new_user, new_pass, perfil):
                    st.success("✅ Usuário cadastrado!")
                else:
                    st.warning("⚠️ Usuário já existe!")
    st.stop()

perfil = st.session_state.get("perfil", "paciente")
st.sidebar.markdown(f"👤 Logado como: **{st.session_state.usuario}**")
if st.sidebar.button("🚪 Sair"):
    st.session_state.autenticado = False
    st.session_state.usuario = None
    st.experimental_rerun()

data = carregar_dados()

menu_prof = ["🏥 Cadastro de Paciente", "📋 Registro Clínico", "📊 Painel de Monitoramento", "📈 Gráficos de Evolução", "📄 Exportar CSV"]
menu_pac = ["📝 Autoavaliação", "📚 Meus Registros"]
menu = st.sidebar.radio("Menu", menu_prof if perfil == "admin" else menu_pac)

if perfil == "admin":
    if menu == "🏥 Cadastro de Paciente":
        st.title("Cadastro de Paciente")
        with st.form("form_cad"):
            nome = st.text_input("Nome")
            data_atual = st.date_input("Data", value=datetime.today())
            sintomas = st.text_area("Sintomas")
            pa = st.text_input("Pressão Arterial")
            glicemia = st.number_input("Glicemia")
            fc = st.number_input("Frequência Cardíaca")
            spo2 = st.number_input("SpO2")
            temperatura = st.number_input("Temperatura")
            adesao = st.selectbox("Adesão", ["Sim", "Não"])
            proxima = st.date_input("Próxima Visita")

            if st.form_submit_button("✅ Salvar Dados"):
                if nome:
                    salvar_dado({
                        "Paciente": nome, "Data": data_atual, "Sintomas": sintomas,
                        "Pressao": pa, "Glicemia": glicemia, "Frequencia": fc,
                        "Saturacao": spo2, "Temperatura": temperatura,
                        "Adesao": adesao, "ProximaVisita": proxima
                    })
                    st.success("✅ Registro salvo!")
                else:
                    st.error("⚠️ Nome é obrigatório!")

    elif menu == "📄 Exportar CSV":
        st.title("📄 Exportação de Dados")
        st.markdown(gerar_link_csv(), unsafe_allow_html=True)

    elif menu == "📊 Painel de Monitoramento":
        st.title("📊 Monitoramento de Pacientes")
        st.dataframe(data)

    elif menu == "📈 Gráficos de Evolução":
        st.title("📈 Gráficos de Evolução")
        paciente = st.selectbox("Selecione o paciente", data["Paciente"].unique())
        df_paciente = data[data["Paciente"] == paciente]
        if not df_paciente.empty:
            fig = px.line(df_paciente, x="Data", y=["Glicemia", "Frequencia", "Temperatura"], 
                          title=f"Evolução de Indicadores - {paciente}")
            st.plotly_chart(fig)
        else:
            st.warning("Nenhum dado encontrado para este paciente.")

elif perfil == "paciente":
    if menu == "📝 Autoavaliação":
        st.title("📝 Autoavaliação")
        with st.form("form_auto"):
            nome = st.session_state.usuario
            data_atual = st.date_input("Data", value=datetime.today())
            sintomas = st.text_area("Sintomas")
            pa = st.text_input("Pressão Arterial")
            glicemia = st.number_input("Glicemia")
            fc = st.number_input("Frequência Cardíaca")
            spo2 = st.number_input("SpO2")
            temperatura = st.number_input("Temperatura")

            if st.form_submit_button("✅ Enviar"):
                salvar_dado({
                    "Paciente": nome, "Data": data_atual, "Sintomas": sintomas,
                    "Pressao": pa, "Glicemia": glicemia, "Frequencia": fc,
                    "Saturacao": spo2, "Temperatura": temperatura,
                    "Adesao": "Não informado", "ProximaVisita": ""
                })
                st.success("✅ Autoavaliação enviada!")

    elif menu == "📚 Meus Registros":
        st.title("📚 Meus Registros")
        meus_dados = data[data["Paciente"] == st.session_state.usuario]
        st.dataframe(meus_dados)
