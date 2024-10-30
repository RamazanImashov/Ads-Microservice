import random
import string

import requests
from decouple import config

login = config('SMS_LOGIN')
password = config('SMS_PASSWORD')
sender = config('SMS_SENDER')


def generate_transaction_id(length=12):
    chars = string.ascii_letters + string.digits
    transactionId = ''.join(random.choice(chars) for _ in range(length))
    return transactionId


def send_sms(username, phone_number, verify_code):

    transactionId = generate_transaction_id()
    username = username
    text = verify_code
    phone = phone_number

    xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <message>
        <login>{login}</login>
        <pwd>{password}</pwd>
        <id>{transactionId}</id>
        <sender>{sender}</sender>
        <text>{text}</text>
        <usernames>
            <username>{username}</username>
        </usernames>
        <phones>
            <phone>{phone}</phone>
        </phones>
    </message>"""

    url = 'https://smspro.nikita.kg/api/message'
    headers = {'Content-Type': 'application/xml'}

    response = requests.post(url, data=xml_data, headers=headers)
    if response.status_code == 200:
        print('Ответ сервера:', response.text)
