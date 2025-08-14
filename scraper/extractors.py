import re
from bs4 import BeautifulSoup
import phonenumbers

def extract_emails(html):
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html)

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    return [a['href'] for a in soup.find_all('a', href=True)]

def extract_social_links(html):
    soup = BeautifulSoup(html, "html.parser")
    social_links = [a['href'] for a in soup.find_all('a', href=True)]
    social = {
        'facebook': [l for l in social_links if 'facebook.com' in l],
        'twitter': [l for l in social_links if 'twitter.com' in l],
        'instagram': [l for l in social_links if 'instagram.com' in l],
        'linkedin': [l for l in social_links if 'linkedin.com' in l],
    }
    return social_links

def extract_phone_numbers(html, country_code="US"):
    numbers = []

    for match in phonenumbers.PhoneNumberMatcher(html, country_code.upper()):
        phone_number = match.number
        formated_number = phonenumbers.format_number(
            phone_number, phonenumbers.PhoneNumberFormat.E164
        )
        numbers.append(formated_number)
    return numbers

def extract_author_names(html):
    soup = BeautifulSoup(html, "html.parser")
    authors = [meta.get('content') for meta in soup.find_all('meta', attrs={'name':'author'})]
    return authors

