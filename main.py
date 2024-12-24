from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import time
from dotenv import load_dotenv
import os
from groq import Groq 
import re
from template import *

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "mixtral-8x7b-32768"

class CoderAgent:
    def __init__(self, GROQ_API_KEY):
        self.client = Groq(
            api_key=GROQ_API_KEY,
        )
        self.controller = Controller()
        
    def __extract__(self, response):
        match = re.search(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return response
        
    def __response__(self, code: str, comment=True):
        if comment:
            prompt = COMMENT_TEMPLATE.substitute(code=code)
        else:
            prompt = REMOVE_COMMENT_TEMPLATE.substitute(code=code)
        
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL_NAME,
            timeout=25,
        )
        return self.__extract__(response.choices[0].message.content)
    
    def __remove__(self):
        with self.controller.pressed(Key.ctrl):
            self.controller.tap('c')
        time.sleep(0.4)
        
        text = pyperclip.paste()
        pyperclip.copy(self.__response__(text, False))
        
        time.sleep(0.2)
        with self.controller.pressed(Key.ctrl):
            self.controller.tap('v')

    def __comment__(self):        
        with self.controller.pressed(Key.ctrl):
            self.controller.tap('c')
        time.sleep(0.4)
        
        text = pyperclip.paste()
        pyperclip.copy(self.__response__(text, True))
        
        time.sleep(0.2)
        with self.controller.pressed(Key.ctrl):
            self.controller.tap('v')
    
    def __select_all__(self):
        self.controller.press(Key.ctrl)
        self.controller.tap('a')
        self.controller.release(Key.ctrl)
    
    def __f7__(self):
        self.__select_all__()
        self.__remove__()
        
    def __f8__(self):
        self.__remove__()
        
    def __f9__(self):
        self.__comment__()    
    
    def __f10__(self):
        self.__select_all__()
        self.__comment__()
    
    def __run__(self):
        with keyboard.GlobalHotKeys({
                '<118>': self.__f7__,
                '<119>': self.__f8__,
                '<120>': self.__f9__,
                '<121>': self.__f10__
            }) as h:
            h.join()
            
if __name__ == "__main__":
    load_dotenv()
    agent = CoderAgent(GROQ_API_KEY)
    agent.__run__()