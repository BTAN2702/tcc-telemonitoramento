
import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Relatório de Telemonitoramento", layout="wide")

# Estilo com as cores do CEUB
st.markdown("""
    <style>
    .stApp {
        background-color: #3d0052;
        color: white;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stButton>button {
        background-color: #e10098;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .css-1d391kg, .css-1wivap2, .stDataFrame {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
        padding: 10px;
    }
    .stDownloadButton > button {
        background-color: #e10098;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📋 Relatório de Telemonitoramento")
st.subheader("Visualize e gere relatórios em PDF dos dados de pacientes.")

# Exemplo de dados
dados = pd.DataFrame({
    'Paciente': ['Exemplo 1', 'Exemplo 2'],
    'Data': ['2025-05-01', '2025-05-02'],
    'Sintomas': ['Dor de cabeça, febre', 'Tontura e fadiga']
})

with st.expander("Visualizar Dados de Telemonitoramento"):
    st.dataframe(dados)

if st.button("Gerar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for index, row in dados.iterrows():
        pdf.cell(200, 10, txt=f"Paciente: {row['Paciente']}", ln=True)
        pdf.cell(200, 10, txt=f"Data: {row['Data']}", ln=True)
        sintoma_txt = f"Sintomas: {row['Sintomas']}"
        pdf.multi_cell(200, 10, txt=sintoma_txt)
    pdf.output("relatorio.pdf")
    with open("relatorio.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button(
        label="📥 Baixar relatório em PDF",
        data=PDFbyte,
        file_name="RelatorioTelemonitoramento.pdf",
        mime="application/pdf"
    )
    st.success("✅ Relatório PDF gerado com sucesso!")
