
import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Relatório de Telemonitoramento", layout="wide")

# Estilo com as cores do CEUB e botões personalizados
st.markdown("""
    <style>
    .stApp {
        background-color: #3d0052;
        color: white;
    }
    h1, h2, h3, label, .stTextInput label, .stDateInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: white !important;
    }

    /* Texto dos inputs */
    input, textarea {
        color: black !important;
    }

    /* Botão de salvar */
    .stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 18px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
        border: none;
    }
    .stButton > button:first-child::before {
        content: "✅ ";
    }

    /* Botão de download */
    .stDownloadButton > button {
        background-color: #e10098;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }

    .css-1d391kg, .css-1wivap2, .stDataFrame {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    .stApp {
        background-color: #3d0052;
        color: white;
    }
    h1, h2, h3, label, .stTextInput label, .stDateInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: white !important;
    }
    input, textarea {
        color: white !important;
        background-color: white !important;
    }
    input[type="text"], input[type="number"], textarea {
        background-color: #ffffff !important;
        color: black !important;
    }
    .stTextInput > div > input, .stDateInput > div > input,
    .stNumberInput > div > input, .stTextArea > div > textarea {
        color: black !important;
    }
    .stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton > button:first-child::before {
        content: "✅ ";
    }
    .stDownloadButton > button {
        background-color: #e10098;
        color: white;
        font-weight: bold;
    }
    .css-1d391kg, .css-1wivap2, .stDataFrame {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    .stApp {
        background-color: #3d0052;
        color: white;
    }
    h1, h2, h3, label, .stTextInput label, .stDateInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: white !important;
    }
    .stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton > button:first-child::before {
        content: "✅ ";
    }
    .stDownloadButton > button {
        background-color: #e10098;
        color: white;
        font-weight: bold;
    }
    .css-1d391kg, .css-1wivap2, .stDataFrame {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📋 Relatório de Telemonitoramento")
st.subheader("Cadastre os dados clínicos dos pacientes e gere relatórios em PDF.")

if "dados" not in st.session_state:
    st.session_state.dados = []

# Formulário com layout ajustado
with st.form("formulario_paciente"):
    st.markdown("### 🧾 Cadastro de Paciente")

    # Linha 1
    col1, col2 = st.columns([2, 1])
    with col1:
        nome = st.text_input("Nome do paciente")
    with col2:
        data = st.date_input("Data da avaliação", value=datetime.today())

    # Linha 2
    col3, col4 = st.columns(2)
    with col3:
        pa = st.text_input("Pressão Arterial (mmHg)")
        glicemia = st.number_input("Glicemia (mg/dL)", min_value=0.0)
        saturacao = st.number_input("Saturação de O2 (%)", min_value=0.0, max_value=100.0)
    with col4:
        temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=43.0)
        frequencia = st.number_input("Frequência Cardíaca (bpm)", min_value=0.0)
        adesao = st.selectbox("Adesão ao tratamento", ["Sim", "Não"])

    # Linha 3
    col5, col6 = st.columns([1, 2])
    with col5:
        proxima = st.date_input("Próxima visita sugerida")
    with col6:
        sintomas = st.text_area("Sintomas")

    enviar = st.form_submit_button("Salvar dados do paciente")

    if enviar:
        novo = {
            "Paciente": nome,
            "Data": str(data),
            "Sintomas": sintomas,
            "Pressão": pa,
            "Glicemia": glicemia,
            "Saturação": saturacao,
            "Temperatura": temperatura,
            "Frequência": frequencia,
            "Adesão": adesao,
            "Próxima Visita": str(proxima)
        }
        st.session_state.dados.append(novo)
        st.success("✅ Dados do paciente salvos!")

if st.session_state.dados:
    df = pd.DataFrame(st.session_state.dados)
    with st.expander("📊 Visualizar dados cadastrados"):
        st.dataframe(df)

    if st.button("📄 Gerar Relatório PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=f"Paciente: {row['Paciente']}", ln=True)
            pdf.cell(200, 10, txt=f"Data: {row['Data']}", ln=True)
            pdf.multi_cell(200, 10, txt=f"Sintomas: {row['Sintomas']}")
            pdf.cell(200, 10, txt=f"PA: {row['Pressão']} - Glicemia: {row['Glicemia']} - Saturação: {row['Saturação']} - Temp: {row['Temperatura']} - FC: {row['Frequência']}", ln=True)
            pdf.cell(200, 10, txt=f"Adesão: {row['Adesão']} - Próxima: {row['Próxima Visita']}", ln=True)
            pdf.cell(200, 10, txt=" ", ln=True)

        pdf.output("relatorio.pdf")
        with open("relatorio.pdf", "rb") as f:
            PDFbyte = f.read()

        st.download_button(
            label="📥 Baixar Relatório em PDF",
            data=PDFbyte,
            file_name="RelatorioTelemonitoramento.pdf",
            mime="application/pdf"
        )
        st.success("✅ PDF gerado com sucesso!")
else:
    st.info("Nenhum paciente cadastrado ainda.")
