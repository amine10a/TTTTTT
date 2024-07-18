from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
import json
from datetime import datetime
from urllib.parse import urlencode

# Setup Chrome options to specify the binary location




def post_booking(cookies,url_c,data):
    url = "https://prenotami.esteri.it/BookingCalendar/InsertNewBooking"
    
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

    data = {
        "idCalendarioGiornaliero": "33128473",
        "selectedDay": "2024-07-24",
        "selectedHour": "10:01 - 10:30(1)"
    }
    
    # Convert Selenium cookies to requests cookies

def get_data(cookies, headers):
    session = requests.Session()
    url_calendar = "https://prenotami.esteri.it/BookingCalendar/RetrieveCalendarAvailability"
    current_date = datetime.now()
    data_calendar = {
        "_Servizio": "2358",
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

    rep_calendar = response.json()

    def get_nearest_available_date(data):
        for entry in data:
            if entry["SlotLiberi"] == 1 and entry["SlotRimanenti"] == 0:
                return entry["DateLibere"]
        return None

    selected_day = get_nearest_available_date(rep_calendar)
    print(selected_day)
    if not selected_day:
        return {"error": "No available dates found"}
    #complete
    url_time_slots = "https://prenotami.esteri.it/BookingCalendar/RetrieveTimeSlots"
    data_time_slots = {
        "selectedDay": selected_day,
        "idService": "2358"
    }

    # Make the second POST request to retrieve time slots
    response = session.post(url_time_slots, headers=headers, data=data_time_slots)
    if response.status_code == 200:
        print("Response received successfully!")
        print(response.json())
    else:
        print(f"Failed to receive response. Status code: {response.status_code}")
        print(response.text)



    rep_time_slots = response.json()
    def get_nearest_available_time_slot(data):
        for entry in data:
            if entry["SlotLiberi"] == 1 and entry["SlotRimanenti"] == 0:
                start_time = entry["OrarioInizioFascia"]
                end_time = entry["OrarioFineFascia"]
                start_time_str = f'{start_time["Hours"]:02}:{start_time["Minutes"]:02}'
                end_time_str = f'{end_time["Hours"]:02}:{end_time["Minutes"]:02}'
                return f'{start_time_str} - {end_time_str}({entry["SlotLiberi"]})'
        return None

    selected_hour = get_nearest_available_time_slot(rep_time_slots)
    print(selected_hour)
    if not selected_hour:
        return {"error": "No available time slots found"}

    return {
        "idCalendarioGiornaliero": "33128473",
        "selectedDay": selected_day,
        "selectedHour": selected_hour
    }


def automt(email, password, services_url,url_c):
    chrome_options = Options()
    chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    # Setup WebDriver with the specified Chrome executable
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
            driver.get(driver.current_url)
            
            # Get cookies from the browser session
            cookies = driver.get_cookies()
            # Call the post_booking function
            data = {
                "idCalendarioGiornaliero": "33128473",
                "selectedDay": "2024-07-24",
                "selectedHour": "10:01 - 10:30(1)"
                }       
            response_data = post_booking(cookies,url_c,data)
            print(response_data)

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":

    url_c = "https://prenotami.esteri.it/BookingCalendar?selectedService=Ufficio%20Cittadinanza%20e%20Notarile.%20Consulta%20la%20pagina%20%22Cittadinanza%22%20e%20%22Servizio%20Notarile%22%20sul%20sito%20dell%27Ambasciata%20prima%20di%20prenotare%20l%27appuntamento%20per%20tutte%20le%20informazioni%20necessarie."
    email = "d5e026bfdc@emailcbox.pro"
    password ="Xzab@am12"
    services_url = "https://prenotami.esteri.it/Services/Booking/2358"


    automt(email,password,services_url,url_c)