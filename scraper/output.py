import json 
import csv
from colorama import Fore, Style


def print_to_terminal(data):
    print(Fore.GREEN + "\nExtracted Links:" + Style.RESET_ALL, data.get('links'))
    print(Fore.CYAN + "\nEmails:" + Style.RESET_ALL, data.get('emails'))
    print(Fore.MAGENTA + "\nSocial Media Links:" + Style.RESET_ALL, data.get('social'))
    print(Fore.YELLOW + "\nAuthor Names:" + Style.RESET_ALL, data.get('authors'))
    print(Fore.RED + "\nPhone Numbers:" + Style.RESET_ALL, data.get('phones'))
    
def save_to_file(data, filename, format="txt"):
    if format == "txt":
        with open(filename, 'w') as f:
            f.write(f"Links:\n{data.get('links')}\n")
            f.write(f"Emails:\n{data.get('links')}\n")
            f.write(f"Social Media:\n{data.get('links')}\n")
            f.write(f"Authors:\n{data.get('links')}\n")
            f.write(f"Phones:\n{data.get('links')}\n")
    elif format == "json":
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    elif format == "csv":
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Data"])
            for key, value in data.items():
                writer.writerow([key, value])