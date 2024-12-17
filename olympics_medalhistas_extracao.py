from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurações do navegador
url = "https://olympics.com/pt/paris-2024/medalhas/medalhistas"
option = Options()
option.headless = False
driver = webdriver.Chrome(options=option)

try:
    driver.get(url) #Acessa a página

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
        print("Aceitou os cookies.")
    except Exception as e:
        print("Botão de cookies não encontrado ou já aceito:", e)

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='emotion-srm-uu0gdl']"))
    ) # Aguarda o elemento desejado estar clicável
    element.click()
    print("Elemento clicado com sucesso.")

except Exception as e:
    print("Ocorreu um erro:", e)

finally:
    time.sleep(5)  # Para visualização do resultado
    driver.quit()
