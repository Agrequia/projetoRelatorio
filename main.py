from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException 
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
else:
    # Acessa a página onde sera configurado o relatório
    driver.get("https://localhost:8080/HAND/pages/nfe/gerenciamento/search/searchGerenciamentoNfe.xhtml")