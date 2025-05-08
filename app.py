
import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Telemonitoramento - Relatório", layout="wide")

# CSS para estilizar botões com fundo verde e ícones
st.markdown("""
<style>
.stApp {
    background-color: #3d0052;
    color: white;
}
h1, h2, h3, label,
.stTextInput label,
.stDateInput label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label {
    color: white !important;
}
input, textarea {
    color: black !important;
    background-color: white !important;
}
.stTextInput > div > input,
.stDateInput > div > input,
.stNumberInput > div > input,
.stTextArea > div > textarea {
    color: black !important;
}

/* Botões com aparência unificada */
.stButton > button, .stDownloadButton > button {
    background-color: #28a745 !important;
    color: white !important;
    font-weight: bold;
    font-size: 18px;
    padding: 10px 24px;
    border-radius: 10px;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #218838 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📋 Relatório de Telemonitoramento")
st.subheader("Cadastre os dados clínicos dos pacientes e gere relatórios em PDF.")

if "dados" not in st.session_state:
    st.session_state.dados = []

# Formulário
with st.form("formulario"):
    st.markdown("### 🧾 Cadastro de Paciente")
    col1, col2 = st.columns([2, 1])
    with col1:
        nome = st.text_input("Nome do paciente")
    with col2:
        data = st.date_input("Data da avaliação", value=datetime.today())
    
    col3, col4 = st.columns(2)
    with col3:
        pa = st.text_input("Pressão Arterial (mmHg)")
        glicemia = st.number_input("Glicemia (mg/dL)", min_value=0.0)
        saturacao = st.number_input("Saturação de O2 (%)", min_value=0.0, max_value=100.0)
    with col4:
        temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=43.0)
        frequencia = st.number_input("Frequência Cardíaca (bpm)", min_value=0.0)
        adesao = st.selectbox("Adesão ao tratamento", ["Sim", "Não"])
    
    col5, col6 = st.columns([1, 2])
    with col5:
        proxima = st.date_input("Próxima visita sugerida")
    with col6:
        sintomas = st.text_area("Sintomas")

    enviar = st.form_submit_button("✅ Salvar dados do paciente")

    if enviar:
        st.session_state.dados.append({
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
        })
        st.success("✅ Dados do paciente salvos!")

# Visualização e geração de PDF
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
            label="📄 Baixar Relatório PDF",
            data=PDFbyte,
            file_name="RelatorioTelemonitoramento.pdf",
            mime="application/pdf"
        )
