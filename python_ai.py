from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from selenium.webdriver.chrome.service import Service as ChromeService


class ChatBot:
    def __init__(self, url: str, view: bool = False, debug: bool = True, incognito:bool=True, executable_path: str ="chromedriver.exe", lang=""):

        self.view = view
        self.debug = debug
        self.name = 'Chatbot Class'
        self.lang = lang
        self.langs = {"fr": ' Répond en Francais',
                      "en": '[Answer in English]', "": "", None: "", "None": ""}
        self.role = ""

        chrome_options = Options()
        if not self.view:
            print("headless")
            chrome_options.add_argument("--headless=new")
        else:
            chrome_options.add_experimental_option("detach", True)
        if incognito:
            chrome_options.add_argument('--incognito')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            options=chrome_options, service=ChromeService(executable_path=executable_path))
        self.driver.get(url)

    def promptify(self, prompt):
        return self.role + " " + prompt + " " + self.langs[self.lang]

    def close(self):
        self.driver.quit()

    def ask(self):
        pass


class youChat(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__("https://you.com/search?q=who+are+you&tbm=youchat&cfr=chat",
                         view=True, *args, **kwargs)
        self.name = 'YouChat'
        time.sleep(1)

    def ask(self, prompt: str = 'Who are you ?'):
        self.driver.find_element(
            By.ID, 'search-input-textarea').send_keys(prompt)
        self.driver.find_element(
            By.ID, 'search-input-textarea').send_keys(Keys.RETURN)
        time.sleep(3)
        stop = self.driver.page_source
        while "Stop generating" in stop:
            time.sleep(1)
            stop = self.driver.page_source
        return self.driver.find_elements(By.XPATH, '/html/body/div/div/div/div[3]/div[2]/section/main/div/div[1]/div[2]/div/div/li/div[1]/div')[-1].text


class CodeAi(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__("https://codepal.ai", *args, **kwargs)
        self.driver.find_element(
            By.XPATH, '//*[@id="termsfeed-com---nb"]/div/div[3]/button[2]').click()

    def set_language(self, langue='python'):
        self.driver.find_element(
            By.ID, "select2-select-language-container").click()
        self.driver.find_element(
            By.XPATH, "/html/body/span/span/span[1]/input").send_keys(langue)
        time.sleep(0.5)
        self.driver.find_element(
            By.ID, 'select2-select-language-results').click()

    def ask(self, prompt=""):
        if prompt not in ["", " ", None]:
            self.driver.find_element(By.ID, 'input-code-description').clear()
        self.driver.find_element(
            By.ID, 'input-code-description').send_keys(prompt)
        self.driver.find_element(By.ID, "btn-generate-code").click()
        time.sleep(10)
        return self.driver.find_element(By.ID, "state-success").text


class ChatAi(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__("https://www.aichatting.net/", *args, **kwargs)
        self.name = "Chat"

    def ask(self, promt):
        self.driver.find_element(
            By.XPATH, '//*[@id="scrollContainer"]/div[2]/div/div[1]/input').send_keys(promt)
        self.driver.find_element(
            By.XPATH, '//*[@id="scrollContainer"]/div[2]/div/div[1]/input').send_keys(Keys.RETURN)
        # time.sleep(10)

        time.sleep(3)
        res = len(self.driver.find_elements(
            By.CLASS_NAME, 'MessageItem_msg__C8oWx')[-1].text)
        time.sleep(1)
        while res < len(self.driver.find_elements(By.CLASS_NAME, 'MessageItem_msg__C8oWx')[-1].text) and self.driver.find_elements(By.CLASS_NAME, 'MessageItem_msg__C8oWx')[-1].text != promt:
            time.sleep(4)
            res = len(self.driver.find_elements(
                By.CLASS_NAME, 'MessageItem_msg__C8oWx')[-1].text)

        # return self.driver.find_elements(By.XPATH, '//*[@id="scrollContainer"]/div[1]/div[7]/div[2]/div[1]')[-1].text
        return self.driver.find_elements(By.CLASS_NAME, 'MessageItem_msg__C8oWx')[-1].text


class LLMA(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__("https://huggingface-projects-llama-2-7b-chat.hf.space/?__theme=dark", *args, **kwargs)
        self.name = 'LLMA'
        time.sleep(1)

    def undo(self):
        self.driver.find_element((By.ID, 'component-10')).click()

    def retry(self):
        self.driver.find_element(By.ID, "component-9").click()
        time.sleep(3)
        res = len(self.driver.find_elements(
            By.XPATH, '//div[@data-testid="bot"]')[-1].text)
        time.sleep(1)
        while res < len(self.driver.find_elements(By.XPATH, '//div[@data-testid="bot"]')[-1].text):
            time.sleep(4)
            res = len(self.driver.find_elements(
                By.XPATH, '//div[@data-testid="bot"]')[-1].text)
        return self.driver.find_elements(By.XPATH, '//div[@data-testid="bot"]')[-1].text

    def get_respnces(self):
        return [i.text for i in self.driver.find_elements(By.XPATH, '//div[@data-testid="bot"]')]

    def ask(self, prompt: str = 'Who are you ?'):

        prompt = self.role+prompt
        # print(prompt)
        self.driver.find_element(
            By.XPATH, '//*[@id="component-11"]/label/textarea').send_keys(prompt)
        self.driver.find_element(
            By.XPATH, '//*[@id="component-11"]/label/textarea').send_keys(Keys.RETURN)
        time.sleep(10)
        """stop = self.driver.page_source
        while "Stop generating" in stop:
            time.sleep(1)
            stop = self.driver.page_source"""
        # res = len(self.driver.find_elements(By.XPATH, '//div[@data-testid="bot"]')[-1].text)
        res = len(self.driver.find_elements(
            By.XPATH, '//*[@id="component-8"]/div[2]/div[2]/div/div[2]/div')[-1].text)

        time.sleep(1)
        while res < len(self.driver.find_elements(By.XPATH, '//*[@id="component-8"]/div[2]/div[2]/div/div[2]/div')[-1].text):
            time.sleep(5)
            res = res = len(self.driver.find_elements(
                By.XPATH, '//*[@id="component-8"]/div[2]/div[2]/div/div[2]/div')[-1].text)

        res = res = self.driver.find_elements(
            By.XPATH, '//*[@id="component-8"]/div[2]/div[2]/div/div[2]/div')[-1].text

        return res


class FreeGPT(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__("https://chataigpt.org/", *args, **kwargs)
        self.name = 'freeGPT'
        time.sleep(1)
        self.driver.find_element(By.ID, "ez-accept-all").click()

        # el = self.driver.find_element(By.XPATH, '//*[@id="vnndvnvjlyxpabujuyysueqwdfbwmybthvhpjwfbmunpdejhkbzxxynf"]')
        el = self.driver.find_element(By.XPATH, '/html/body/div[2]')
        self.driver.execute_script("arguments[0].remove()", el)

    def ask(self, prompt: str = 'Who are you ?'):

        # print(prompt)
        self.driver.find_element(
            By.XPATH, '//*[@id="post-10"]/div/div/div[6]/div/div/div/div/div/div[3]/textarea').send_keys(prompt)
        self.driver.find_element(
            By.XPATH, '//*[@id="post-10"]/div/div/div[6]/div/div/div/div/div/div[3]/textarea').send_keys(Keys.RETURN)
        time.sleep(5)

        res = len(self.driver.find_elements(
            By.CLASS_NAME, 'wpaicg-ai-message')[-1].text)

        time.sleep(1)
        while res < len(self.driver.find_elements(By.CLASS_NAME, 'wpaicg-ai-message')[-1].text):
            time.sleep(5)
            res = res = len(self.driver.find_elements(
                By.CLASS_NAME, 'wpaicg-ai-message')[-1].text)

        res = res = self.driver.find_elements(
            By.CLASS_NAME, 'wpaicg-ai-message')[-1].text

        return res


class EChat(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__("https://echatgpt.org/chat", *args, **kwargs)
        self.name = 'eChat'
        time.sleep(1)

    def ask(self, prompt: str = 'Who are you ?'):

        self.driver.find_element(
            By.CLASS_NAME, 'chatview__textarea-message').send_keys(prompt)
        self.driver.find_element(
            By.CLASS_NAME, 'chatview__textarea-message').send_keys(Keys.RETURN)
        time.sleep(10)

        res = len(self.driver.find_elements(
            By.CLASS_NAME, 'flex-row-reverse')[-1].text)

        time.sleep(1)
        while res < len(self.driver.find_elements(By.CLASS_NAME, 'flex-row-reverse')[-1].text):
            time.sleep(5)
            res = res = len(self.driver.find_elements(
                By.CLASS_NAME, 'flex-row-reverse')[-1].text)

        res = res = self.driver.find_elements(
            By.CLASS_NAME, 'flex-row-reverse')[-1].text

        return res


class MyGPT(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__("https://www.mychatbotgpt.com/", *args, **kwargs)
        self.name = 'MyGPT'
        time.sleep(1)

    def ask(self, prompt: str = 'Who are you ?'):

        # print(prompt)
        self.driver.find_element(
            By.XPATH, '//*[@id="post-10"]/div/div/div[6]/div/div/div/div/div/div[3]/textarea').send_keys(prompt)
        self.driver.find_element(
            By.XPATH, '//*[@id="post-10"]/div/div/div[6]/div/div/div/div/div/div[3]/textarea').send_keys(Keys.RETURN)
        time.sleep(5)

        res = len(self.driver.find_elements(
            By.CLASS_NAME, 'wpaicg-ai-message')[-1].text)

        time.sleep(1)
        while res < len(self.driver.find_elements(By.CLASS_NAME, 'wpaicg-ai-message')[-1].text):
            time.sleep(5)
            res = res = len(self.driver.find_elements(
                By.CLASS_NAME, 'wpaicg-ai-message')[-1].text)

        res = res = self.driver.find_elements(
            By.CLASS_NAME, 'wpaicg-ai-message')[-1].text

        return res


if __name__ == '__main__':
    chat = FreeGPT()


    command = input(">")
    while command not in ("q", "quit", "exit"):
        print(chat.ask(b))
        command = input(">")
    print("Bye")
    chat.close()
