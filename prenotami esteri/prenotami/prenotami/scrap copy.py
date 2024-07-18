from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests

# Setup Chrome options to specify the binary location
chrome_options = Options()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Setup WebDriver with the specified Chrome executable
driver = webdriver.Chrome(options=chrome_options)

def post_booking(cookies):
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
        "Referer": "https://prenotami.esteri.it/BookingCalendar?selectedService=Ufficio%20Legalizzazioni.%20Consulta%20la%20pagina%20%22Dichiarazioni%20di%20Valore%22%20sul%20sito%20dell%27Ambasciata%20prima%20di%20prenotare%20l%27appuntamento%20per%20tutte%20le%20informazioni%20necessarie.",
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
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    response = session.post(url, headers=headers, data=data)
    return response.json()

try:
    # Open the login page
    driver.get("https://prenotami.esteri.it/")

    # Locate the email field and input the email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-email"))
    )
    email_field.send_keys("d5e026bfdc@emailcbox.pro")

    # Locate the password field and input the password
    password_field = driver.find_element(By.ID, "login-password")
    password_field.send_keys("Xzab@am12")

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
        services_url = "https://prenotami.esteri.it/Services/Booking/2357"
        driver.get(services_url)

        
        
        # Get cookies from the browser session
        cookies = driver.get_cookies()

        # Call the post_booking function
        response_data = post_booking(cookies)
        print(response_data)
        driver.get(services_url)

finally:
    # Close the browser
    driver.quit()
    print("Browser closed.")
