# 🕸️ Web Scraper Project

A modern Python tool for extracting links, emails, social media profiles, author names, phone numbers, images, documents, tables, and metadata from any website. Output results directly to your terminal or save them in multiple formats.

---

## 🚀 Features

- Extracts:
  - Links
  - Email addresses
  - Social media profiles (Facebook, Twitter, Instagram, etc.)
  - Author names
  - Phone numbers (country-specific)
  - Images (with optional download)
  - Documents (PDF, DOCX, XLSX, etc.)
  - Tables (with optional CSV export)
  - Metadata (title, meta tags)
- Output to terminal (with colors) or file
- Supports TXT, JSON, CSV, Markdown, Excel, and SQLite formats
- Recursive and parallel scraping
- Live preview mode
- Scheduled scraping
- Data filtering and processing (deduplication, sorting)
- Modular codebase for easy extension

---

## 📦 Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Togeee12/web-scraper-project.git
   cd web-scraper-project
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## 📝 Usage

Run the scraper from the command line:

```sh
python main.py --url <website_url> --output <terminal|file> [options]
```

**Key Arguments:**
- `--url`               (required): Website URL to scrape.
- `--output`:           Output mode (`terminal` or `file`).
- `--format`:           File format (`txt`, `json`, `csv`, `md`, `xlsx`, `sqlite`).
- `--filename`:         Output filename.
- `--country`:          Country code for phone numbers (default: `US`).
- `--depth`:            Depth for recursive scraping.
- `--recursive`:        Enable recursive scraping.
- `--parallel`:         Enable parallel scraping.
- `--urls`:             List of URLs for parallel scraping.
- `--max-workers`:      Number of parallel workers.
- `--schedule`:         Schedule scraping every X hours.
- `--schedule-output`:  Output file for scheduled scraping.
- `--filter-keyword`:   Filter results by keyword.
- `--filter-regex`:     Filter results by regex pattern.
- `--process`:          Deduplicate and sort data.
- `--download-images`:  Download images locally.
- `--live-preview`:     Enable live preview mode.

**Examples:**

- Output to terminal:
  ```sh
  python main.py --url https://example.com --output terminal
  ```

- Output to file (JSON):
  ```sh
  python main.py --url https://example.com --output file --format json --filename results.json
  ```

- Recursive scraping:
  ```sh
  python main.py --url https://example.com --recursive --depth 2
  ```

- Parallel scraping:
  ```sh
  python main.py --parallel --urls https://site1.com https://site2.com --output file --format csv
  ```

- Live preview:
  ```sh
  python main.py --url https://example.com --live-preview
  ```

---

## 🗂️ Project Structure

```
web-scraper-project/
├── config.json
├── CONTRIBUTING.md
├── main.py
├── README.md
├── requirements.txt
└── scraper/
    ├── extractors.py
    ├── output.py
    └── scraper.py
```

---

## 🛠️ Dependencies

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)
- [colorama](https://pypi.org/project/colorama/)
- [phonenumbers](https://pypi.org/project/phonenumbers/)
- [tqdm](https://pypi.org/project/tqdm/)
- [pandas](https://pypi.org/project/pandas/) (for Excel/CSV export)
- [openpyxl](https://pypi.org/project/openpyxl/) (for Excel export)
- [schedule](https://pypi.org/project/schedule/) (for scheduled scraping)

Install all dependencies with:
```sh
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome!  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License. See [LICENSE](https://opensource.org/license/mit/) for details.

---

## 🙏 Acknowledgments

- Created by [Togeee12](https://github.com/Togeee12)
- Thanks to the developers of the Python libraries
