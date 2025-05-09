import streamlit as st
import pandas as pd
import plotly.express as px
import bcrypt
import sqlite3
from datetime import datetime
from fpdf import FPDF
import base64

st.set_page_config(page_title="Telemonitoramento CEUB", layout="wide")

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("telemonitoramento.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (usuario TEXT PRIMARY KEY, senha TEXT, perfil TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS registros 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, paciente TEXT, data TEXT, sintomas TEXT, 
                  pressao TEXT, glicemia REAL, frequencia REAL, saturacao REAL, temperatura REAL, 
                  adesao TEXT, proxima_visita TEXT)''')
    conn.commit()
    conn.close()

def add_user(usuario, senha, perfil):
    conn = sqlite3.connect("telemonitoramento.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)", 
                  (usuario, hashed, perfil))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def validate_login(usuario, senha):
    conn = sqlite3.connect("telemonitoramento.db")
    c = conn.cursor()
    c.execute("SELECT senha, perfil FROM usuarios WHERE usuario=?", (usuario,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.checkpw(senha.encode(), result[0]):
        return result[1]  # Retorna o perfil
    return None

def save_record(record):
    conn = sqlite3.connect("telemonitoramento.db")
    c = conn.cursor()
    c.execute('''INSERT INTO registros (paciente, data, sintomas, pressao, glicemia, frequencia, 
                saturacao, temperatura, adesao, proxima_visita) VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                (record["Paciente"], record["Data"], record["Sintomas"], record["Pressao"], 
                 record["Glicemia"], record["Frequencia"], record["Saturacao"], 
                 record["Temperatura"], record["Adesao"], record["ProximaVisita"]))
    conn.commit()
    conn.close()
def get_records():
    conn = sqlite3.connect("telemonitoramento.db")
    c = conn.cursor()
    c.execute("SELECT * FROM registros")
    records = c.fetchall()
    conn.close()
    cols = ["ID", "Paciente", "Data", "Sintomas", "Pressao", "Glicemia", "Frequencia", 
            "Saturacao", "Temperatura", "Adesao", "ProximaVisita"]
    return pd.DataFrame(records, columns=cols)

# ---------------- Início da Aplicação ----------------
init_db()

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Login - Telemonitoramento CEUB")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        perfil = validate_login(usuario, senha)
        if perfil:
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.session_state.perfil = perfil
            st.success(f"✅ Bem-vindo, {usuario}!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# ---------------- Interface Principal ----------------
perfil = st.session_state.perfil
st.sidebar.markdown(f"👤 Logado como: **{st.session_state.usuario} ({perfil})**")

if perfil == "admin" and st.sidebar.button("👥 Cadastrar Usuário"):
    with st.form("form_cadastro"):
        new_user = st.text_input("Novo Usuário")
        new_pass = st.text_input("Nova Senha", type="password")
        new_perfil = st.selectbox("Perfil", ["admin", "paciente"])
        if st.form_submit_button("Cadastrar"):
            if add_user(new_user, new_pass, new_perfil):
                st.success("✅ Usuário cadastrado com sucesso!")
            else:
                st.warning("⚠️ Usuário já existe!")

if st.sidebar.button("🚪 Sair"):
    st.session_state.autenticado = False
    st.session_state.usuario = None
    st.experimental_rerun()

data = get_records()
menu_prof = ["🏥 Cadastro de Paciente", "📋 Registro Clínico", "📊 Painel de Monitoramento", 
              "📈 Gráficos de Evolução", "📄 Exportar CSV"]
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
                    save_record({
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
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV", data=csv, file_name="dados.csv", mime="text/csv")

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
                save_record({
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
