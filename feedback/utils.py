from django.conf import settings
import requests

def verify_captcha(token):
    if not token:
        return False
    response = requests.post(
        settings.RECAPTCHA_URL,
        data={'secret': settings.RECAPTCHA_KEY,'response': token})
    data = response.json()
    return data