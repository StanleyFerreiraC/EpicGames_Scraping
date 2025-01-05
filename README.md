# Epic Games Free Games Scraper

Este projeto é um script automatizado que extrai informações sobre jogos gratuitos disponíveis na Epic Games Store. Ele também envia mensagens no WhatsApp com os detalhes dos jogos extraídos, utilizando o Selenium e a API do WebDriver.

## Funcionalidades

- Coleta informações sobre jogos gratuitos na Epic Games Store, incluindo:
  - Nome do jogo
  - Período da oferta
  - Link para a loja
  - Link para o logo do jogo
- Verifica duplicatas no arquivo CSV para evitar entradas repetidas.
- Escreve os dados extraídos em um arquivo CSV.
- Envia mensagens formatadas via WhatsApp com os detalhes dos jogos.

## Requisitos

Certifique-se de ter as seguintes dependências instaladas:

### Python
- Python 3.7 ou superior

### Bibliotecas Python
- `requests`
- `csv`
- `time`
- `selenium`
- `pyperclip`
- `webdriver_manager`

Você pode instalar as dependências com o seguinte comando:

```bash
pip install requests selenium pyperclip webdriver-manager
```

### Outros Requisitos
- Google Chrome instalado.
- Diretório de dados do usuário do Chrome configurado (para autenticação no WhatsApp Web).

## Configuração

1. **Caminho do executável do Chrome**: Certifique-se de que o caminho do Chrome esteja corretamente configurado no script. Altere a linha:

```python
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
```

2. **Diretório de dados do usuário**: Defina o caminho correto do diretório de dados do usuário para o WebDriver no método `setup_driver`:

```python
user_data_dir="C:/Users/SEU_USUARIO/AppData/Local/Google/Chrome/User Data"
```

3. **Destino do arquivo CSV**: Atualize o caminho do arquivo CSV para onde os dados serão salvos:

```python
with open('H:/Projetos/EpicGames/dags/EGS_Data.csv', 'a', newline='') as f:
```

4. **Grupo do WhatsApp**: Certifique-se de que o grupo ou contato está corretamente especificado:

```python
search_box.send_keys('Os MORCEGÃO')
```

## Como Usar

1. Clone este repositório para sua máquina local:

```bash
git clone https://github.com/seuusuario/epic-games-scraper.git
```

2. Navegue até o diretório do projeto:

```bash
cd epic-games-scraper
```

3. Execute o script:

```bash
python main.py
```

## Estrutura do Projeto

- **`setup_driver`**: Configura o WebDriver do Chrome.
- **`scrape_data`**: Realiza a extração de dados da Epic Games Store.
- **`check_duplicate`**: Verifica duplicatas no arquivo CSV.
- **`write_data`**: Salva os dados extraídos em um arquivo CSV.
- **`wpp_message`**: Envia mensagens formatadas no WhatsApp com os detalhes dos jogos.
- **`send_game_message`**: Formata e envia uma mensagem para um contato ou grupo.

## Notas Importantes

- **Autenticação no WhatsApp**: Certifique-se de estar autenticado no WhatsApp Web antes de usar a funcionalidade de envio de mensagens.
- **Modo Headless**: O navegador pode ser configurado para rodar em modo "headless" (sem interface gráfica) para operações silenciosas.
- **Erros de Seletores**: Caso o layout do site ou do WhatsApp Web mude, os seletores XPath podem precisar ser ajustados.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um issue ou enviar um pull request com melhorias.

