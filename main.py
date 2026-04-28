from selenium import webdriver
from selenium.webdriver.firefox.service import Service

service = Service(executable_path="geckodriver.exe")

driver = webdriver.Firefox(service=service)
driver.get("http://localhost")

input("Pressione Enter para fechar...")
driver.quit()