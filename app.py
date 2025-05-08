
import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import base64
import os

st.set_page_config(page_title="Telemonitoramento CEUB", layout="wide")

# --- Login ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario == "admin" and senha == "1234":
            st.session_state.autenticado = True
            st.success("✅ Login realizado com sucesso! Você será redirecionado automaticamente.")
            st.stop()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# --- Arquivo de dados persistente ---
csv_path = "pacientes.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=["Paciente", "Data", "Sintomas", "Pressão", "Glicemia", "Saturação", "Temperatura", "Frequência", "Adesão", "Próxima Visita"])

# --- Menu lateral ---
menu = st.sidebar.radio("Navegação", ["📋 Cadastro", "📈 Gráficos", "📄 Relatórios", "📥 Exportar CSV"])

# --- Cadastro ---
if menu == "📋 Cadastro":
    st.title("Cadastro de Paciente")
    with st.form("formulario"):
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
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(csv_path, index=False)
            st.success("✅ Dados salvos com sucesso!")

# --- Gráficos ---
elif menu == "📈 Gráficos":
    st.title("Gráficos de Evolução Clínica")
    if df.empty:
        st.warning("Nenhum dado cadastrado.")
    else:
        paciente_opcao = st.selectbox("Selecione um paciente", df["Paciente"].unique())
        dados_paciente = df[df["Paciente"] == paciente_opcao]
        dados_paciente["Data"] = pd.to_datetime(dados_paciente["Data"])

        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(dados_paciente.set_index("Data")["Glicemia"])
            st.line_chart(dados_paciente.set_index("Data")["Temperatura"])
        with col2:
            st.line_chart(dados_paciente.set_index("Data")["Frequência"])
            st.line_chart(dados_paciente.set_index("Data")["Saturação"])

# --- Relatórios ---
elif menu == "📄 Relatórios":
    st.title("📄 Gerar Relatório PDF")
    if df.empty:
        st.warning("Nenhum dado disponível.")
    else:
        paciente_escolhido = st.selectbox("Escolha o paciente", df["Paciente"].unique())
        registros = df[df["Paciente"] == paciente_escolhido]

        if st.button("📄 Gerar PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Relatório de {paciente_escolhido}", ln=True, align="C")

            for _, row in registros.iterrows():
                pdf.cell(200, 10, txt=f"Data: {row['Data']} - PA: {row['Pressão']} - Glicemia: {row['Glicemia']} - FC: {row['Frequência']} - SpO2: {row['Saturação']} - Temp: {row['Temperatura']} - Adesão: {row['Adesão']}", ln=True)
                pdf.multi_cell(200, 10, txt=f"Sintomas: {row['Sintomas']}\n\n")

            buffer = io.BytesIO()
            pdf.output(buffer)
            b64 = base64.b64encode(buffer.getvalue()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_{paciente_escolhido}.pdf">📥 Baixar PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

# --- Exportar CSV ---
elif menu == "📥 Exportar CSV":
    st.title("📥 Exportar Dados")
    if df.empty:
        st.warning("Nenhum dado para exportar.")
    else:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📤 Baixar arquivo CSV", data=csv, file_name="dados_pacientes.csv", mime="text/csv")
