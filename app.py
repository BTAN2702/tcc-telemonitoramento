
import streamlit as st
import pandas as pd
from fpdf import FPDF

st.title("Telemonitoramento - Relatório de Monitoramento")

# Carregar os dados de telemonitoramento (substitua este exemplo pela fonte de dados real)
dados = pd.DataFrame({
    'Paciente': ['Exemplo 1', 'Exemplo 2'],
    'Data': ['2025-05-01', '2025-05-02'],
    'Sintomas': ['Dor de cabeça, febre', 'Tontura e fadiga']
})

st.write("Dados de telemonitoramento:", dados)

if st.button("Gerar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for index, row in dados.iterrows():
        pdf.cell(200, 10, txt=f"Paciente: {row['Paciente']}", ln=True)
        pdf.cell(200, 10, txt=f"Data: {row['Data']}", ln=True)
        pdf.multi_cell(200, 10, txt=f"Sintomas: {row['Sintomas']}

")
    pdf.output("relatorio.pdf")
    with open("relatorio.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button(
        label="Baixar relatório em PDF",
        data=PDFbyte,
        file_name="RelatorioTelemonitoramento.pdf",
        mime="application/pdf"
    )
