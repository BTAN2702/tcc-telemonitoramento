
# 🩺 Aplicativo de Telemonitoramento CEUB

Este repositório contém um sistema web interativo para **telemonitoramento de pacientes crônicos**, desenvolvido como parte do Trabalho de Conclusão de Curso em Enfermagem no CEUB (Centro Universitário de Brasília).

## 🎯 Objetivo

Facilitar o acompanhamento clínico remoto de pacientes atendidos na clínica escola de enfermagem do CEUB, permitindo:

- Cadastro de pacientes e coleta de indicadores clínicos
- Monitoramento contínuo e visualização gráfica da evolução
- Geração de relatórios em PDF
- Exportação de dados em CSV
- Interface segura com login

## 🚀 Funcionalidades

- ✅ **Login simples** para acesso seguro
- ✅ **Cadastro de pacientes** e indicadores (PA, glicemia, FC, temperatura, sintomas...)
- ✅ **Gráficos de evolução clínica**
- ✅ **Filtro por paciente**
- ✅ **Geração de relatório PDF com histórico**
- ✅ **Exportação de dados em .csv**
- ✅ **Salvamento persistente em arquivo CSV**
- ✅ **Interface com menu lateral e cores do CEUB**

## 🛠 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/) – desenvolvimento da interface web
- [Pandas](https://pandas.pydata.org/) – manipulação dos dados clínicos
- [FPDF](https://pyfpdf.github.io/fpdf2/) – geração de relatórios PDF

## 🧑‍⚕️ Público-alvo

- Estudantes e profissionais de enfermagem
- Equipes multidisciplinares
- Clínicas escola ou centros de atenção comunitária

## 📦 Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/tcc-telemonitoramento.git
cd tcc-telemonitoramento
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run app.py
```

## ☁️ Deploy no Streamlit Cloud

1. Crie um repositório no GitHub com este conteúdo
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
3. Conecte com seu GitHub e selecione o repositório
4. Defina o arquivo principal como `app.py`
5. Clique em **Deploy** 🚀

---

## 📄 Licença

Este projeto é acadêmico e livre para fins educacionais.

---

**Desenvolvido por:**  
Artur Nascimento Bittencourt – TCC Enfermagem CEUB (2025)  
📧 artur.bittencourt@sempreceub.com
