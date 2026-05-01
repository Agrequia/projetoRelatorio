from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from datetime import datetime, timedelta
import time
import os

def estaLogado(driver):
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

# Formata no padrao dd/mm/yyyy
data_inicio = primeiro_dia_mes_anterior.strftime("%d/%m/%Y")
data_fim = ultimo_dia_mes_anterior.strftime("%d/%m/%Y")

# Acessa o hand
driver.get("https://localhost:8080/HAND/")
time.sleep(3)

if not estaLogado(driver):
    print("Não está logado! Realizando login...")

    # Preenche o login
    driver.find_element(By.XPATH, "//input[@placeholder='Login']").send_keys("6")

    # Preenche a senha + Enter
    driver.find_element(By.XPATH, "//input[@placeholder='Senha']").send_keys("6" + Keys.ENTER)

    time.sleep(3)

# Acessa a página onde sera configurado o relatório
driver.get("https://localhost:8080/HAND/pages/nfe/gerenciamento/search/searchGerenciamentoNfe.xhtml")

time.sleep(3)

# Configura o primeiro relatório
dropDown = Select(driver.find_element(By.NAME, "j_idt93:j_idt94"))
dropDown.select_by_visible_text("NFC-e")

time.sleep(3)

# Limpa e insere periodo inicial e final
# Periodo inicial
campo_inicio = driver.find_element(By.NAME, "j_idt100:dtInicio:dtInicio_input")
campo_inicio.clear()
campo_inicio.send_keys(data_inicio)

time.sleep(3)

# Periodo final
campo_fim = driver.find_element(By.NAME, "j_idt100:dtFim:dtFim_input")
campo_fim.clear()
campo_fim.send_keys(data_fim)

time.sleep(3)

# Pressiona botao pesquisar
driver.find_element(By.ID, "btnPesquisar").click()

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

time.sleep(3)

# Pressiona exportar notas
driver.find_element(By.ID, "j_idt332").click()

time.sleep(10)

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

time.sleep(5)

### Identificar e renomear os arquivos ###
# Local dos arquivos baixados
pasta_downloads = r"C:\Users\Usuario\Downloads"

# Função que obtem os arquivos mais recentes
arquivos = obtem_arquivos_recentes(pasta_downloads)

# Separa os arquivos em duas variaveis
zip_file = next(f for f in arquivos if f.endswith(".zip"))
pdf_file = next(f for f in arquivos if f.endswith(".pdf"))



### Enviar para contadora ###

