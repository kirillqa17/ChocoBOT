import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor

COOKIES_FOLDER = "./cookies"
PAYLOAD_FOLDER = "./payload"  # Папка, где хранятся файлы payload
ADD_TO_CART_URL = "https://api.ae.deliveroo.com/consumer/basket/graphql"
CHECKOUT_URL = "https://api.ae.deliveroo.com/consumer/checkout"


def load_cookies(account_id):
    """
    Загружает cookies из файла для заданного аккаунта и возвращает их в формате словаря.
    """
    cookies_path = os.path.join(COOKIES_FOLDER, f"cookies_{account_id}.json")
    with open(cookies_path, "r") as file:
        cookies = json.load(file)
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    return cookies_dict


def load_payload(filename):
    """
    Загружает данные payload из указанного файла в папке payload.
    """
    payload_path = os.path.join(PAYLOAD_FOLDER, filename)
    if not os.path.exists(payload_path):
        raise FileNotFoundError(f"Файл payload {filename} не найден в папке {PAYLOAD_FOLDER}")
    with open(payload_path, "r") as file:
        payload = json.load(file)
    return payload


def make_request(account_id):
    """
    Отправляет запрос на добавление товара в корзину от имени аккаунта с использованием cookies и Bearer токена.
    """
    cookies = load_cookies(account_id)
    bearer_token = cookies.get("consumer_auth_token")
    roo_sticky_guid = cookies.get("roo_sticky_guid")
    roo_guid = cookies.get("roo_guid")
    roo_session_guid = cookies.get("roo_session_guid")

    if not bearer_token:
        print(f"Bearer токен не найден для аккаунта {account_id}")
        return None
    if not roo_sticky_guid or not roo_guid or not roo_session_guid:
        print(f"Один из необходимых GUID не найден для аккаунта {account_id}")
        return None

    session = requests.Session()
    session.cookies.update(cookies)

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "sec-ch-ua-platform": "Windows",
        "x-roo-country": "ae",
        "accept-language": "en",
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'accept': 'application/json, application/vnd.api+json',
        'content-type': 'application/json',
        'origin': 'https://deliveroo.ae',
        'x-roo-client-referer': 'https://deliveroo.ae/restaurants/dubai/district-one?fulfillment_method=DELIVERY&geohash=thrr4w7tmxgh',
        'x-roo-external-device-id': '5e0e7b85-e3ba-4d9c-ba8a-4906aba779d2',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://deliveroo.ae/',
        "x-roo-client": "consumer-web-app",
        'content-length': '20330',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'priority': 'u=1, i',
        'host': 'api.ae.deliveroo.com',
        "x-roo-sticky-guid": roo_sticky_guid,
        "x-roo-guid": roo_guid,
        "x-roo-session-guid": roo_session_guid
    }

    payload = load_payload("addToCart.json")  # Загружаем payload для добавления товара в корзину

    try:
        response = session.post(ADD_TO_CART_URL, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"Товар успешно добавлен в корзину для аккаунта {account_id}")
            return session  # Возвращаем сессию, если запрос был успешным
        else:
            print(
                f"Ошибка {response.status_code} при добавлении товара в корзину для аккаунта {account_id}: {response.text}")
            return None
    except requests.RequestException as exception:
        print(f"Ошибка при выполнении запроса для аккаунта {account_id}: {exception}")
        return None


def checkout_request(session, account_id):
    """
    Отправляет запрос для оплаты корзины, используя ту же сессию и заголовки.
    """
    headers = session.headers.copy()
    headers.update({
        "content-type": "application/json",
        "Authorization": session.headers["Authorization"]
    })

    payload = load_payload("checkout.json")  # Загружаем payload для оплаты корзины

    try:
        response = session.post(CHECKOUT_URL, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"Оплата успешно выполнена для аккаунта {account_id}")
        else:
            print(f"Ошибка {response.status_code} при оплате корзины для аккаунта {account_id}: {response.text}")
    except requests.RequestException as exception:
        print(f"Ошибка при оплате корзины для аккаунта {account_id}: {exception}")


def process_account(account_id):
    """
    Основная функция для обработки запросов: добавляет товар в корзину и выполняет оплату.
    """
    session = make_request(account_id)

    if session:
        checkout_request(session, account_id)


def main():
    cookie_files = [file for file in os.listdir(COOKIES_FOLDER) if
                    file.startswith("cookies_") and file.endswith(".json")]
    num_accounts = len(cookie_files)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_account, account_id) for account_id in range(1, num_accounts + 1)]

        for future in futures:
            future.result()

    print("Все запросы выполнены.")


if __name__ == "__main__":
    main()
