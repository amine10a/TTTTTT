import requests
import json
import random
from datetime import datetime
from itertools import cycle
import time


def post_days(cookies, url_c):
    session = requests.Session()
    url_calendar = "https://prenotami.esteri.it/BookingCalendar/RetrieveCalendarAvailability"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": url_c,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    }

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
        return response.json()
    else:
        print(f"Failed to receive response. Status code: {response.status_code}")
        print(response.text)
        return None


def post_booking(cookies, url_c, data):
    url = "https://prenotami.esteri.it/BookingCalendar/InsertNewBooking"
    session = requests.Session()
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": url_c,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    }

    # Log data being sent
    print("Data being sent:", data)
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Make the POST request to insert a new booking
    response = session.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Booking successful!")
        return True
    else:
        print(f"Booking failed. Status code: {response.status_code}")
        print(response.text)
        return False


def post_time(cookies, selectday, url_c):
    session = requests.Session()
    url_calendar = "https://prenotami.esteri.it/BookingCalendar/RetrieveTimeSlots"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": url_c,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    }

    data_calendar = {
        "selectedDay": selectday,
        "idService": "2358"
    }

    # Set cookies
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Make the first POST request to retrieve calendar availability
    response = session.post(url_calendar, headers=headers, data=data_calendar)
    if response.status_code == 200:
        print("Response received successfully!")
        return response.json()
    else:
        print(f"Failed to receive response. Status code: {response.status_code}")
        print(response.text)
        return None


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
        slot_count = 1  # Assume "n" is 1

        selected_hour = f"{start_time_str} - {end_time_str}({slot_count})"
        return selected_hour, selected_time["IDCalendarioServizioGiornaliero"]
    else:
        return None, None


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


def login_and_get_cookies(email, password):
    session = requests.Session()
    login_url = "https://prenotami.esteri.it/Home/Login"
    
    # Get the login page to set initial cookies
    session.get(login_url)

    # Payload for login
    login_data = {
        "login-email": email,
        "login-password": password,
        # Add other necessary fields here if needed
    }
    
    # Perform login
    response = session.post(login_url, data=login_data)

    if "Home/Login" in response.url:
        print("Login failed. Check your credentials or handle CAPTCHA.")
        return None
    else:
        print("Login successful!")
        return session.cookies


def automt(email, password, services_url, url_c):
    cookies = login_and_get_cookies(email, password)
    if not cookies:
        return

    response_days = post_days(cookies, url_c)
    if not response_days:
        print("Failed to retrieve days")
        return

    print(response_days)
    selected_day = selectday(response_days)
    if not selected_day:
        print("No available days found")
        return

    print(selected_day)
    response_time = post_time(cookies, selected_day, url_c)
    if not response_time:
        print("Failed to retrieve times")
        return

    print(response_time)
    data = generate_output(response_days, response_time)
    if not data:
        print("Failed to generate booking data")
        return

    print(data)
    if post_booking(cookies, url_c, data):
        save_valid(email, password, url_c)


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
    url_c = "https://prenotami.esteri.it/BookingCalendar?selectedService=Ufficio%20Cittadinanza%20e%20Notarile.%20Consulta%20la%20pagina%20%22Cittadinanza%22%20e%20%22Servizio%20Notarile%22%20sul%20sito%20dell%27Ambasciata%20prima%20di%20prenotare%20l%27appuntamento%20per%20tutte%20le%20informazioni%20necessarie."
    services_url = "https://prenotami.esteri.it/Services/Booking/2358"
    accounts = read_accounts('accounts.txt')
    proxies = read_proxy('proxy.txt')

    account_cycle = cycle(accounts)  # Create an infinite cycle of accounts
    proxy_cycle = cycle(proxies)  # Create an infinite cycle of proxies

    while True:
        email, password = next(account_cycle)  # Get the next account in
       # proxy = next(proxy_cycle)  # Get the next proxy in the cycle

        try:
            automt(email, password, services_url, url_c)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        time.sleep(10)  # Wait time before the next account tries to book