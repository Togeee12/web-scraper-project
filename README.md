# Web Scraper Project

A modern Python tool for extracting links, emails, social media profiles, author names, and phone numbers from any website. Output results directly to your terminal or save them to a file.

---

## 🚀 Features

- Extracts:
  - Links
  - Email addresses
  - Social media links (e.g., Facebook)
  - Author names
  - Phone numbers
- Output to terminal or file
- Easy command-line usage
- Colorful terminal output (with Colorama)
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
python main.py --url <website_url> --output <terminal|file> [--country <country_code>]
```

**Arguments:**
- `--url` (required): The website URL to scrape.
- `--output` (required): Output mode, either `terminal` or `file`.
- `--country` (optional): Country code for phone number extraction (e.g., `PL`).

**Examples:**

- Output to terminal:
  ```sh
  python main.py --url https://check.me --output terminal
  ```

- Output to file:
  ```sh
  python main.py --url https://check.me --output file
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


Install all dependencies with:
```sh
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome!  
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License. See [LICENSE](https://opensource.org/license/mit/) for details.

---

## 🙏 Acknowledgments

- Created by [Togeee12](https://github.com/Togeee12)
- Thanks to the developers of the Python libraries
