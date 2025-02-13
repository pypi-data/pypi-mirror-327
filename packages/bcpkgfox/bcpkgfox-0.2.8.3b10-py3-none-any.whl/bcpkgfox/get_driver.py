from .find_elements import backcode__dont_use__find_element_with_wait_backcode, By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium import webdriver
from typing import Optional

import undetected_chromedriver as uc

import subprocess
import requests
import logging
import random
import time
import sys
import os

class Webdriver:
    def __init__(self,
        version: Optional[str | int] = "latest",
        subprocess: Optional[bool] = False,
        Selenoid: Optional[str] = None,
        Navegador: Optional[str] = "Chrome"
        ):

        global driver
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
        )
        self.version_main = self._get_chrome_version() if version == "latest" else version
        self.options = uc.ChromeOptions()
        self.subprocess = subprocess
        self.selenoid = Selenoid
        self.nav = Navegador

        self.captcha_api_key = None
        self.extension_path = None
        self.captcha_name = None
        self.driver = None

        self.arguments = self.Arguments(self)

    def initialize_driver(self,
        maximize: Optional[bool] = True
        ):

        if self.selenoid:
            if self.nav.lower() == "firefox":
                self.options = webdriver.FirefoxOptions()
            elif self.nav.lower() == "opera":
                self.options = webdriver.OperaOptions()
            else:
                self.options = webdriver.ChromeOptions()

            self.options.set_capability("browserVersion", "128.0")
            self.options.set_capability("selenoid:options", {"enableVNC": True})

            self.driver = webdriver.Remote(
                command_executor='http://host.docker.internal:4444/wd/hub',
                options=self.options,
            )

        else:
            if self.nav.lower() in ["ie", "internet_explorer", "internet explorer", "explorer"]:
                self.driver = webdriver.Ie()
            elif self.nav.lower() == "edge":
                self.driver = webdriver.Edge()
            else:
                self.driver = uc.Chrome(
                    options=self.options,
                    version_main=self.version_main,
                    use_subprocess=self.subprocess
                )
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        if maximize: self.driver.maximize_window()
        return self.driver

    def add_extension(self, extension_folder: str,
        config: Optional[bool] = False,
        key: Optional[str|int] = None
        ):
        """ Inicia o navegador com uma extensão, o 'config' ele identifica o nome da pasta e se for uma conhecida (capmonster, twocaptcha) configura automaticamente

        - OBS: Caso a extensão precise de alguma KEY, declare ela também na variavel "key"

        - Exemplo: add_extension("capmonster", config=True)"""
        try:
            extensao_caminho = self.__resource_path(extension_folder)
            if not os.path.exists(extensao_caminho): extensao_caminho = os.path.abspath(extension_folder)
            self.arguments.add_new_argument(f'--load-extension={extensao_caminho}')
        except Exception as e:
            logging.error("Erro ao verificar pasta da extensão", exc_info=True)
            raise SystemError("Verificar pasta da extensão") from e

        if key:
            key = str(key) ; cap_monster_names = ["capmonster", "captchamonster", "monster", "cap-monster", "captcha monster", "captcha-monster", "cmonster", "cap monster"]
            for name in cap_monster_names:
                if name in extension_folder.lower(): self._config_capmonster(key)

    @staticmethod
    def _get_chrome_version() -> int:
        """Obtém a versão do Chrome instalada no sistema e retorna a versão principal (int)."""
        try:
            version_str = None
            if os.name == 'nt':
                try:
                    cmd = ['reg', 'query', r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome', '/v', 'DisplayVersion']
                    result = subprocess.check_output(cmd, universal_newlines=True)
                except subprocess.CalledProcessError:
                    try:
                        cmd = ['reg', 'query', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome', '/v', 'DisplayVersion']
                        result = subprocess.check_output(cmd, universal_newlines=True)
                    except subprocess.CalledProcessError:
                        raise SystemError("Não foi possível obter a versão do Chrome")
                version_str = result.split()[-1]
            elif os.name == 'posix':
                version_str = subprocess.check_output(
                    ['google-chrome', '--version'], stderr=subprocess.PIPE, text=True
                ).strip()
                version_str = version_str.split()[-1]
            return int(version_str.split('.')[0])
        except Exception as e:
            logging.error("Erro ao obter versão do Chrome", exc_info=True)
            raise SystemError("Não foi possível obter a versão do Chrome") from e

    def _config_capmonster(self, api_key: str) -> None:
        self.driver.get("chrome://extensions/") ; time.sleep(5)

        # Shadow-doom
        id_extension = self.driver.execute_script("""
            return document.querySelector('extensions-manager')
            .shadowRoot.querySelector('extensions-item-list')
            .shadowRoot.querySelector('extensions-item').id;
        """) ; print("ID extensão extraido:", id_extension)

        self.driver.get(f"chrome-extension://{id_extension.lower()}/popup.html")

        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.ID, "client-key-input").send_keys(api_key) ; time.sleep(2.5)
        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.XPATH, '//label[span[input[@id="captcha-radio-token-ReCaptcha2"]]]').click()
        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.ID, "client-key-save-btn").click()
        print(" - Capmonter configurado.")

    @staticmethod
    def __resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def __check_selenoid_connection(selenoid_url: str):
        try:
            response = requests.get(selenoid_url)
            if response.status_code != 200:
                raise ConnectionError(f"Falha na conexão com o Selenoid. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise SystemError(f"Erro ao conectar ao servidor do Selenoid: {e}")

    class Arguments:
        def __init__(self, self_bot):
            self.web = self_bot
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
            )

        def add_new_argument(self, Args: str | list):
            """ Coloque apenas o argumento que você quer adicionar a inicialização do driver.

            - Exemplo único: add_new_argument("--headless")

            - Exemplo composto: add_new_argument(["--headless", "--disable-gpu", ... ])"""

            if isinstance(Args,list) == True:
                for arg in Args: self.web.options.add_argument(arg)
            else: self.web.options.add_argument(Args)

        def add_experimental_new_option(self, Args: str | list):
            """ Coloque apenas o argumento que você quer adicionar a inicialização do driver.

            - Exemplo: add_experimental_new_option("prefs", profile)"""

            if isinstance(Args, list) == True:
                for arg in Args: self.web.options.add_experimental_option [arg]
            else: self.web.options.add_experimental_option[Args]

    class Selenoid:
        def __init__(self, self_bot):
            self.web = self_bot
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
            )
            self.capabilities = DesiredCapabilities.CHROME.copy()

        def add_capabilities(self, capabilities: str | list):

            if isinstance(capabilities, list) == True:
                for cap in capabilities: self.web.options.add_experimental_option [arg]
            else: self.web.options.add_experimental_option[Args]


            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities["browserName"] = "chrome"
            capabilities["version"] = "122.0"  # Verifique a versão instalada no Selenoid
            capabilities["enableVNC"] = True  # Para visualizar a execução no Selenoid UI

            # Conectar ao Selenium Hub (Selenoid)
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                desired_capabilities=capabilities
            )

            # Abrir um site de teste
            driver.get("https://www.google.com")

            # Manter o navegador aberto por alguns segundos
            import time
            time.sleep(10)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def backcode__dont_use__set_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

