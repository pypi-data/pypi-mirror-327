from colorama import init, Fore, Style

# Initialize colorama with autoreset so the style resets automatically after each print.
init(autoreset=True)

def success(message: str):
    print(f"{Fore.GREEN}[✅] {message}{Style.RESET_ALL}")

def warning(message: str):
    print(f"{Fore.YELLOW}[ ! ] {message}{Style.RESET_ALL}")

def error(message: str):
    print(f"{Fore.RED}[❌] {message}{Style.RESET_ALL}")
