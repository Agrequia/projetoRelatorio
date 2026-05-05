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

def esperar_downlad(pasta, snapshot, extensao, timeout = 30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        arquivos_depois = set(os.listdir(pasta))
        novos = arquivos_depois - snapshot
        for arquivo in novos:
            if arquivo.endswith(extensao):
                return os.path.join(pasta, arquivo)
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

# Snapshot dos arquivos antes do download
snapshot_arquivos = set(os.listdir(pasta_downloads))

# Aguarda página carregar:
wait.until(
    EC.invisibility_of_element_located((By.ID, "loadingModal"))
)

# Pressiona exportar notas
wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Exportar')]"))
).click()

zip_path = esperar_downlad(pasta_downloads, snapshot_arquivos, ".zip")

### Geração do segundo arquivo ###

# Acessa a página onde sera configurado o segundo relatório
driver.get("https://localhost:8080/HAND/pages/entrada/porNota/search/searchEntradaPorNota.xhtml")

# Limpa e insere periodo inicial e final
# Periodo inicial
campo_inicio = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "(//input[contains(@class,'hasDatepicker')])[1]")
    )
)
campo_inicio.clear()
campo_inicio.send_keys(data_inicio)

# Periodo final
campo_fim = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "(//input[contains(@class,'hasDatepicker')])[2]")
    )
)
campo_fim.clear()
campo_fim.send_keys(data_fim)

# Configura o modelo de relatório
dropDown = Select(wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'ItemFiltro') and text()='Modelo']/following::select[1]"
    ))
))
for option in dropDown.options:
    if "Consumidor" in option.text:
        option.click()
        break

# Pressiona botao pesquisar
wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[.//span[contains(text(),'Consultar')]]"))
)

# Espera terminar carregamento
wait.until(
    EC.invisibility_of_element_located((By.ID,"loadingModal"))
)

# Esperar elemento carregado
wait.until(
    EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'box-icon')]"))
)

# Pressiona imprimir
botao = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@title='Imprimir PDF']"))
)
driver.execute_script("arguments[0].click();", botao)

# Aguarda modal carregar
wait.until(
    EC.visibility_of_element_located((
        By.XPATH, "//div[contains(@class,'ui-dialog') and .//div[contains(text(),'Modelo do Relatório)]]"
    ))
)

# Seleciona o modelo
dropDown = Select(wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(text(),'Modelo do Relatório')]//following::select[1]"
    ))    
))

for option in dropDown.options:
    if "NFC-e" in option.text:
        option.click()
        break

# Snapshot antes
snapshot_arquivos = set(os.listdir(pasta_downloads))

wait.until(
    EC.invisibility_of_element_located((By.ID,"loadingModal"))
)

# Pressiona PDF
wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[.span[text()='PDF']]"
    ))
).click()

# Espera conclusao do download:
pdf_path = esperar_downlad(pasta_downloads, snapshot_arquivos, ".pdf")

### Identificar e renomear os arquivos ###
# Novo nome dos arquivos
novo_zip = os.path.join(pasta_downloads, f"NFE_{mes_ref}.zip")
novo_pdf = os.path.join(pasta_downloads, f"NFCe_{mes_ref}.pdf")

# Renomeia os arquivos
os.rename(zip_path, novo_zip)
#os.rename(pdf_file, novo_pdf)

time.sleep(10)

### Enviar para contadora ###
enviar_email(
    remetente = "mariabombomcco@gmail.com",
    senha_app = os.getenv("EMAIL_SENHA"),
    destinatario = "arthurrodrigueslima@gmail.com",
    zip_path = novo_zip,
    pdf_path = novo_pdf
)