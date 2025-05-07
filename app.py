import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
import base64

st.set_page_config(page_title="Telemonitoramento CEUB", layout="wide")

# --- Autenticação simples ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Login - Telemonitoramento CEUB")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario == "admin" and senha == "1234":
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# --- Banco de dados em sessão ---
if 'pacientes' not in st.session_state:
    st.session_state.pacientes = []

if 'registros' not in st.session_state:
    st.session_state.registros = []

# --- Menu ---
menu = st.sidebar.radio("Menu", [
    "Cadastro de Paciente",
    "Registro Clínico",
    "Painel de Monitoramento",
    "Gráficos de Evolução",
    "Gerar Relatório PDF"
])

# --- Cadastro de paciente ---
if menu == "Cadastro de Paciente":
    st.title("Cadastro de Paciente")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome do Paciente")
        idade = st.number_input("Idade", min_value=0)
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino", "Outro"])
        contato = st.text_input("Telefone/Contato")
        email = st.text_input("E-mail")
        encaminhamento = st.text_area("Encaminhamento / Observações")
        enviar = st.form_submit_button("Salvar Paciente")

        if enviar:
            st.session_state.pacientes.append({
                "Nome": nome, "Idade": idade, "Sexo": sexo,
                "Contato": contato, "Email": email,
                "Encaminhamento": encaminhamento
            })
            st.success("Paciente cadastrado com sucesso!")

    if st.session_state.pacientes:
        st.subheader("Pacientes Cadastrados")
        st.dataframe(pd.DataFrame(st.session_state.pacientes))

# --- Registro Clínico ---
elif menu == "Registro Clínico":
    st.title("Registro de Indicadores Clínicos")
    if not st.session_state.pacientes:
        st.warning("Cadastre ao menos um paciente antes de registrar indicadores.")
    else:
        nomes = [p["Nome"] for p in st.session_state.pacientes]
        with st.form("form_registro"):
            paciente = st.selectbox("Selecionar Paciente", nomes)
            data = st.date_input("Data da Avaliação", value=datetime.today())
            pa = st.text_input("Pressão Arterial (mmHg)")
            glicemia = st.number_input("Glicemia (mg/dL)", min_value=0.0)
            fc = st.number_input("Frequência Cardíaca (bpm)", min_value=0.0)
            spo2 = st.number_input("Saturação O2 (%)", min_value=0.0, max_value=100.0)
            temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=43.0)
            sintomas = st.text_area("Relato de sintomas")
            adesao = st.selectbox("Adesão ao Tratamento", ["Sim", "Não"])
            proxima_visita = st.date_input("Próxima visita sugerida")
            salvar = st.form_submit_button("Salvar Registro")

            if salvar:
                st.session_state.registros.append({
                    "Paciente": paciente,
                    "Data": data,
                    "Pressão": pa,
                    "Glicemia": glicemia,
                    "Frequência": fc,
                    "Saturação": spo2,
                    "Temperatura": temperatura,
                    "Sintomas": sintomas,
                    "Adesão": adesao,
                    "Próxima Visita": proxima_visita
                })
                st.success("Registro salvo com sucesso!")

# --- Painel de Monitoramento ---
elif menu == "Painel de Monitoramento":
    st.title("Painel de Monitoramento")
    if not st.session_state.registros:
        st.warning("Nenhum dado registrado ainda.")
    else:
        df = pd.DataFrame(st.session_state.registros)
        paciente_filtro = st.selectbox("Filtrar por paciente", ["Todos"] + df["Paciente"].unique().tolist())
        if paciente_filtro != "Todos":
            df = df[df["Paciente"] == paciente_filtro]
        st.dataframe(df)

        st.subheader("Alertas Clínicos")
        alertas = df[(df["Saturação"] < 90) | (df["Glicemia"] > 300)]
        if not alertas.empty:
            st.error("Atenção: Pacientes com indicadores críticos:")
            st.dataframe(alertas)
        else:
            st.success("Nenhum alerta crítico encontrado.")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar dados em CSV", data=csv, file_name="monitoramento_clinico.csv", mime='text/csv')

# --- Gráficos de evolução ---
elif menu == "Gráficos de Evolução":
    st.title("Gráficos de Evolução Clínica")
    if not st.session_state.registros:
        st.warning("Nenhum dado registrado ainda.")
    else:
        df = pd.DataFrame(st.session_state.registros)
        paciente = st.selectbox("Selecione o paciente para visualizar evolução", df["Paciente"].unique())
        df_paciente = df[df["Paciente"] == paciente].sort_values("Data")
        df_paciente["Data"] = pd.to_datetime(df_paciente["Data"])

        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(df_paciente.set_index("Data")["Glicemia"])
            st.line_chart(df_paciente.set_index("Data")["Temperatura"])
        with col2:
            st.line_chart(df_paciente.set_index("Data")["Frequência"])
            st.line_chart(df_paciente.set_index("Data")["Saturação"])

# --- Gerar PDF ---
elif menu == "Gerar Relatório PDF":
    st.title("📄 Gerar Relatório em PDF")
    if not st.session_state.registros:
        st.warning("Nenhum dado registrado.")
    else:
        df = pd.DataFrame(st.session_state.registros)
        pacientes = df["Paciente"].unique().tolist()
        escolhido = st.selectbox("Escolha o paciente para gerar o PDF", pacientes)
        dados = df[df["Paciente"] == escolhido]

        if st.button("Gerar PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Relatório de {escolhido}", ln=True, align="C")

            for index, row in dados.iterrows():
                pdf.cell(200, 10, txt=f"Data: {row['Data']} - PA: {row['Pressão']} - Glicemia: {row['Glicemia']} - FC: {row['Frequência']} - SpO2: {row['Saturação']} - Temp: {row['Temperatura']} - Adesão: {row['Adesão']}", ln=True)
               pdf.multi_cell(200, 10, txt=f"Sintomas: {row['Sintomas']}\n\n")

            buffer = io.BytesIO()
            pdf.output(buffer)
            b64 = base64.b64encode(buffer.getvalue()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_{escolhido}.pdf">📥 Clique aqui para baixar o PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
