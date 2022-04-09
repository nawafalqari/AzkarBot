from requests import get

api_url = 'https://azkar-api.nawafhq.repl.co/'
api_url_with_json = 'https://azkar-api.nawafhq.repl.co/zekr?json=true'

def zekr() -> dict:
    return get(api_url_with_json).json()