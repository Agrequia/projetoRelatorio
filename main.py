from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get("https://localhost:8080/HAND/")

input("Pressione Enter para fechar...")
driver.quit()