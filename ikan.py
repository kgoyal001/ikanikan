import requests
import time
from colorama import Fore, Style, init
import random
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

url_shop = "https://fishapi.xboost.io/zone/order/goodslist"
url_order_status = "https://fishapi.xboost.io/zone/order/status" #{"order_no":"7222987293051585536"}
url_create_order = "https://fishapi.xboost.io/zone/order/createorder" #{"goods_id":2}
login_tokens = []
check_counter = 0
previous_results = {}

custom_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://happy-aquarium.xboost.io",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://happy-aquarium.xboost.io/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}

def get_random_color():
    colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

def login(query):
    url = "https://fishapi.xboost.io/index/tglogin"
    custom_headers["content-type"] = "application/json"
    payload = {"initData": query}
    try:
        response = requests.post(url, headers=custom_headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

def load_game_state(login_token):
    url = "https://fishapi.xboost.io/zone/user/gamestate"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    try:
        response = requests.post(url, headers=custom_headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
def delete_fish(fish_id, login_token):
    url = "https://fishapi.xboost.io/zone/user/gameactions"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"actions":[{"action":"recover","id":fish_id}]}
    try:
        response = requests.post(url, headers=custom_headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
def combine_fishes(fish_id, login_token):
    url = "https://fishapi.xboost.io/zone/user/gameactions"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"actions":[{"action":"compose","id":fish_id}]}
    try:
        response = requests.post(url, headers=custom_headers, json=payload)
        # print(response)
        if response.status_code == 200:
            # print(response.json())
            return response.json()
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
def check_free_diamond(login_token):
    url = "https://fishapi.xboost.io/zone/order/goodslist"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    try:
        response = requests.post(url, headers=custom_headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
def create_order(goods_id, login_token):
    url = "https://fishapi.xboost.io/zone/order/createorder"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"goods_id": goods_id}
    try:
        response = requests.post(url, headers=custom_headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
def check_order_status(order_no, login_token):
    url = "https://fishapi.xboost.io/zone/order/status"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"order_no": order_no}
    try:
        response = requests.post(url, headers=custom_headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
def fetch_and_print_user_data(login_token, index):
    query = login_token['query']
    token = login_token['login_token']
    color = get_random_color()

    time.sleep(random.randint(1, 5))
    while True:
        game_state = load_game_state(token)
        if game_state and game_state.get('code', None) == 200:
            fishes = game_state['data']['fishes']
            fish_limit = game_state['data']['fishLimit']
            gold = game_state['data']['gold']
            level = game_state['data']['level']
            if gold in previous_results.values():
                time.sleep(random.randint(1, 5))
                continue
            else:
                previous_results[index] = gold

            if len(fishes) > 1:
                first_fish = fishes[0]
                # if first fish is the lowest level from the list, delete it
                if first_fish == min(fishes) and check_counter == 20:
                    delete_fish(first_fish, token)

            fish_id = 0
            for fish in fishes:
                if fishes.count(fish) > 1:
                    fish_id = fish
                    break
            if fish_id != 0:
                combine_fishes(fish_id, token)

            result = (
                f"Akun {Style.BRIGHT}{color}{index + 1}{Style.RESET_ALL} | "
                f"Level: {Style.BRIGHT}{color}{level}{Style.RESET_ALL} | "
                f"Gold: {Style.BRIGHT}{color}{gold}{Style.RESET_ALL} | "
                f"Fish Limit: {Style.BRIGHT}{color}{fish_limit}{Style.RESET_ALL} | "
                f"Fishes: {Style.BRIGHT}{color}{fishes}{Style.RESET_ALL}"
            )
            return result

        elif game_state and game_state.get('code', None) == 10006:
            # getting new login token
            login_response = login(query)
            if login_response and login_response.get('code', None) == 200:
                login_tokens[index] = ({
                    "query": query,
                    "login_token": login_response['data']['login_token']
                })
                return f"{Fore.GREEN}User Login in another device! Net login token: {login_response['data']['login_token']}{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}Failed to fetch user data!{Style.RESET_ALL}"
    
def Main():
    init(autoreset=True)
    next_check_shop = datetime.now()
    global check_counter
    with open("query.txt", "r") as file:
        querys = file.read().splitlines()
    
    for query in querys:
        login_response = login(query)
        if login_response and login_response.get('code', None) == 200:
            login_tokens.append({
                "query": query,
                "login_token": login_response['data']['login_token']
            })
        else:
            print(f"{Fore.RED}Login Failed!{Style.RESET_ALL}")

    while True:
        results = []
        current_time = datetime.now()

        if current_time >= next_check_shop:
            for index, login_token in enumerate(login_tokens):
                check_list = check_free_diamond(login_token['login_token'])
                if check_list and check_list.get('code') == 200:
                    goods = check_list['data']['goods']
                    for good in goods:
                        if good['price'] == 0:
                            ordersend = create_order(good['id'], login_token['login_token'])
                            if ordersend and ordersend.get('code') == 200:
                                order_status = check_order_status(ordersend['data']['info']['order_no'], login_token['login_token'])
                                if order_status and order_status.get('code') == 200:
                                    print(f"{Fore.GREEN}Akun {index + 1} | {order_status['data']['info']['name']} | Cost {order_status['data']['info']['price']} | {order_status['data']['info']['diamond']} Diamond{Style.RESET_ALL}")
            next_check_shop = current_time + timedelta(hours=3)

        with ThreadPoolExecutor(max_workers=len(login_tokens)) as executor:
            futures = [executor.submit(fetch_and_print_user_data, login_token, index) for index, login_token in enumerate(login_tokens)]
            for future in futures:
                result = future.result()  # Wait for all threads to complete
                if result:
                    results.append(result)
        
        if results:
            # Clear the previous output
            print("\033c", end="")  # ANSI escape code to clear the screen
            # Print How many seconds until next 
            time_diff = next_check_shop - current_time
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Next Check Shop in {hours} hours {minutes} minutes {seconds} seconds")
            # Print all results at once
            print("\n".join(results), end="\r", flush=True)

        if check_counter == 20:
            check_counter = 0
        else:
            check_counter += 1


if __name__ == "__main__":
    Main()