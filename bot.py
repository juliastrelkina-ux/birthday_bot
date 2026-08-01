import time
import os
import requests
import gspread

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES,
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1


def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


import os
import requests
import gspread
from datetime import datetime, timedelta

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES,
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1


def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


def check_birthdays():

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m")

    rows = sheet.get_all_records()

    found = False

    for row in rows:

        birthday = str(row["Дата рождения"])[:5]

        if birthday == tomorrow:

            found = True

            name = row["Имя"]

            msg1 = (
                "@juliastrelkina, сегодня нужно создать группу, всех собрать и открыть сбор 💵\n\n"
                f"Завтра день рождения у:\n{name}"
            )

            msg2 = (
                f"Коллеги, завтра день рождения у {name} 🎉\n\n"
                "Давайте оперативно соберем сегодня и завтра до 12:00.\n\n"
                "Перевод можно сделать мне на Тинькофф.\n"
                "Любая сумма от 500 ₽."
            )

            send(msg1)
            send(msg2)

    if not found:
        print("Завтра именинников нет.")


last_date = None
print ("Бот работает...")

while True:

    now = datetime.now()

    # Каждый день в 15:00
    if (
        now.hour == 15
        and now.minute == 0
        and last_date != now.date()
    ):

        check_birthdays()
        last_date = now.date()

    time.sleep(30)
