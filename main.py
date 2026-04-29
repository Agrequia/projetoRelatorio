from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import Select
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

driver.get("https://localhost:8080/HAND/")
time.sleep(3)

if not estaLogado(driver):
    print("Não está logado! Realizando login...")

    # Preenche o login
    driver.find_element(By.XPATH, "//input[@placeholder='Login']").send_keys("6")

    # Preenche a senha + Enter
    driver.find_element(By.XPATH, "//input[@placeholder='Senha']").send_keys("6" + Keys.ENTER)

    time.sleep(5)

# Acessa a página onde sera configurado o relatório
driver.get("https://localhost:8080/HAND/pages/nfe/gerenciamento/search/searchGerenciamentoNfe.xhtml")

time.sleep(3)

# Configura o primeiro relatório
dropDown = Select(driver.find_element(By.NAME, "j_idt93:j_idt94"))
dropDown.select_by_visible_text("NFC-e")

time.sleep(3)

# Encontra o período para gerar o relatorio (primeiro e ultimo dia do mes anterior ao que nos encontramos)
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

driver.find_element(By.ID, "btnPesquisar").click()