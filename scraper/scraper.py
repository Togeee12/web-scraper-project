import requests

def fetch_html(url):
    """Fetch HTML content from a given URL!"""
    try: 
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
    