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
        'accept-language': 'en-US,en;q=0.9'
    }

    url_get_tasks = 'https://api.agent301.org/getMe'
    try:
        response = requests.post(url_get_tasks, headers=headers)
        response.raise_for_status()
        json_response = response.json()

        if json_response.get("ok"):
            result = json_response.get("result", {})
            balance = result.get("balance", 0)
            print(f"{Fore.LIGHTCYAN_EX}Name: {Fore.LIGHTGREEN_EX}{username} {Fore.LIGHTCYAN_EX}Balance: {Fore.LIGHTGREEN_EX}{balance} AP")
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
    except requests.RequestException as e:
        print(f"{Fore.LIGHTRED_EX}Request failed: {e}")
    return 0

def claim_task(headers, task_type, title):
    url_complete_task = 'https://api.agent301.org/completeTask'
    claim_data = {"type": task_type}
    try:
        response = requests.post(url_complete_task, headers=headers, json=claim_data)
        response.raise_for_status()
        if response.json().get("ok"):
            result = response.json().get("result", {})
            task_reward = result.get("reward", 0)
            balance = result.get("balance", 0)
            print(f"{Fore.LIGHTYELLOW_EX}Task {task_type} - {title} - Reward {Fore.LIGHTGREEN_EX}{task_reward} AP - Balance now: {Fore.LIGHTGREEN_EX}{balance} AP")
            return True
        else:
            print(f"{Fore.LIGHTRED_EX}Task {task_type} - {title} - Failed to complete!")
            return False
    except requests.RequestException as e:
        print(f"{Fore.LIGHTRED_EX}Request failed: {e}")
        return False

def claim_wheel(authorization, username):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'authorization': authorization.strip(),
        'origin': 'https://telegram.agent301.org',
        'accept-language': 'en-US,en;q=0.9'
    }

    url_get_tasks = 'https://api.agent301.org/getMe'
    try:
        response = requests.post(url_get_tasks, headers=headers)
        response.raise_for_status()
        json_response = response.json()

        reward_mapping = {
            'tc4': '4 TON',
            'c1000': '1,000 AP',
            't1': '1 ticket',
            'nt1': '1 NOT',
            'nt5': '5 NOT',
            't3': '3 tickets',
            'tc1': '0.01 TON',
            'c10000': '10,000 AP'
        }

        if json_response.get("ok"):
            result = json_response.get("result", {})
            tickets = result.get("tickets", 0)
            print(f"{Fore.LIGHTCYAN_EX}Account {Fore.LIGHTGREEN_EX}{username} {Fore.LIGHTCYAN_EX}Ticket Balance: {Fore.LIGHTGREEN_EX}{tickets}")

            if tickets > 0:
                print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
                print(Fore.LIGHTCYAN_EX + "• Spinning the Wheel •\n")  # Title for spinning wheel
                print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
            else:
                print(f"{Fore.LIGHTRED_EX}No tickets\n")
                return

            while tickets > 0:
                responsew = requests.post('https://api.agent301.org/wheel/spin', headers=headers)
                if responsew.status_code == 200:
                    try:
                        json_responsew = responsew.json()
                        resultw = json_responsew.get("result", {})
                        reward_code = resultw.get("reward", '')
                        reward = reward_mapping.get(reward_code, reward_code)
                        print(f'{Fore.LIGHTYELLOW_EX}Won: {Fore.LIGHTGREEN_EX}{reward}')
                    except json.JSONDecodeError:
                        print(f"{Fore.LIGHTRED_EX}Error: Server response is not valid JSON.")
                        print(f"{Fore.LIGHTRED_EX}Server response: {responsew.text}")
                        break
                else:
                    print(f"{Fore.LIGHTRED_EX}Error spinning the wheel: {responsew.status_code}")
                    print(f"{Fore.LIGHTRED_EX}Server response: {responsew.text}")
                    break

                response = requests.post(url_get_tasks, headers=headers)
                if response.status_code == 200:
                    json_response = response.json()
                    if json_response.get("ok"):
                        result = json_response.get("result", {})
                        tickets = result.get("tickets", 0)
                    else:
                        print(f"{Fore.LIGHTRED_EX}Failed to get updated ticket count. Please try again.")
                        break
                else:
                    print(f"{Fore.LIGHTRED_EX}Error getting updated ticket count: {response.status_code}")
                    break

            print(f"{Fore.LIGHTRED_EX} ✔ Spin finished!")  # Added message
        else:
            print(f"{Fore.LIGHTRED_EX}Failed to get tasks. Please try again.")
    except requests.RequestException as e:
        print(f"{Fore.LIGHTRED_EX}Request failed: {e}")

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

    print(Fore.LIGHTGREEN_EX + 'Waiting: 00:00:00')

def main():
    print_banner()
    print(Fore.LIGHTCYAN_EX + "Choose an option:")
    print(Fore.LIGHTGREEN_EX + "1. Claim Tasks")
    print(Fore.LIGHTGREEN_EX + "2. Spin Wheel")
    print(Fore.LIGHTGREEN_EX + "3. Claim All")
    choice = input(Fore.LIGHTMAGENTA_EX + "Enter your choice: ")

    auth_data = load_authorizations_with_usernames('query.txt')
    total_balance = 0

    while True:
        for account_number, data in enumerate(auth_data, start=1):
            authorization = data['authorization']
            username = data['username']

            print(f"\n{Fore.LIGHTYELLOW_EX}------------------------------------")
            print(f"{Fore.LIGHTYELLOW_EX}Account {Fore.LIGHTWHITE_EX}#{account_number}")
            print(f"{Fore.LIGHTYELLOW_EX}------------------------------------")

            if choice == '1':
                total_balance += claim_tasks(authorization, username)
            elif choice == '2':
                claim_wheel(authorization, username)
            elif choice == '3':
                total_balance += claim_tasks(authorization, username)
                claim_wheel(authorization, username)

        print(f"{Fore.LIGHTWHITE_EX}Finished!")
        print(f"{Fore.LIGHTYELLOW_EX}Total Balance: {Fore.LIGHTWHITE_EX}{total_balance} AP")
        countdown_timer(28800)  # Wait for 8 hours

if __name__ == "__main__":
    main()
