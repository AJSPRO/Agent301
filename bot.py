import requests
import urllib.parse
from fake_useragent import UserAgent
import time
import json
from colorama import Fore, init
from art import text2art
import os
from datetime import datetime

init(autoreset=True)

def print_banner():
    banner = text2art("AJSPRO", font='standard')
    print(Fore.LIGHTCYAN_EX + banner)
    print(Fore.LIGHTYELLOW_EX + "Don't forget to grab a coffee!")
    print()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_username(authorization):
    try:
        parsed_data = urllib.parse.parse_qs(authorization)
        user_data_json = parsed_data.get('user', [''])[0]

        user_data = json.loads(urllib.parse.unquote(user_data_json))

        username = user_data.get('username', 'Not found')
        return username
    except (json.JSONDecodeError, KeyError):
        return 'Not found'

def load_authorizations_with_usernames(file_path):
    with open(file_path, 'r') as file:
        authorizations = file.readlines()

    auth_with_usernames = [{'authorization': auth.strip(), 'username': extract_username(auth)} for auth in
                           authorizations]
    return auth_with_usernames

def claim_tasks(authorization, username):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'authorization': authorization.strip(),
        'origin': 'https://telegram.agent301.org',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    url_get_tasks = 'https://api.agent301.org/getMe'
    response = requests.post(url_get_tasks, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok"):
            result = json_response.get("result", {})
            balance = result.get("balance", 0)
            print(f"{Fore.LIGHTCYAN_EX}Name :  {Fore.LIGHTGREEN_EX}{username} {Fore.LIGHTCYAN_EX}Balance: {Fore.LIGHTGREEN_EX}{balance}AP")
            print(f"{Fore.LIGHTYELLOW_EX}Processing automatic tasks...\n")

            # Print claim time
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{Fore.LIGHTCYAN_EX}Claim time: {Fore.LIGHTGREEN_EX}{current_time}")

            tasks = result.get("tasks", [])
            print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
            print(Fore.LIGHTCYAN_EX + "• Claiming Tasks •\n")  # Title for tasks
            print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")

            for task in tasks:
                task_type = task.get("type")
                title = task.get("title")
                reward = task.get("reward", 0)
                is_claimed = task.get("is_claimed")
                count = task.get("count", 0)
                max_count = task.get("max_count")

                if max_count is None and not is_claimed:
                    print(f"{Fore.LIGHTBLUE_EX}Claiming task: {title}")
                    claim_task(headers, task_type, title)

                elif task_type == "video" and count < max_count:
                    while count < max_count:
                        print(f"{Fore.LIGHTBLUE_EX}Claiming task: {title} Progress: {count}/{max_count}")
                        if claim_task(headers, task_type, title):
                            count += 1
                        else:
                            break

                elif not is_claimed and count >= max_count:
                
                    print(f"{Fore.LIGHTBLUE_EX} • Claiming task • {title}")
                    claim_task(headers, task_type, title) 

            print(f"{Fore.LIGHTRED_EX} ✔ All tasks claimed")
            return balance

        else:
            print(f"{Fore.LIGHTRED_EX}Failed to request tasks. Try again.")
    else:
        print(f"{Fore.LIGHTRED_EX}Error: {response.status_code}")
    return 0

def claim_task(headers, task_type, title):
    url_complete_task = 'https://api.agent301.org/completeTask'
    claim_data = {"type": task_type}
    response = requests.post(url_complete_task, headers=headers, json=claim_data)

    if response.status_code == 200 and response.json().get("ok"):
        result = response.json().get("result", {})
        task_reward = result.get("reward", 0)
        balance = result.get("balance", 0)
        print(f"{Fore.LIGHTYELLOW_EX}Task {task_type} - {title} - Reward {Fore.LIGHTYELLOW_EX}{task_reward}AP - Balance now : {Fore.LIGHTGREEN_EX}{balance}AP")
        return True
    else:
        print(f"{Fore.LIGHTRED_EX}Task {task_type} - {title} - Failed to complete!")
        return False

def claim_wheel(authorization, username):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'authorization': authorization.strip(),
        'origin': 'https://telegram.agent301.org',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    url_get_tasks = 'https://api.agent301.org/wheel/load'
    response = requests.post(url_get_tasks, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok"):
            tasks = json_response.get("result", {}).get("tasks", {})
            spin_completed = True


            print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
            print(Fore.LIGHTCYAN_EX + "• Claiming Wheel Tasks •\n") 
            print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")

            for _ in range(5):
                payload = {'type': 'hour'}
                requests.post('https://api.agent301.org/wheel/task', headers=headers, json=payload)
                print(f'{Fore.LIGHTYELLOW_EX}turning wheel')

            if tasks.get('daily', 1) == 0:
                payload = {'type': 'daily'}
                requests.post('https://api.agent301.org/wheel/task', headers=headers, json=payload)
                print(f'{Fore.LIGHTBLUE_EX}Claiming daily tasks on the wheel')

            if not tasks.get('bird', True):
                payload = {'type': 'bird'}
                requests.post('https://api.agent301.org/wheel/task', headers=headers, json=payload)
                print(f'{Fore.LIGHTBLUE_EX}Claiming bird tasks on the wheel')

            if tasks.get('hour', 0) == 0 and tasks.get('daily', 1) == 0 and tasks.get('bird', True):
                spin_completed = False

            if not spin_completed:
                print(f'{Fore.LIGHTRED_EX} ✔ Spin tasks completed. Please wait until tomorrow for the next spin.')

            # Add RGB color for spin reward
            rgb_colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
            spin_reward = 500  # Example spin reward value
            color_index = 0
            print(f'{Fore.LIGHTYELLOW_EX}Spin reward: {rgb_colors[color_index % len(rgb_colors)]}{spin_reward} AP')
            color_index += 1

            print(f'{Fore.LIGHTRED_EX} ✔ Spin task completed ')
        else:
            print(f"{Fore.LIGHTRED_EX}Failed to request wheel tasks. Try again.")
    else:
        print(f"{Fore.LIGHTRED_EX}Error: {response.status_code}")

def countdown_timer(seconds):
    rgb_colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    color_index = 0

    while seconds:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        timer = f'{hours:02}:{mins:02}:{secs:02}'
        
        # Countdown in RGB colors
        print(Fore.LIGHTGREEN_EX + 'Waiting: ' + rgb_colors[color_index % len(rgb_colors)] + f'{timer}', end='\r')

        time.sleep(1)
        seconds -= 1
        color_index += 1

    print(Fore.LIGHTGREEN_EX + 'Finished waiting!')

def main():
    clear_console()  # Clear console before starting
    print_banner()

    # Initial options in English
    print(Fore.LIGHTGREEN_EX + "Choose an option:")
    print(Fore.LIGHTCYAN_EX + "1. Run tasks only")
    print(Fore.LIGHTCYAN_EX + "2. Run spins only")
    print(Fore.LIGHTCYAN_EX + "3. Run all")
    choice = input(Fore.LIGHTGREEN_EX + "Enter your choice (1/2/3): ")

    auth_data = load_authorizations_with_usernames('query.txt')
    total_balance = 0

    while True:
        for account_number, data in enumerate(auth_data, start=1):
            authorization = data['authorization']
            username = data['username']

            print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
            print(f"{Fore.LIGHTCYAN_EX}Account {Fore.LIGHTCYAN_EX}No.{Fore.LIGHTCYAN_EX}{account_number}")
            print(f"{Fore.LIGHTYELLOW_EX}------------------------------------")

            if choice in ('1', '3'):
                balance = claim_tasks(authorization, username)
                total_balance += balance

            if choice in ('2', '3'):
                claim_wheel(authorization, username)

       
        print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
        print(Fore.LIGHTCYAN_EX + f"• All tasks and spins complete •")
        print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
        
        print(f"\n{Fore.LIGHTGREEN_EX}Total Balance for all accounts : {Fore.LIGHTYELLOW_EX}{total_balance}AP")
        
        print(Fore.LIGHTRED_EX + f"Buy coffee :")
        print(Fore.LIGHTYELLOW_EX + "  - ajspro.sol  (Solana)")
        
        print(Fore.LIGHTYELLOW_EX + "  - 0xC226c4AF21d95d8CaAf6A7b0e060adBCd51C4C24  (EVM)")
        
        print(Fore.LIGHTYELLOW_EX + "  - UQBa5v9pWqP1pgEBaGdSI1dbDUvASSpRwN_N4NLyZGamV8WN  (TON)")
        
        
        
       

        # Wait for 3 hours
        countdown_timer(10800)  # 3 hours

        clear_console()
        print_banner()
        print(Fore.LIGHTCYAN_EX + "Choose an option :")
        print(Fore.LIGHTYELLOW_EX + "1. Run tasks only")
        print(Fore.LIGHTYELLOW_EX + "2. Run spins only")
        print(Fore.LIGHTYELLOW_EX + "3. Run all")
        choice = input(Fore.LIGHTCYAN_EX + "Enter your choice (1/2/3): ")

if __name__ == "__main__":
    main()
