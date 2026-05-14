import requests

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
ADMIN_PHONE = "91XXXXXXXXXX"

def send_whatsapp(message):

    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN":
        print("Configure WhatsApp API")
        return

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": ADMIN_PHONE,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.json())
