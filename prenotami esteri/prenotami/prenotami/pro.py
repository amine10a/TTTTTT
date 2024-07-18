from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
import json
from datetime import datetime
import random
from itertools import cycle
from urllib.parse import quote,urlencode
def post_days(cookies,url_c):
    session = requests.Session()
    url_calendar = "https://prenotami.esteri.it/BookingCalendar/RetrieveCalendarAvailability"
    headers = {
        "Content-Length": "89",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Accept-Language": "en-US",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://prenotami.esteri.it",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": url_c,
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        "Connection": "keep-alive"
    }

    current_date = datetime.now()
    data_calendar = {
        "_Servizio": "2357",
        "selectedDay": current_date.strftime("%d/%m/%Y")
    }

    # Set cookies
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Make the first POST request to retrieve calendar availability
    response = session.post(url_calendar, headers=headers, data=data_calendar)
    if response.status_code == 200:
        print("Response received successfully!")
        print(response.json())
    else:
        print(f"Failed to receive response. Status code: {response.status_code}")
        print(response.text)
    return response.json()


def post_booking(cookies, url_c, data, retry_count=3):
    url = "https://prenotami.esteri.it/BookingCalendar/InsertNewBooking"
    session = requests.Session()
    headers = {
        "Content-Length": "89",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Accept-Language": "en-US",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://prenotami.esteri.it",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": url_c,
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        "Connection": "keep-alive"
    }   

    # Log data being sent
    print("Data being sent:", data)
    
    # Set cookies
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    # Encode data to ensure it's properly formatted
    encoded_data = data
    
    attempt = 0
    while attempt < retry_count:
        attempt += 1
        try:
            # Make the POST request to insert a new booking
            response = session.post(url, headers=headers, data=encoded_data)
            
            if response.status_code == 200:
                print("Booking successful!")
                print(response.text)
                return True
            else:
                print(f"Booking failed. Status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        print(f"Retrying... Attempt {attempt} of {retry_count}")
        time.sleep(2)  # Add a small delay before retrying

    return False
    


def post_time(cookies,selectday,url_c):
    session = requests.Session()
    url_calendar = "https://prenotami.esteri.it/BookingCalendar/RetrieveTimeSlots"
    headers = {
        "Content-Length": "48",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Accept-Language": "en-US",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://prenotami.esteri.it",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": url_c,
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        "Connection": "keep-alive"
    }

    
    data_calendar = {
        "selectedDay":selectday,
         "idService":"2357"
    }

    # Set cookies
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Make the first POST request to retrieve calendar availability
    response = session.post(url_calendar, headers=headers, data=data_calendar)
    if response.status_code == 200:
        print("Response received successfully!")
        print(response.json())
    else:
        print(f"Failed to receive response. Status code: {response.status_code}")
        print(response.text)
    return response.json()




def selectday(response_days):
    if isinstance(response_days, str):
        response_days = json.loads(response_days)
    
    available_days = [
        day for day in response_days 
        if isinstance(day, dict) and day.get("SlotLiberi") == 1 and day.get("SlotRimanenti") == 0
    ]
    
    if available_days:
        selected_day = random.choice(available_days)
        date_string = selected_day["DateLibere"].split(" ")[0]
        date_obj = datetime.strptime(date_string, "%d/%m/%Y")
        return date_obj.strftime("%Y-%m-%d")
    else:
        return None

def select_time(response_time):
    if isinstance(response_time, str):
        response_time = json.loads(response_time)
    
    available_times = [
        time for time in response_time 
        if time.get("SlotLiberi") == 1 and time.get("SlotRimanenti") == 0
    ]
    
    if available_times:
        selected_time = random.choice(available_times)
        start_time = selected_time["OrarioInizioFascia"]
        end_time = selected_time["OrarioFineFascia"]
        
        start_time_str = f'{start_time["Hours"]:02}:{start_time["Minutes"]:02}'
        end_time_str = f'{end_time["Hours"]:02}:{end_time["Minutes"]:02}'
        slot_count = 1  # As per the example provided in the question, assume "n" is 1
        
        selected_hour = f"{start_time_str} - {end_time_str}({slot_count})"
        return selected_hour, selected_time["IDCalendarioServizioGiornaliero"]
    else:
        return None

def generate_output(response_days, response_time):
    selected_day = selectday(response_days)
    selected_hour, id_calendario = select_time(response_time)
    
    if selected_day and selected_hour:
        output = {
            "idCalendarioGiornaliero": str(id_calendario),
            "selectedDay": selected_day,
            "selectedHour": selected_hour
        }
        return output
    else:
        return None

def save_valid(email, password, url_c):
    with open("list_valid.txt", "a") as file:
        file.write(f"{email}:{password}:{url_c}\n")
        
def automt(email, password, services_url,url_c,proxy):
    chrome_options = Options()
    #chrome_options.add_argument("--incognito")
    chrome_options.add_argument(f'--proxy-server={proxy}')
    #chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    driver = webdriver.Chrome(options=chrome_options)
    

    try:
        # Open the login page
        driver.get("https://prenotami.esteri.it/")

        # Locate the email field and input the email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-email"))
        )
        email_field.send_keys(email)

        # Locate the password field and input the password
        password_field = driver.find_element(By.ID, "login-password")
        password_field.send_keys(password)

        # Locate the login button and click it
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        # Wait for the login to process (adjust time as needed)
        WebDriverWait(driver, 10).until(
            EC.url_changes("https://prenotami.esteri.it/Home/Login")
        )

        # Check for login success
        if "Home/Login" in driver.current_url:
            print("Login failed. Check your credentials or handle CAPTCHA.")
        else:
            print("Login successful!")

            # Navigate to the "Services" page
            driver.get(services_url)

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "PrivacyCheck"))
            )

            # Click the checkbox
            checkbox = driver.find_element(By.ID, "PrivacyCheck")
            checkbox.click()

            # Click the forward button
            forward_button = driver.find_element(By.ID, "btnAvanti")
            forward_button.click()

            # Function to handle JS alerts
            def handle_alert():
                try:
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    print(f"Alert text: {alert_text}")
                    alert.accept()
                    print("Alert accepted.")
                    # Optionally, you can get the URL after accepting the alert
                    print(f"Redirected URL: {driver.current_url}")
                    
                    time.sleep(20)
                except:
                    print("No alert to accept.")

            # Call the function to handle any alert
            handle_alert()
            
            
            # Get cookies from the browser session
            cookies = driver.get_cookies()

            response_days = post_days(cookies,url_c)
            print(response_days)
            slected_day = selectday(response_days)
            print(slected_day)
            
            response_time = post_time(cookies,slected_day.replace(" ", ""),url_c)
            print(response_time)   
            data = generate_output(response_days,response_time)
            print(data)
            if post_booking(cookies,url_c,data) :
                save_valid(email,password,url_c)
            

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")
def read_accounts(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        accounts = [line.strip().split(':') for line in lines]
    return accounts

def read_proxy(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies
          
if __name__ == "__main__":

    url_c = "https://prenotami.esteri.it/BookingCalendar?selectedService=Ufficio%20AIRE.%20Consulta%20la%20pagina%20%22AIRE%20-%20Anagrafe%20degli%20Italiani%20Residenti%20all%27Estero%22%20sul%20sito%20dell%27Ambasciata%20prima%20di%20prenotare%20l%27appuntamento%20per%20tutte%20le%20informazioni%20necessarie."
    services_url = "https://prenotami.esteri.it/Services/Booking/2357"

    accounts = read_accounts('accounts.txt')
    proxies = read_proxy('proxy.txt')
    
    account_cycle = cycle(accounts)  # Create an infinite cycle of accounts
    proxy_cycle = cycle(proxies)  # Create an infinite cycle of proxies
    
    while True:
        email, password = next(account_cycle)  # Get the next account in the cycle
        proxy = "" #next(proxy_cycle)  # Get the next proxy in the cycle
        
        try:
            automt(email, password, services_url, url_c, proxy)
        except Exception as e:
            print(f"An error occurred: {str(e)}")