from operator import index
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

navegador = webdriver.Chrome()
navegador.get("https://www.google.com")

# ACHANDO COTAÇAO DO DÓLAR
navegador.find_element(
    By.XPATH, r"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys("cotação dólar")
navegador.find_element(
    By.XPATH, r"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(Keys.ENTER)
cotacaoDolar = navegador.find_element(
    By.XPATH, r'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cotacaoDolar)

# ACHANDO COTAÇAO DO EURO
navegador.find_element(
    By.XPATH, r'//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').clear()
navegador.find_element(
    By.XPATH, r'//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element(
    By.XPATH, r'//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys(Keys.ENTER)
cotacaoEuro = navegador.find_element(
    By.XPATH, r'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cotacaoEuro)

# PEGANDO COTAÇAO OURO
navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacaoOuro = navegador.find_element(
    By.XPATH, '//*[@id="comercial"]').get_attribute("value")
cotacaoOuro = cotacaoOuro.replace(",", ".")
print(cotacaoOuro)


# SAINDO DO NAVEGADOR
navegador.quit()

# USANDO BASE DE DADOS

tabela = pd.read_excel("Produtos.xlsx")

tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacaoDolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacaoEuro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacaoOuro)

tabela["Preço de Compra"] = tabela["Preço Original"] * tabela["Cotação"]
tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

tabela.to_excel("ProdutosNovos.xlsx", index=False)
