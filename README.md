
# Web Scraping Tool

A Python script for web scraping that extracts various types of data (links, email addresses, social media links, author names, and phone numbers) from a given URL. It provides both terminal and file-based output options.

## Table of Contents

- [Web Scraping Tool](#web-scraping-tool)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Running the Script](#running-the-script)
    - [Output Options](#output-options)
      - [Terminal Output](#terminal-output)
      - [File Output](#file-output)
  - [Dependencies](#dependencies)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

Before running the script, you need to have Python 3.x installed on your system. If you don't have it, you can download it from the [official Python website](https://www.python.org/downloads/).

### Installation

1. Clone this repository to your local machine using Git or download it as a ZIP archive and extract it.

2. Navigate to the project directory:

   ```shell
   cd web-scraper-project
   ```

3. Install the required Python dependencies using pip:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

### Running the Script

1. Run the `urlScrapper.py` script:

   ```shell
   python urlScrapper.py
   ```

2. Enter the URL you want to scrape when prompted.

3. Choose the output format:
   - Enter `1` for terminal output.
   - Enter `2` to save the data to a file.

### Output Options

#### Terminal Output

If you choose terminal output (`1`), the script will display the following information in the terminal:

- Extracted Links
- Extracted Email Addresses
- Extracted Facebook Links
- Extracted Author Names
- Extracted Phone Numbers

#### File Output

If you choose file output (`2`), you will be prompted to enter a filename. The script will save the extracted data to a file with the following structure:

- Scraped data from [URL]
  - Links
  - Email Addresses
  - Facebook Links
  - Author Names
  - Phone Numbers

## Dependencies

This project relies on the following Python libraries, which are listed in the `requirements.txt` file:

- `beautifulsoup4`: Used for parsing HTML content.
- `requests`: Used for making HTTP requests to fetch HTML content.
- `colorama`: Used for terminal text color formatting.

You can install these dependencies using the `pip install -r requirements.txt` command, as mentioned in the installation instructions.

## Contributing

Contributions are welcome! If you have any improvements, bug fixes, or new features to add, please open an issue or create a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit/) file for details.

## Acknowledgments

- This project was created by [Togeee12].
- Special thanks to the developers of the Python libraries used in this project.
