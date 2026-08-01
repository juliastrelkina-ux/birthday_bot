import os
import requests
import gspread

from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# Подключение Google Sheets
creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

# Открываем таблицу по ID
sheet = client.open_by_key(
    "1OQciIYGBX8Tv3W4_17Y-txMy63G8J9CIuyHtMgPkvaU"
).sheet1


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print(response.text)


def check_birthdays():

    tomorrow = (
        datetime.now() + timedelta(days=1)
    ).strftime("%d.%m")


    rows = sheet.get_all_records()

    birthdays = []

    for row in rows:

        date = str(row.get("Дата рождения", ""))

        if date[:5] == tomorrow:
            birthdays.append(
                row.get("Имя", "")
            )


    if not birthdays:
        print("Завтра именинников нет")
        return


    names = "\n".join(
        f"🎉 {name}"
        for name in birthdays
    )


    msg1 = (
        "@juliastrelkina, сегодня нужно создать группу "
        "и открыть сбор 💵\n\n"
        "Завтра день рождения у:\n"
        f"{names}"
    )


    msg2 = (
        "Коллеги, завтра день рождения у:\n\n"
        f"{names}\n\n"
        "Давайте оперативно соберем сегодня "
        "и завтра до 12:00.\n\n"
        "Переводим мне на Тинькофф банк.\n"
        "Любая сумма от 500 ₽."
    )


    send_message(msg1)
    send_message(msg2)


    print("Сообщения отправлены")


print("Бот запущен")

check_birthdays()

print("Бот завершил работу")
