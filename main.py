from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
import time

service = Service(executable_path="geckodriver.exe")
driver = webdriver.Firefox(service=service)

driver.get("https://localhost:8080/HAND/")

time.sleep(3)

# Preenche o login
driver.find_element(By.XPATH, "//input[@placeholder='Login']").send_keys("6")

# Preenche a senha + Enter
driver.find_element(By.XPATH, "//input[@placeholder='Senha']").send_keys("6" + Keys.ENTER)

time.sleep(5)

# Acessa a página onde sera configurado o relatório
driver.get("https://localhost:8080/HAND/pages/nfe/gerenciamento/search/searchGerenciamentoNfe.xhtml")