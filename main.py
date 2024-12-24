from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import time
from dotenv import load_dotenv
import os
from groq import Groq 
import re
from template import *

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "mixtral-8x7b-32768"

client = Groq(
    api_key=GROQ_API_KEY,
)

controller = Controller()

def extract_code(response):
    match = re.search(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return response

def comment_code(text):
    prompt = COMMENT_TEMPLATE.substitute(code=text)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL_NAME,
        timeout=120,
    )
    return extract_code(response.choices[0].message.content)

def decomment_code(text):
    prompt = REMOVE_COMMENT_TEMPLATE.substitute(code=text)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL_NAME,
        timeout=120,
    )
    return extract_code(response.choices[0].message.content)

def worker_commenter():
    controller.press(Key.ctrl)
    controller.tap('a')
    
    controller.release(Key.ctrl)
    comment_selection()

def comment_selection():
    with controller.pressed(Key.ctrl):
        controller.tap('c')
    time.sleep(0.4)
    
    text = pyperclip.paste()
    pyperclip.copy(comment_code(text))
    
    time.sleep(0.2)
    with controller.pressed(Key.ctrl):
        controller.tap('v')

def on_f9():
    comment_selection()

def on_f10():
    worker_commenter()
        
def worker_remover():
    controller.press(Key.ctrl)
    controller.tap('a')

    controller.release(Key.ctrl)
    remove_comment()
    
def remove_comment():
    with controller.pressed(Key.ctrl):
        controller.tap('c')
    time.sleep(0.4)
    
    text = pyperclip.paste()
    pyperclip.copy(decomment_code(text))
    
    time.sleep(0.2)
    with controller.pressed(Key.ctrl):
        controller.tap('v')

def on_f7():
    worker_remover()

with keyboard.GlobalHotKeys({
        '<118>': on_f7,
        '<120>': on_f9,
        '<121>': on_f10
        }) as h:
    h.join()