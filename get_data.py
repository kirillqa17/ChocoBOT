import random

def get_random_user_agent():
    with open('userAgents.txt', 'r') as file:
        user_agents = file.readlines()
    return random.choice(user_agents).strip()


import requests

headers = {
    'accept': 'application/json, application/vnd.api+json',
    'accept-language': 'en',
    'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsImprdSI6Imh0dHBzOi8vZGVsaXZlcm9vLmNvLnVrL2lkZW50aXR5LWtleXMvMS5qd2sifQ.eyJleHAiOjE3MzA0NjQ4OTgsImN1c3QiOjgzOTE1ODI4LCJkcm5faWQiOiI1ZDNjMDk1Yi03MDEzLTQzMGMtYmRjNi0wNWQ4MWNlYmU4ZGYiLCJzZXNzIjoid2ViLDM4ZDA0YWEwNWY3YjRiZjZiMGMzY2NmN2FkY2Y5YzBjIn0.yTjxu1hMNKaU3r3tcvydL8MUDIhg0_eXQxPq1X6fPXZpGbxkjz_sNE6PLvR-Hf3eZOLViebJUms_Luxz54Zjgg',
    'content-type': 'application/json',
    'origin': 'https://deliveroo.ae',
    'priority': 'u=1, i',
    'referer': 'https://deliveroo.ae/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-roo-client': 'consumer-web-app',
    'x-roo-client-referer': 'https://deliveroo.ae/account/vouchers',
    'x-roo-country': 'ae',
    'x-roo-external-device-id': '7e96da96-d808-44b5-a0e4-814ff2928d1d',
    'x-roo-guid': '25f7683d-610e-4f01-9179-cff8f3d9f7b8',
    'x-roo-platform': 'web',
    'x-roo-session-guid': 'b62b7e83-b190-437a-a521-4cd6f5138ab3',
    'x-roo-sticky-guid': '2D48F3FB-0F80-4C2C-AA22-6C92F3579104',
}

json_data = {
    'redemption_code': 'K8PW4DD4Q8GY',
    'page': 'account',
}

response = requests.post('https://api.ae.deliveroo.com/orderapp/v1/users/83915828/vouchers', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"redemption_code":"K8PW4DD4Q8GY","page":"account"}'
#response = requests.post('https://api.ae.deliveroo.com/orderapp/v1/users/83915828/vouchers', headers=headers, data=data)
