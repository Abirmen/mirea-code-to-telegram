import requests, imaplib, re, time
from config import BOT_TOKEN, CHAT_ID, MAIL_LOGIN, MAIL_PASSWORD
from email import message_from_bytes


url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

last_id = None

while True:

    mail = imaplib.IMAP4_SSL("imap.mail.ru", 993)
    mail.login(MAIL_LOGIN, MAIL_PASSWORD)

    mail.select("INBOX")

    status, messages = mail.search(None, "ALL")

    mail_ids = messages[0].split()
    current_id = mail_ids[-1]

    if current_id != last_id:

        status, data = mail.fetch(current_id, "(RFC822)")

        r_email = data[0][1]

        email = message_from_bytes(r_email)

        text = email.get_payload(decode=True).decode("utf-8")

        match = re.search(r"\b\d{6}\b", text)

        sender = email["From"]

        if "sso@mirea.ru" in sender and match:
            code = match.group()

            data = {
                "chat_id": CHAT_ID,
                "text": f"Ваш код: {code}"
            }

            requests.post(url, data=data)

        last_id = current_id

    mail.logout()

    time.sleep(4)