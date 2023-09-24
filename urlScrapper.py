import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style


# Function to fetch HTML content from a URL
def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(
            f"{Fore.RED}Failed to retrieve the page. Status code: {response.status_code}{Style.RESET_ALL}"
        )
        return None


# Function to extract and print links from HTML content
def extract_links(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    all_links = soup.find_all("a")
    links = [link.get("href") for link in all_links if link.get("href")]
    return links


# Function to extract and print email addresses from HTML content
def extract_emails(html_content):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    emails = re.findall(email_pattern, html_content)
    return emails


# Function to extract and print social media links (e.g., Facebook)
def extract_social_media_links(html_content, social_media_domain):
    soup = BeautifulSoup(html_content, "html.parser")
    social_links = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if social_media_domain in a["href"]
    ]
    return social_links


# Function to extract and print author names from HTML content
def extract_author_names(html_content, author_class):
    soup = BeautifulSoup(html_content, "html.parser")
    author_names = [p.text.strip() for p in soup.find_all("p", class_=author_class)]
    return author_names


# Function to extract and print phone numbers from HTML content
def extract_phone_numbers(html_content):
    phone_pattern = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
    phone_numbers = re.findall(phone_pattern, html_content)
    return phone_numbers


# Function to save data to a file
def save_to_file(data, filename):
    with open(filename, "w") as file:
        for item in data:
            file.write(item + "\n")


# Main scraping logic
if __name__ == "__main__":
    url = input("Enter the URL you want to scrape: ")
    html_content = get_html_content(url)

    if html_content:
        output_choice = input("Choose output format (1 for terminal, 2 for file): ")

        if output_choice == "1":
            print("\n" + Fore.BLUE + "===[ Links ]===" + Style.RESET_ALL)
            links = extract_links(html_content)
            for link in links:
                print(link)

            print("\n" + Fore.BLUE + "===[ Email Addresses ]===" + Style.RESET_ALL)
            emails = extract_emails(html_content)
            for email in emails:
                print(email)

            print("\n" + Fore.BLUE + "===[ Facebook Links ]===" + Style.RESET_ALL)
            facebook_links = extract_social_media_links(html_content, "facebook.com")
            for link in facebook_links:
                print(link)

            print("\n" + Fore.BLUE + "===[ Author Names ]===" + Style.RESET_ALL)
            author_names = extract_author_names(html_content, "author")
            for name in author_names:
                print(name)

            print("\n" + Fore.BLUE + "===[ Phone Numbers ]===" + Style.RESET_ALL)
            phone_numbers = extract_phone_numbers(html_content)
            for phone in phone_numbers:
                print(phone)

        elif output_choice == "2":
            filename = input("Enter the filename to save the data: ")
            with open(filename, "w") as file:
                file.write(f"Scraped data from {url}\n\n")

            with open(filename, "a") as file:
                file.write("=== Links ===\n")
                links = extract_links(html_content)
                for link in links:
                    file.write(link + "\n")

                file.write("\n=== Email Addresses ===\n")
                emails = extract_emails(html_content)
                for email in emails:
                    file.write(email + "\n")

                file.write("\n=== Facebook Links ===\n")
                facebook_links = extract_social_media_links(
                    html_content, "facebook.com"
                )
                for link in facebook_links:
                    file.write(link + "\n")

                file.write("\n=== Author Names ===\n")
                author_names = extract_author_names(html_content, "author")
                for name in author_names:
                    file.write(name + "\n")

                file.write("\n=== Phone Numbers ===\n")
                phone_numbers = extract_phone_numbers(html_content)
                for phone in phone_numbers:
                    file.write(phone + "\n")

            print(f"Data saved to {filename}")

        else:
            print(
                "Invalid choice. Please enter 1 for terminal output or 2 for file output."
            )

    # Your name as a signature
    print("\n" + Fore.GREEN + "Scraped by Togeee12" + Style.RESET_ALL)
