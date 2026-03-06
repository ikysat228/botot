import os
import time
import speech_recognition as sr
import pyautogui
import pyttsx3
import pytesseract
from groq import Groq
from PIL import Image

# Вкажи шлях до встановленого Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ================= НАЛАШТУВАННЯ =================
GROQ_API_KEY = "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"
MIC_INDEX = 1
MODEL_ID = "llama-3.3-70b-versatile"
WAKE_WORD = "саня"

engine = pyttsx3.init()
engine.setProperty('rate', 190)

def speak(text):
    print(f"Асистент: {text}")
    engine.say(text)
    engine.runAndWait()

client = Groq(api_key=GROQ_API_KEY)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=MIC_INDEX) as source:
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Слухаю...")
            audio = r.listen(source, timeout=10, phrase_time_limit=12)
            return r.recognize_google(audio, language="uk-UA").lower()
        except: return ""

def analyze_screen():
    """Робить скріншот і перетворює його на текст з координатами"""
    screenshot = pyautogui.screenshot()
    data = pytesseract.image_to_data(screenshot, lang='ukr+eng', output_type=pytesseract.Output.DICT)
    # Повертаємо список слів та їх координат
    screen_content = []
    for i in range(len(data['text'])):
        if data['text'][i].strip():
            screen_content.append(f"{data['text'][i]} ({data['left']},{data['top']})")
    return " ".join(screen_content)[:2000] # Обмежуємо обсяг для ШІ

def ask_ai(command, screen_context=""):
    """Головний мозок: планування дій"""
    prompt = f"""
    Ти — ШІ-агент. На екрані зараз є такий текст: {screen_context}
    Користувач каже: "{command}"
    
    Видай ланцюжок команд через кому:
    SEARCH [назва] - знайти і відкрити програму через Windows Search
    TYPE [текст] - надрукувати текст
    WAIT [сек] - зачекати
    CLICK_TEXT [слово] - знайти слово на екрані і клікнути
    PRESS [клавіша] - натиснути клавішу (наприклад, enter, win, space)
    CHAT [відповідь] - якщо треба просто щось сказати
    
    Приклад (відкрий блокнот і напиши анекдот): 
    SEARCH блокнот, WAIT 2, TYPE Ось мій анекдот: Чому ШІ не спить? Бо в нього немає ліжок!, PRESS enter
    """
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_ID,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e: return f"CHAT Помилка: {e}"

def execute_chain(chain):
    """Виконує список команд по черзі"""
    actions = chain.split(",")
    for action in actions:
        action = action.strip()
        print(f"Виконую: {action}")
        
        if action.startswith("SEARCH"):
            app = action.replace("SEARCH", "").strip()
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(app, interval=0.1)
            time.sleep(0.5)
            pyautogui.press('enter')
            
        elif action.startswith("TYPE"):
            text = action.replace("TYPE", "").strip()
            pyautogui.write(text, interval=0.05)
            
        elif action.startswith("WAIT"):
            sec = int(action.replace("WAIT", "").strip())
            time.sleep(sec)
            
        elif action.startswith("PRESS"):
            key = action.replace("PRESS", "").strip().lower()
            pyautogui.press(key)

        elif action.startswith("CLICK_TEXT"):
            # Тут можна додати логіку пошуку координат через pytesseract
            speak("Шукаю об'єкт на екрані")
            
        elif action.startswith("CHAT"):
            speak(action.replace("CHAT", "").strip())

# ================= ЦИКЛ =================
if __name__ == "__main__":
    speak("Джарвіс на зв'язку. Я готовий до складних завдань.")
    
    while True:
        voice = get_audio()
        if voice and WAKE_WORD in voice:
            cmd = voice.split(WAKE_WORD)[-1].strip()
            if not cmd:
                speak("Слухаю вас")
                cmd = get_audio()
            
            if cmd:
                if "стоп" in cmd: break
                
                # Якщо команда вимагає знання про екран
                context = ""
                if "екран" in cmd or "що там" in cmd or "клікни" in cmd:
                    speak("Аналізую екран")
                    context = analyze_screen()
                
                res = ask_ai(cmd, context)
                execute_chain(res)