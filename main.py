import time
import os
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from datetime import datetime, timedelta
from email.message import EmailMessage

def esperar_downlad(pasta, extensao, timeout = 30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        arquivos = [f for f in os.listdir(pasta) if f.endswith(extensao)]
        if arquivos:
            return True
        time.sleep(1)
    raise TimeoutError(f"Download de {extensao} não concluido!")

def esta_logado(driver):
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'NF-e')]")
        return True
    except NoSuchElementException:
        return False

def criar_driver():
    options = webdriver.FirefoxOptions()
    options.set_preference("browser.download.folderlist", 2)
    options.set_preference("browser.download.dir", r"C:\Users\Usuario\Downloads")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)
    service = Service(executable_path="geckodriver.exe")

    return webdriver.Firefox(service=service, options=options)

def obtem_arquivos_recentes(pasta, extensoes=(".zip", ".pdf")):
    arquivos = [
        os.path.join(pasta, f)
        for f in os.listdir(pasta)
        if f.endswith(extensoes)
    ]

    arquivos.sort(key=os.path.getmtime, reverse = True)

    return arquivos

def enviar_email(remetente, senha_app, destinatario, zip_path, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = 'Relatórios Mensais'
    msg['From'] = remetente
    msg['To'] = destinatario

    msg.set_content('Bom dia\n\nSegue em anexo os relatórios mensais.\n\nAtt.')

    # Anexa zip
    with open(zip_path, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype = 'application',
            subtype = 'zip',
            filename = os.path.basename(zip_path)
        )

    # Anexa o pdf
    with open(pdf_path, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype = 'application',
            subtype = 'pdf',
            filename = os.path.basename(pdf_path)
        )
    
    # Envia o email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha_app)
        smtp.send_message(msg)

    print("Email enviado com sucesso!")

# Local dos arquivos baixados
pasta_downloads = r"C:\Users\Usuario\Downloads"

driver = criar_driver()
wait = WebDriverWait(driver, 10) #Todos os time.sleep serao substituidos por isso futuramente

# Encontra o período para geração dos relatorios (primeiro e ultimo dia do mes anterior ao que nos encontramos)
hoje = datetime.today()

# Primeiro dia do mes atual
primeiro_dia_mes_atual = hoje.replace(day=1)
# Último dia do mês anterior
ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
# Primeiro dia do mês anterior
primeiro_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)
# Mes anterior formato mm-yyyy (para renomear os arquivos baixados)
mes_ref = primeiro_dia_mes_anterior.strftime("%m-%Y") 
# Formata no padrao dd/mm/yyyy
data_inicio = primeiro_dia_mes_anterior.strftime("%d/%m/%Y")
data_fim = ultimo_dia_mes_anterior.strftime("%d/%m/%Y")

# Acessa o hand
driver.get("https://localhost:8080/HAND/")

if not esta_logado(driver):
    print("Não está logado! Realizando login...")
    
    # Aguarda a página carregar
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Login']"))
    )

    # Preenche o login
    driver.find_element(By.XPATH, "//input[@placeholder='Login']").send_keys("6")

    # Preenche a senha + Enter
    driver.find_element(By.XPATH, "//input[@placeholder='Senha']").send_keys("6" + Keys.ENTER)

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'NFC-e')]"))
    )



# Acessa a página onde sera configurado o relatório
driver.get("https://localhost:8080/HAND/pages/nfe/gerenciamento/search/searchGerenciamentoNfe.xhtml")
wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'dtInicio')]"))
)

# Configura o primeiro relatório
dropDown = Select(wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Modelo de Documento Fiscal')]/following::select[1]"))
))
dropDown.select_by_visible_text("NFC-e")

# Limpa e insere periodo inicial e final
# Periodo inicial
campo_inicio = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@name,'dtInicio')]"))
)
campo_inicio.clear()
campo_inicio.send_keys(data_inicio)

# Periodo final
campo_fim = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@name,'dtFim')]"))
)
campo_fim.clear()
campo_fim.send_keys(data_fim)

# Pressiona botao pesquisar
wait.until(
    EC.element_to_be_clickable((By.ID, "btnPesquisar"))
).click()

# Aguarda o driver carregar
wait = WebDriverWait(driver, 10)

# Seleciona todas as notas do periodo
checkbox = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//th//div[contains(@class,'ui-chkbox-box')]")
    )
)
# Se a checkbox nao estiver marcada, marca
if "ui-state-active" not in checkbox.get_attribute("class"):
    checkbox.click()

# Pressiona exportar notas
wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Exportar')]"))
)

esperar_downlad(pasta_downloads, ".zip")

### Geração do segundo arquivo ###

# Acessa a página onde sera configurado o segundo relatório
driver.get("https://localhost:8080/HAND/pages/entrada/porNota/search/searchEntradaPorNota.xhtml")
time.sleep(10)

# Limpa e insere periodo inicial e final
# Periodo inicial
campo_inicio = driver.find_element(By.NAME, "j_idt65:j_idt66:j_idt66_input")
campo_inicio.clear()
campo_inicio.send_keys(data_inicio)
time.sleep(3)

# Periodo final
campo_fim = driver.find_element(By.NAME, "j_idt70:j_idt71:j_idt71_input")
campo_fim.clear()
campo_fim.send_keys(data_fim)

time.sleep(3)

# Configura o modelo de relatório
dropDown = Select(driver.find_element(By.NAME, "j_idt304:j_idt305"))
dropDown.select_by_visible_text("Nota Fiscal de Consumidor Eletronica")

time.sleep(3)

# Pressiona botao pesquisar
driver.find_element(By.ID, "btnSalvarCadastro").click()

time.sleep(3)

# Pressiona imprimir
botao = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@title='Imprimir PDF']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", botao)
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Imprimir PDF']")))
driver.execute_script("arguments[0].click();", botao)

# Seleciona o modelo
dropDown = Select(driver.find_element(By.NAME, "j_idt62:j_idt65:comboModeloRelatorio:j_idt71"))
dropDown.select_by_visible_text("Venda com NFC-e")

# Pressiona PDF
driver.find_element(By.ID, "j_idt62:j_idt65:j_idt76").click()

time.sleep(10)

### Identificar e renomear os arquivos ###
# Função que obtem os arquivos mais recentes
arquivos = obtem_arquivos_recentes(pasta_downloads)

# Separa os arquivos em duas variaveis
zip_file = next(f for f in arquivos if f.endswith(".zip"))
pdf_file = next(f for f in arquivos if f.endswith(".pdf"))

# Novo nome dos arquivos
novo_zip = os.path.join(pasta_downloads, f"NFE_{mes_ref}.zip")
novo_pdf = os.path.join(pasta_downloads, f"NFCe_{mes_ref}.pdf")

# Renomeia os arquivos
os.rename(zip_file, novo_zip)
os.rename(pdf_file, novo_pdf)

time.sleep(10)

### Enviar para contadora ###
enviar_email(
    remetente = "mariabombomcco@gmail.com",
    senha_app = os.getenv("EMAIL_SENHA"),
    destinatario = "arthurrodrigueslima@gmail.com",
    zip_path = novo_zip,
    pdf_path = novo_pdf
)