import requests
import json
import urllib.parse
import os
from datetime import datetime
import time
from colorama import *
import pytz

wib = pytz.timezone('Asia/Jakarta')

class Agent301:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.agent301.org',
            'Origin': 'https://telegram.agent301.org',
            'Pragma': 'no-cache',
            'Referer': 'https://telegram.agent301.org/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Jangan Lupa {Fore.BLUE + Style.BRIGHT} DI TUYUL
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim{Fore.YELLOW + Style.BRIGHT}<AGENT 301>
            """
        )

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            return {
                'first_name': first_name,
                'last_name': last_name
            }
        else:
            raise ValueError("User data not found in query.")
        
    def get_me(self, query: str):
        url = "https://api.agent301.org/getMe"
        self.headers.update({ 
            'Authorization': query,
            'Content-Type': 'application/json'
        })
        
        try:
            response = self.session.post(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if data.get("ok"):
                return data.get('result', {})
            else:
                return None
        
        except requests.exceptions.HTTPError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}HTTP error occurred: {e}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Request error occurred: {e}{Style.RESET_ALL}")
        except ValueError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}JSON decode error: {e}{Style.RESET_ALL}")
        return None
    
    def get_tasks(self, query: str):
        url = "https://api.agent301.org/getTasks"
        self.headers.update({ 
            'Authorization': query,
            'Content-Type': 'application/json'
        })
        
        try:
            response = self.session.post(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if data.get("ok"):
                return data.get('result', {})
            else:
                return None
        
        except requests.exceptions.HTTPError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}HTTP error occurred: {e}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Request error occurred: {e}{Style.RESET_ALL}")
        except ValueError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}JSON decode error: {e}{Style.RESET_ALL}")
        return None
    
    def complete_tasks(self, query: str, task_type: str, title: str):
        url = "https://api.agent301.org/completeTask"
        self.headers.update({ 
            'Authorization': query,
            'Content-Type': 'application/json'
        })
        body = {
            "type": task_type
        }
        
        try:
            response = self.session.post(url, headers=self.headers, data=json.dumps(body))
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                result = data.get('result', {})
                is_completed = result.get('is_completed', False)
                reward = result.get('reward', 0)
                balance = result.get('balance', 0)

                if is_completed:
                    self.log(
                        f"{Fore.GREEN + Style.BRIGHT}[ Task ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {task_type.upper()} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}Completed{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.GREEN + Style.BRIGHT}[ Task ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}|{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} [ Reward ] {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{reward}{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ New Balance ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {balance} {Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.YELLOW + Style.BRIGHT}[ Task ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {task_type.upper()} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                    )
                return is_completed
            else:
                self.log(
                    f"{Fore.RED + Style.BRIGHT}[ Task ] Failed to complete task{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {task_type.upper()} {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                )
                return None
        
        except requests.exceptions.HTTPError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}HTTP error occurred: {e}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Request error occurred: {e}{Style.RESET_ALL}")
        except ValueError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}JSON decode error: {e}{Style.RESET_ALL}")
        return None
    
    def load_wheel(self, query: str):
        url = "https://api.agent301.org/wheel/load"
        self.headers.update({ 
            'Authorization': query,
            'Content-Type': 'application/json'
        })

        try:
            response = self.session.post(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if data.get("ok"):
                return data.get('result', {})
            else:
                return None

        except requests.exceptions.HTTPError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}HTTP error occurred: {e}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Request error occurred: {e}{Style.RESET_ALL}")
        except ValueError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}JSON decode error: {e}{Style.RESET_ALL}")
        return None
    
    def spin_wheel(self, query: str):
        url = "https://api.agent301.org/wheel/spin"
        self.headers.update({ 
            'Authorization': query,
            'Content-Type': 'application/json'
        })

        try:
            response = self.session.post(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if data.get("ok"):
                return data.get('result', {})
            else:
                return None

        except requests.exceptions.HTTPError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}HTTP error occurred: {e}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Request error occurred: {e}{Style.RESET_ALL}")
        except ValueError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}JSON decode error: {e}{Style.RESET_ALL}")
        return None
    
    def process_query(self, query: str):
        try:
            user = self.load_data(query)
            authorization = query.strip()

            if user:
                self.log(
                        f"{Fore.CYAN+Style.BRIGHT}[ Name{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {user['first_name']} {user['last_name']} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            
            get_me = self.get_me(authorization)
            if get_me:
                tickets = get_me.get('tickets', 0)
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}[ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {get_me['balance']} {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}[ Ticket{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {tickets} {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}[ Streak{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {get_me['daily_streak']['day']} {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            
            get_tasks = self.get_tasks(authorization)
            if get_tasks:
                tasks = get_tasks.get('data', [])
                if tasks:
                    for task in tasks:
                        task_type = task.get("type")
                        title = task.get("title")
                        is_claimed = task.get("is_claimed", False)
                        count = task.get("count", 0)
                        max_count = task.get("max_count")

                        if max_count is None and not is_claimed:
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}[ Task ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {task_type.upper()} {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                            )
                            time.sleep(1)
                            self.complete_tasks(authorization, task_type, title)

                        elif task_type == "video" and count < max_count:
                            while count < max_count:
                                self.log(
                                    f"{Fore.GREEN + Style.BRIGHT}[ Task ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task_type.upper()} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}[ Progress ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {count} {Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT}/{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {max_count} {Style.RESET_ALL}"
                                )
                                time.sleep(1)
                                if self.complete_tasks(authorization, task_type, title):
                                    count += 1
                                else:
                                    break

                        elif not is_claimed and count >= max_count:
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}[ Task ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {task_type.upper()} {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                            )
                            time.sleep(1)
                            self.complete_tasks(authorization, task_type, title)

                while tickets > 0:
                    wheel = self.load_wheel(authorization)
                    if wheel:
                        spin = self.spin_wheel(authorization)
                        if spin:
                            current_tickets = spin.get('tickets', 0)
                            self.log(f"{Fore.BLUE + Style.BRIGHT}[ Spin Wheel ] Mencoba melakukan spin wheel...{Style.RESET_ALL}")
                            time.sleep(5)

                            tickets = current_tickets
                            if tickets > 0:
                                # self.log(f"{Fore.GREEN + Style.BRIGHT}[ Spin Wheel ] Sukses{Style.RESET_ALL}")
                                self.log(
                                    f"{Fore.GREEN + Style.BRIGHT}[ Rewards{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {spin['reward']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}[ Ticket{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {current_tickets} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.GREEN + Style.BRIGHT}[ TON{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {spin['toncoin']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}[ NOT{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {spin['notcoin']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}[ Balance{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {spin['balance']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(f"{Fore.YELLOW + Style.BRIGHT}[ Spin Wheel ] Tidak ada ticket tersisa{Style.RESET_ALL}")
                                break
                        else:
                            self.log(f"{Fore.RED + Style.BRIGHT}[ Spin Wheel ] Failed to spin the wheel{Style.RESET_ALL}")
                            break
                    else:
                        self.log(f"{Fore.RED + Style.BRIGHT}[ Spin Wheel ] Failed to load the wheel{Style.RESET_ALL}")
                        break

            self.log(f"{Fore.CYAN + Style.BRIGHT}-------------------------------------------------------------------{Style.RESET_ALL}")

        except ValueError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}ValueError: {e}{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.log(f"{Fore.RED + Style.BRIGHT}HTTP error occurred: {e}{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Error processing query: {e}{Style.RESET_ALL}")

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                time.sleep(1)
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-------------------------------------------------------------------{Style.RESET_ALL}")
                
                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)

                seconds = 1800
                while seconds > 0:
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {seconds} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}seconds ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Agent301 - BOT.{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    agent301 = Agent301()
    agent301.main()
