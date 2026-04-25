# 🤖 Automação de Emissão de Notas - Hand PDV

Este projeto tem como objetivo automatizar a geração mensal de documentos fiscais no sistema web **Hand PDV**, além do envio automático desses arquivos para a contadora via WhatsApp Web.

---

## 📌 Objetivo

Eliminar a necessidade de execução manual do processo de:
- Geração de relatórios fiscais (NFC-e)
- Exportação de arquivos (.zip e .pdf)
- Organização dos documentos
- Envio para a contadora

Tudo isso sendo executado automaticamente no **primeiro dia útil de cada mês**.

---

## ⚙️ Funcionalidades

- 🔐 Login automático no sistema Hand PDV  
- 📄 Geração automática de:
  - Arquivo `.zip` com notas fiscais
  - Relatório `.pdf` de vendas com NFC-e  
- 📅 Seleção automática do período (mês anterior)  
- 💾 Organização e renomeação dos arquivos  
- 📤 Envio automático via WhatsApp Web  
- 📝 Geração de logs de execução  

---

## 🧱 Estrutura do Projeto
projeto_notas/
│── main.py # Script principal
│── config.json # Configurações (login, senha, paths, contato)
│── modules/
│ ├── hand_pdv.py # Automação do sistema Hand PDV
│ ├── whatsapp.py # Automação do WhatsApp Web
│ └── utils.py # Funções auxiliares
│── logs/
│ └── execucao.log # Logs de execução
│── downloads/ # Arquivos temporários
│── notas/ # Arquivos organizados por mês


---

## 🛠️ Tecnologias Utilizadas

- Python 3.x  
- Selenium (automação web com Firefox)  
- Geckodriver (driver do Firefox)  
- Windows Task Scheduler (agendamento automático)  

---

## 🚀 Como Executar

### 1. Clonar o repositório

git clone https://github.com/seu-usuario/projeto_notas.git
cd projeto_notas

### 2. Instalar dependências

pip install selenium schedule

### 3. Baixar o Geckodriver

{
  "url": "https://seu-handpdv.com",
  "usuario": "SEU_USUARIO",
  "senha": "SUA_SENHA",
  "contadora": "Nome do Contato no WhatsApp",
  "caminho_download": "C:\\Notas\\downloads",
  "caminho_final": "C:\\Notas\\arquivos"
}

### 5. Executar manualmente

python main.py

---

⏰ Agendamento Automático (Windows)
1. Abrir o Agendador de Tarefas do Windows
2. Criar nova tarefa
3. Definir gatilho:
* Mensal
* Primeiro dia útil
4. Ação:
* Programa/script: python
* Argumentos: caminho\para\main.py

---

⚠️ Observações
* O sistema depende da estrutura HTML do Hand PDV — mudanças na interface podem exigir ajustes no código.
* O WhatsApp Web precisa estar previamente autenticado no navegador.
* Recomenda-se não usar o computador durante a execução da automação.

---

📌 Melhorias Futuras
* Interface gráfica (GUI) para facilitar uso
* Criptografia das credenciais
* Notificação por e-mail em caso de erro
* Suporte a múltiplas empresas
* Execução em servidor (sem dependência de PC local)

---

👨‍💻 Autor

Projeto desenvolvido por Arthur Bortolanza
Engenheiro de Controle e Automação | Automação Industrial | Programação

---

📄 Licença

Este projeto é de uso pessoal. Sinta-se livre para adaptar conforme necessário.
