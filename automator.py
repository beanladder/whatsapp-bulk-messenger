from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

# Setup Chrome options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=C:/temp/chrome_user_data")  # Adjust path for Windows

# Suppress WDM logs
os.environ["WDM_LOG_LEVEL"] = "0"

# Custom styling class for terminal output
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Terminal welcome message
print(style.BLUE)
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****      This tool was built by Anirudh Bagri     ******")
print("*****           www.github.com/anirudhbagri         ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(style.RESET)

# Reading message from message.txt
f = open("message.txt", "r", encoding="utf8")
message = f.read()
f.close()

print(style.YELLOW + '\nThis is your message:')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)  # Encode message for URL

# Reading phone numbers from numbers.txt
numbers = []
f = open("numbers.txt", "r")
for line in f.read().splitlines():
    if line.strip() != "":
        numbers.append(line.strip())
f.close()

total_number = len(numbers)
print(style.RED + f'We found {total_number} numbers in the file' + style.RESET)
delay = 30  # Delay in seconds before each message is sent

# Initialize Chrome WebDriver with the correct ChromeDriver version
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open WhatsApp Web and wait for user to log in
print('Once your browser opens up, sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
input(style.MAGENTA + "AFTER logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

# Sending messages to each number
for idx, number in enumerate(numbers):
    number = number.strip()
    if number == "":
        continue
    print(style.YELLOW + f'{idx+1}/{total_number} => Sending message to {number}.' + style.RESET)
    try:
        url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
        sent = False
        for i in range(3):  # Try sending message 3 times
            if not sent:
                driver.get(url)
                try:
                    # Wait for the send button to become clickable
                    click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']")))
                except Exception as e:
                    print(style.RED + f"\nFailed to send message to: {number}, retry ({i+1}/3)")
                    print("Make sure your phone and computer are connected to the internet.")
                    print("If there is an alert, please dismiss it." + style.RESET)
                else:
                    sleep(1)
                    click_btn.click()  # Click the send button
                    sent = True
                    sleep(3)
                    print(style.GREEN + 'Message sent to: ' + number + style.RESET)
    except Exception as e:
        print(style.RED + f'Failed to send message to {number}: {str(e)}' + style.RESET)

# Close the browser
driver.close()
