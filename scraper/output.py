import csv
from colorama import Fore, Style

def print_to_terminal(data):
    # Links in blue
    print(Fore.BLUE + "\nExtracted Links:" + Style.RESET_ALL)
    for link in data.get('links', []):
        print(f"  {Fore.CYAN}{link}{Style.RESET_ALL}")
    
    # Emails in green
    print(Fore.GREEN + "\nEmails:" + Style.RESET_ALL)
    for email in data.get('emails', []):
        print(f"  {Fore.GREEN}{email}{Style.RESET_ALL}")
    
    # Social media links in magenta
    print(Fore.MAGENTA + "\nSocial Media Links:" + Style.RESET_ALL)
    social = data.get('social', {})
    for platform, links in social.items():
        print(f"  {Fore.YELLOW}{platform}:{Style.RESET_ALL}")
        for link in links:
            print(f"    {Fore.MAGENTA}{link}{Style.RESET_ALL}")
    
    # Author names in yellow
    print(Fore.YELLOW + "\nAuthor Names:" + Style.RESET_ALL)
    for author in data.get('authors', []):
        print(f"  {Fore.YELLOW}{author}{Style.RESET_ALL}")
    
    # Phone numbers in red
    print(Fore.RED + "\nPhone Numbers:" + Style.RESET_ALL)
    for phone in data.get('phones', []):
        print(f"  {Fore.RED}{phone}{Style.RESET_ALL}")
    
    # Images in cyan
    print(Fore.CYAN + "\nImages:" + Style.RESET_ALL)
    for img in data.get('images', []):
        print(f"  {Fore.CYAN}{img}{Style.RESET_ALL}")
    
    # Metadata in white
    print(Fore.WHITE + "\nMetadata:" + Style.RESET_ALL)
    metadata = data.get('metadata', {})
    for key, value in metadata.items():
        print(f"  {Fore.WHITE}{key}:{Style.RESET_ALL} {value}")
    
    # Documents in blue
    print(Fore.BLUE + "\nDocuments:" + Style.RESET_ALL)
    for doc in data.get('documents', []):
        print(f"  {Fore.BLUE}{doc}{Style.RESET_ALL}")
    
    # Tables in white
    print(Fore.WHITE + "\nTables:" + Style.RESET_ALL)
    tables = data.get('tables', [])
    for i, table in enumerate(tables):
        print(f"  {Fore.WHITE}Table {i}:{Style.RESET_ALL}")
        if isinstance(table, dict) and 'data' in table:
            for row in table['data'][:5]:
                print(f"    {row}")
            if len(table['data']) > 5:
                print(f"    ... and {len(table['data']) - 5} more rows")

def save_to_file(data, filename, format="txt"):
    if format == "txt":
        with open(filename, 'w') as f:
            f.write(f"Links:\n{data.get('links')}\n")
            f.write(f"Emails:\n{data.get('emails')}\n")
            f.write(f"Social Media:\n{data.get('social')}\n")
            f.write(f"Authors:\n{data.get('authors')}\n")
            f.write(f"Phones:\n{data.get('phones')}\n")
            f.write(f"Images:\n{data.get('images')}\n")
            f.write(f"Metadata:\n{data.get('metadata')}\n")
            f.write(f"Documents:\n{data.get('documents')}\n")
            f.write(f"Tables:\n{data.get('tables')}\n")
    elif format == "json":
        import json
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    elif format == "csv":
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Data"])
            for key, value in data.items():
                writer.writerow([key, value])
    elif format == "md":
        with open(filename, 'w') as f:
            f.write("# Web Scraping Results\n\n")
            f.write(f"## Links\n\n{data.get('links')}\n\n")
            f.write(f"## Emails\n\n{data.get('emails')}\n\n")
            f.write(f"## Social Media\n\n{data.get('social')}\n\n")
            f.write(f"## Authors\n\n{data.get('authors')}\n\n")
            f.write(f"## Phone Numbers\n\n{data.get('phones')}\n\n")
            f.write(f"## Images\n\n{data.get('images')}\n\n")
            f.write(f"## Metadata\n\n{data.get('metadata')}\n\n")
            f.write(f"## Documents\n\n{data.get('documents')}\n\n")
            f.write(f"## Tables\n\n{data.get('tables')}\n\n")
    elif format == "xlsx":
        try:
            import pandas as pd
            
            dfs = {}
            for key, value in data.items():
                if isinstance(value, list):
                    dfs[key] = pd.DataFrame({key: value})
                elif isinstance(value, dict):
                    dfs[key] = pd.DataFrame([value])
                else:
                    dfs[key] = pd.DataFrame({key: [value]})
            
            with pd.ExcelWriter(filename) as writer:
                for key, df in dfs.items():
                    df.to_excel(writer, sheet_name=key[:31])
        except ImportError:
            print("Error: pandas and openpyxl are required for Excel export. Install with: pip install pandas openpyxl")
    elif format == "sqlite":
        try:
            import sqlite3
            import json
            
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                data TEXT
            )
            ''')
            
            for key, value in data.items():
                cursor.execute("INSERT INTO scraping_data (category, data) VALUES (?, ?)",
                             (key, json.dumps(value)))
            
            conn.commit()
            conn.close()
        except ImportError:
            print("Error: sqlite3 is required for SQLite export.")