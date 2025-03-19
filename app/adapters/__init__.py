import os
from requests import post


class SMS:
    def send(self, destination, message):
        try:
            r = post(
                url=f"{os.getenv('MONTY_BASEURL')}/API/SendBulkSMS",
                headers={
                    "Authorization": f"Basic {os.getenv('AUTH_HEADER')}",
                    "X-Access-Token": os.getenv('AUTH_TOKEN'),
                    "Content-Type": "application/json"
                },
                json={
                    "source": "SMS-ALERT.",
                    "destination": [destination],
                    "text": message,
                    "campaignname": "Paigham"
                },
            )
            return r.json()
        except Exception as e:
            return {"error": str(e)}


class Email:
    def send(self, recipients, subject, message):
        try:
            r = post(
                url=os.getenv("MONTY_BASEURL") + "/email",
                headers={"Authorization": os.getenv("MONTY_AUTH_HEADER")},
                json={"To": recipients, "Subject": subject, "Body": message},
            )
            return r.json()
        except:
            return "error"
