from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from datetime import datetime, timedelta
import time

def estaLogado(driver):
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'NF-e')]")
        return True
    except NoSuchElementException:
        return False

service = Service(executable_path="geckodriver.exe")
driver = webdriver.Firefox(service=service)
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

time.sleep(3)

### Fim da geração do primeiro arquivo, inicio do proximo ###

# Acessa a página onde sera configurado o segundo relatório
driver.get("https://localhost:8080/HAND/pages/entrada/porNota/search/searchEntradaPorNota.xhtml")
time.sleep(3)

# Configura o modelo de relatório
dropDown = Select(driver.find_element(By.NAME, "j_idt304:j_idt305"))
dropDown.select_by_visible_text("Nota Fiscal de Consumidor Eletronica ")

time.sleep(3)

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

# Pressiona botao pesquisar
driver.find_element(By.ID, "btnSalvarCadastro").click()