def backcode__dont_use__launch_browser(download_dir: str, extension_path, captcha_name, captcha_api_key) -> WebElement:
    global driver

    # Configurações para o Chrome
    options = uc.ChromeOptions()

    # Alterar o User-Agent
    options.add_argument(f"user-agent={backcode__dont_use__set_user_agent()}")

    # Default's
    profile = {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'download.default_directory': download_dir,
    }
    options.add_experimental_option('prefs', profile)

    # Configurações para reduzir detecção
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')

    if extension_path:
        extensao_caminho = resource_path(extension_path)
        if not os.path.exists(extensao_caminho):
            extensao_caminho = os.path.abspath(extension_path)

        options.add_argument(f'--load-extension={extensao_caminho}')

    # options.add_argument('--disable-extensions') # Fix: Possibilita ter extensões ou não, nunca influenciou na detecção

    # Inicializar o navegador com undetected_chromedriver
    driver = uc.Chrome(options=options, use_subprocess=True)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if captcha_name:
        cap_monster_names = ["capmonster", "captchamonster", "monster", "cap-monster", "captcha monster", "captcha-monster", "cmonster", "cap monster"]

        for name in cap_monster_names:
            if captcha_name.lower() == name:
                backcode__dont_use__capmonster(captcha_api_key)

    driver.maximize_window()
    return driver

def backcode__dont_use__get(driver, link) -> WebElement:
    driver.get(link)

def backcode__dont_use__capmonster(api_key) -> None:
    global driver

    driver.get("chrome://extensions/")
    time.sleep(5)

    # Pega por JS pois está dentro da shadow
    id_extension = driver.execute_script("""
        return document.querySelector('extensions-manager')
        .shadowRoot.querySelector('extensions-item-list')
        .shadowRoot.querySelector('extensions-item').id;
    """)

    print("ID extensão extraido:", id_extension)
    driver.get(f"chrome-extension://{id_extension.lower()}/popup.html")

    backcode__dont_use__find_element_with_wait_backcode(driver, By.ID, "client-key-input").send_keys(api_key)
    time.sleep(2.5)
    backcode__dont_use__find_element_with_wait_backcode(driver, By.XPATH, '//label[span[input[@id="captcha-radio-token-ReCaptcha2"]]]').click() # icone salvar
    backcode__dont_use__find_element_with_wait_backcode(driver, By.ID, "client-key-save-btn").click() # icone salvar
    print(" - Capmonter configurado.")