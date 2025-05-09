import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
import base64

st.set_page_config(page_title="Telemonitoramento CEUB", layout="wide")

# CSS CEUB
st.markdown("""
<style>
.stApp { background-color: #3d0052; color: white; }
h1, h2, h3, h4, h5, h6, .stMarkdown { color: white; }
.stTextInput > label, .stSelectbox label, .stTextArea label { color: white !important; }
.stButton > button {
    background-color: #28a745;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 18px;
}
.stDownloadButton > button {
    background-color: #28a745;
    color: white;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = None

# Login
if not st.session_state.autenticado:
    st.title("🔐 Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if (usuario == "admin" and senha == "1234") or (usuario == "paciente" and senha == "1234"):
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# Logout
if st.sidebar.button("🚪 Sair"):
    st.session_state.autenticado = False
    st.session_state.usuario = None
    st.rerun()

# Telas
st.title("📋 Relatório de Telemonitoramento")
st.markdown("Cadastre os dados clínicos dos pacientes e gere relatórios em PDF.")

if "dados" not in st.session_state:
    st.session_state.dados = []

with st.form("cadastro"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do paciente")
        data = st.date_input("Data da avaliação", value=datetime.today())
        pressao = st.text_input("Pressão Arterial (mmHg)")
        glicemia = st.number_input("Glicemia (mg/dL)", min_value=0.0)
        saturacao = st.number_input("Saturação de O2 (%)", min_value=0.0, max_value=100.0)
    with col2:
        temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=43.0)
        frequencia = st.number_input("Frequência Cardíaca (bpm)", min_value=0.0)
        adesao = st.selectbox("Adesão ao tratamento", ["Sim", "Não"])
        proxima = st.date_input("Próxima visita sugerida", value=datetime.today())
        sintomas = st.text_area("Sintomas")

    enviado = st.form_submit_button("💾 Salvar Dados do Paciente")
    if enviado:
        st.session_state.dados.append({
            "Paciente": nome, "Data": data, "Pressão": pressao, "Glicemia": glicemia,
            "Saturação": saturacao, "Temperatura": temperatura, "Frequência": frequencia,
            "Adesão": adesao, "Próxima Visita": proxima, "Sintomas": sintomas
        })
        st.success("✅ Dados do paciente salvos!")

# Tabela
if st.checkbox("📊 Visualizar dados cadastrados"):
    st.dataframe(pd.DataFrame(st.session_state.dados))

# PDF
if st.session_state.dados and st.button("📝 Gerar Relatório PDF"):
    df = pd.DataFrame(st.session_state.dados)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Monitoramento", ln=True, align="C")
    for _, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Paciente']} - {row['Data']} - PA: {row['Pressão']} - Glicemia: {row['Glicemia']}", ln=True)
        pdf.multi_cell(200, 10, txt=f"Sintomas: {row['Sintomas']}")
    buffer = io.BytesIO()
    pdf.output(buffer)
    b64 = base64.b64encode(buffer.getvalue()).decode()
    st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio.pdf">📥 Baixar PDF</a>', unsafe_allow_html=True)