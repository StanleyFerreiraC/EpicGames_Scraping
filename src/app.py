import requests
import csv
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip


def setup_driver(headless=False, user_data_dir=None):
    """
    Configura o driver do Chrome com as opções especificadas.
    Argumentos:
        headless (bool): Indica se o navegador será executado em modo headless.
        user_data_dir (str): Caminho do diretório de dados do usuário, se aplicável.
    Retorna:
        driver: Instância configurada do WebDriver.
    """
    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    
    if headless:
        chrome_options.add_argument("--headless")
    if user_data_dir:
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        
    
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def scrape_data():
    """
    Extraí dados sobre jogos gratuitos na Epic Games Store.
    """
    url = "https://store.epicgames.com/pt-BR/free-games"
    driver = setup_driver(headless=True)
    driver.get(url)

    games = []
    game_containers = driver.find_elements(By.XPATH, "//div[@data-component='VaultOfferCard']")
    
    for container in game_containers:
        try:
            if container.find_element(By.CLASS_NAME, "css-1p5cyzj-ROOT"):
                game_name = container.find_element(By.XPATH, ".//h6").text
                offer_period = container.find_element(By.XPATH, ".//p").text.replace("Grátis - ", "").replace(". às", " as")
                store_link = container.find_element(By.XPATH, "./a").get_attribute("href")
                logo_link = container.find_element(By.XPATH, ".//img").get_attribute("src")
                
                if check_duplicate(game_name, offer_period):
                    continue

                games.append({
                    'game_name': game_name,
                    'offer_period': offer_period,
                    'store_link': store_link,
                    'date_written': str(date.today()),
                    'logo_link': logo_link
                })
        except NoSuchElementException:
            print("Elemento esperado não encontrado no contêiner.")

    driver.quit()
    
    if len(games) == 0:
        print("Nenhum jogo gratuito encontrado na Epic Games Store.")
        return
    
    write_data(games)
    wpp_message(games)
    


def check_duplicate(game_name, offer_period):
    """
    Verifica duplicatas de jogos no arquivo CSV.
    """
    fieldnames = ['game_name', 'offer_period', 'store_link', 'date_written', 'logo_link']
    try:
        with open('historico_jogos.csv', 'r', newline='') as f:
            reader = csv.DictReader(f, fieldnames=fieldnames)
            for line in reader:
                if line['game_name'] == game_name and line['offer_period'] == offer_period:
                    return True
    except FileNotFoundError:
        pass  # Arquivo ainda não existe.
    return False


def write_data(games):
    """
    Escreve os dados dos jogos em um arquivo CSV.
    """
    fieldnames = ['game_name', 'offer_period', 'store_link', 'date_written', 'logo_link']
    with open('H:\Projetos\EpicGames\EpicGames_Scraping\src\historico_jogos.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for game in games:
            writer.writerow(game)


def wpp_message(games):
    """
    Envia mensagens no WhatsApp com os dados dos jogos gratuitos.
    """
    driver = setup_driver(user_data_dir="C:/Users/stanl/AppData/Local/Google/Chrome/User Data")
    driver.get('https://web.whatsapp.com')

    search_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "x1hx0egp x6ikm8r x1odjw0f x6prxxf x1k6rcq7 x1whj5v")]'))
)
    search_box.click()
    search_box.send_keys('Os MORCEGÃO')
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)

    for game in games:
        send_game_message(driver, game)
        
    driver.quit()


def send_game_message(driver, game):
    """
    Envia uma mensagem formatada no WhatsApp com os detalhes de um jogo.
    """
    message = f"Jogo: {game['game_name']}\nOferta válida até: {game['offer_period']}\nLink: {game['store_link']}\n\n"
    pyperclip.copy(message)

    message_box = driver.find_element(By.XPATH, '//div[contains(@class, "x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf")]')
    message_box.click()
    message_box.send_keys(Keys.CONTROL + 'v')
    time.sleep(0.2)

    # Lista de comandos para enviar menções no WhatsApp
    mentions = ['@G','@S']

    for mention in mentions:
        message_box.send_keys(f' {mention}')
        time.sleep(0.1)
        message_box.send_keys(Keys.TAB)
        time.sleep(0.1)

    message_box.send_keys(Keys.ENTER)
    time.sleep(1)

if __name__ == '__main__':
    scrape_data()
