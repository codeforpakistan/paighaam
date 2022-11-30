import os
from requests import post


class SMS:
    def send(self, destination, message):
        try:
            r = post(
                url=os.getenv("MONTY_BASEURL") + "/smppServers/sms",
                headers={"Authorization": os.getenv("MONTY_AUTH_HEADER")},
                json={
                    "from": "Digi Alert",
                    "to": destination,
                    "message": "KP Super App " + message,
                },
            )
            return r.json()
        except:
            return "error"


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
