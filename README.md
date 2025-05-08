
# 📋 Telemonitoramento CEUB

Este projeto é um aplicativo desenvolvido com [Streamlit](https://streamlit.io/) para auxiliar no **telemonitoramento de pacientes** da Clínica Escola de Enfermagem do CEUB.

## 🎯 Objetivo

Permitir que profissionais de saúde possam:
- Registrar dados clínicos de pacientes em acompanhamento
- Visualizar esses dados em tempo real
- Gerar relatórios em PDF com todas as informações

## 🛠 Tecnologias utilizadas

- `streamlit` – para interface web interativa
- `pandas` – para manipulação de dados clínicos
- `fpdf` – para geração dos relatórios em PDF

## 🎨 Identidade Visual

A interface do sistema utiliza as **cores institucionais do CEUB**:
- Fundo: Roxo escuro (`#3d0052`)
- Destaques e botões: Rosa (`#e10098`)
- Textos: Branco

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/BTAN2702/tcc-telemonitoramento.git
cd tcc-telemonitoramento
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run app.py
```

## 📄 Relatórios

Após cadastrar os pacientes e inserir os dados clínicos, é possível gerar um relatório em PDF com:
- Dados de avaliação (PA, glicemia, temperatura etc.)
- Relato de sintomas
- Adesão ao tratamento
- Próxima visita

O arquivo gerado pode ser baixado diretamente pela interface.

## 👨‍⚕️ Público-alvo

- Estudantes e profissionais de enfermagem
- Equipe multiprofissional da clínica escola
- Projetos de TCC e monitoramento acadêmico

## 📌 Autor

Desenvolvido por **Artur Nascimento Bittencourt**  
Projeto de Trabalho de Conclusão de Curso (TCC) – CEUB 2025  
Contato: artur.bittencourt@sempreceub.com

---

*Este repositório faz parte de um projeto acadêmico de implementação de ferramentas digitais na assistência em saúde.*
