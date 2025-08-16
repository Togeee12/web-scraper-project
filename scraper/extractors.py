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
        'youtube': [l for l in social_links if 'youtube.com' in l or 'youtu.be' in l],
        'tiktok': [l for l in social_links if 'tiktok.com' in l],
        'pinterest': [l for l in social_links if 'pinterest.com' in l],
        'github': [l for l in social_links if 'github.com' in l],
    }
    return social

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

def extract_images(html, download=False, download_path='images'):
    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all('img')
    img_urls = [img.get('src') for img in img_tags if img.get('src')]

    if download:
        import os 
        import requests
        from urllib.parse import urlparse

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        downloaded_images = []
        for i, img_url in enumerate(img_urls):
            try:
                if not bool(urlparse(img_url).netloc):
                    continue

                img_data = requests.get(img_url).content
                img_extension = os.path.splitext(urlparse(img_url).path)[1]
                if not img_extension:
                    img_extension = '.jpg'

                filename = os.path.join(download_path, f"image_{i}{img_extension}")
                with open(filename, "wb") as f:
                    f.write(img_data)
                downloaded_images.append(filename)
            except Exception as e:
                print(f"Error downloading image {img_url}: {e}")
        return downloaded_images
    return img_urls

def extract_metadata(html):
    soup = BeautifulSoup(html, "html.parser")
    metadata = {}

    title_tag = soup.find('title')
    metadata['title'] = title_tag.text if title_tag else ""

    meta_tags = soup.find_all('meta')
    for tag in meta_tags: 
        name = tag.get('name') or tag.get('property')
        if name: 
            content = tag.get('content', '')
            if name in metadata:
                if isinstance(metadata[name], list):
                    metadata[name].append(content)
                else:
                    metadata[name] = [metadata[name], content]
            else:
                metadata[name] = content
    return metadata

def extract_document_links(html):
    soup = BeautifulSoup(html, "html.parser")
    all_links = [a['href'] for a in soup.find_all('a', href = True)]

    document_extensions = ['.pdf','.doc','.docx','.xls','.xlsx','.ppt','.pptx']
    document_links = [link for link in all_links if any(link.lower().endswith(ext) for ext in document_extensions)]

    return document_links

def extract_tables(html, save_csv=False, csv_path='tables'):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all('table')
    
    if not tables:
        return []
    
    extracted_tables = []
    
    if save_csv:
        import os
        try:
            import pandas as pd
        except ImportError:
            print("Warning: pandas not installed. Tables will be extracted as HTML.")
            save_csv = False
    
    if save_csv:
        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
            
        for i, table in enumerate(tables):
            try:
                df = pd.read_html(str(table))[0]
                csv_file = os.path.join(csv_path, f"table_{i}.csv")
                df.to_csv(csv_file, index=False)
                extracted_tables.append({
                    'table_index': i,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'csv_file': csv_file
                })
            except Exception as e:
                print(f"Error processing table {i}: {e}")
    else:
        for i, table in enumerate(tables):
            rows = table.find_all('tr')
            table_data = []
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                table_data.append(row_data)
            
            extracted_tables.append({
                'table_index': i,
                'data': table_data
            })
    
    return extracted_tables