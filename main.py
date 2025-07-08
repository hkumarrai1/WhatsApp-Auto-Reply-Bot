from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import json#type:ignore
import os
from dotenv import load_dotenv#type:ignore


load_dotenv()

def get_ai_reply(message_text):#type:ignore
    """Generate AI reply using SambaNova API"""
    try:
        print(f"Calling AI with message: {message_text}")  # Debug
        
        url = "https://api.sambanova.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('SAMBANOVA_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {#type:ignore
            "model": "Meta-Llama-3.1-8B-Instruct",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful WhatsApp assistant. Reply in a friendly, Shyrana humilating way. Keep responses short."
                },
                {
                    "role": "user", 
                    "content": message_text
                }
            ],
            "max_tokens": 50
        }
        
        response = requests.post(url, headers=headers, json=data)#type:ignore
        print(f"API response status: {response.status_code}")  # Debug
        
        ai_reply = response.json()["choices"][0]["message"]["content"]
        return ai_reply.strip()
        
    except Exception as e:
        print(f"AI API error: {e}")  # Debug
        return "Thanks for your message! I'll get back to you soon."


options = Options()
options.add_argument("--user-data-dir=C:\\temp\\edge_profile")#type:ignore

driver=webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()),options=options)

driver.get("https://web.whatsapp.com")

time.sleep(10)

input("Open a chat and press Enter to continue...")

messages = driver.find_elements(By.CSS_SELECTOR, ".message-in")
initial_count = len(messages)
print(f"Initial messages: {initial_count}")

start_time=time.time()

while True:
    time.sleep(2)
    
    try:
        current_messages = driver.find_elements(By.CSS_SELECTOR, ".message-in")
        current_count = len(current_messages)
        print(f"Current: {current_count}, Initial: {initial_count}")
        
        if current_count > initial_count:
            print("New message detected!")
            new_message = current_messages[-1]
            message_text = new_message.text
            print(f"Message text: {message_text}")

            try:
                input_box = driver.find_element(By.XPATH, "//div[@role='textbox'][@data-tab='10']")
                print("Found message input box!")
                
                # Step 2: Type a reply message
                reply_text =get_ai_reply(message_text)
                print(f"AI returned: '{reply_text}'")  # Debug print
                if reply_text:  # Only send if we have a reply
                    input_box.send_keys(reply_text)#type:ignore
                    print(f"Typed reply: {reply_text}")#type:ignore
                    time.sleep(1)
                    input_box.send_keys(Keys.ENTER)#type:ignore
                    print("Message sent!")
                else:
                    print("No reply text received from AI!")
                
            except:
                try:
                    input_box = driver.find_element(By.CSS_SELECTOR, "div[data-tab='10']")
                    print("Found input box with method 2!")
                    input_box.send_keys("This is an auto-reply!")#type:ignore
                    input_box.send_keys(Keys.ENTER)#type:ignore
                    print("Message sent!")
                except:
                    print("Could not find message input box!")

            initial_count = current_count
            
    except Exception as e:
        print(f"Error: {e}")
        print("Browser connection lost!")
        break
        
    # Stop after 5 minutes
    if time.time() > start_time + 300:
        break

print("Script finished.")
input("Press Enter to close browser...")   

driver.quit()