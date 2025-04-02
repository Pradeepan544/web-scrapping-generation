# AI-Powered Web Scrapping & Testing Tool

## Overview
This project is an AI-powered web testing tool that extracts UI elements from a given website, generates test cases and Selenium scripts using Gemini 1.5 Flash, and saves them as downloadable files. The tool is built with **Streamlit** for a simple UI, **Selenium** and **BeautifulSoup** for web scraping, and **regular expressions (re)** for extracting structured test cases and Selenium scripts from the AI-generated text.

## Features
- Extracts buttons, links, input fields, and forms from a given webpage.
- Generates test cases using **Gemini 1.5 Flash**.
- Converts extracted test cases into structured **JSON format**.
- Generates **Selenium scripts** for automated UI testing.
- Saves results as **JSON and Excel files**.
- Provides a **Streamlit-based UI** for easy interaction.

## Installation
### Prerequisites
Ensure you have **Python 3.7+** installed.

### Install Required Packages
Run the following command to install dependencies:
```sh
pip install streamlit requests pandas beautifulsoup4 selenium webdriver-manager google-generativeai python-dotenv openpyxl
```

## Usage
1. **Set Up the API Key:**
   - Create a `.env` file in the project directory.
   - Add your **Gemini API Key**:
     ```sh
     GEMINI_API_KEY=your_api_key_here
     ```

2. **Run the Streamlit App:**
   ```sh
   streamlit run app.py
   ```

3. **Interact with the UI:**
   - Enter a website URL.
   - Click the **Extract UI Elements** button.
   - Download the generated files (`elements.json`, `test_cases.xlsx`, `test_scripts.xlsx`).

## Approach
1. **Web Scraping with Selenium & BeautifulSoup**
   - Uses **Selenium** to load the webpage.
   - Extracts **buttons, links, input fields, and forms** using **BeautifulSoup**.
   - Saves extracted elements into a `JSON` file.

2. **Test Case Generation using Gemini 1.5 Flash**
   - Sends extracted elements as a prompt to **Gemini 1.5 Flash**.
   - Generates test cases with:
     - Test Case ID
     - Test Scenario
     - Steps to Execute
     - Expected Result
   - Extracts structured test cases using **regular expressions (re)**.
   - Saves them in an **Excel file**.

3. **Selenium Script Generation**
   - Generates **Python Selenium scripts** using AI.
   - Extracts scripts using **regular expressions (re)**.
   - Saves scripts in an **Excel file**.

4. **Streamlit UI for User Interaction**
   - Provides an **input field** for URL entry.
   - Displays extracted data in a **structured table**.
   - Allows users to **download** the generated files easily.

## Output Files
- `elements.json` - Extracted UI elements from the webpage.
- `test_cases.xlsx` - Generated test cases.
- `test_scripts.xlsx` - Selenium test scripts.

## License
This project is licensed under the **MIT License**.

## Author
[Shanmuga Pradeepan R](https://github.com/your-github-profile)

## Contributing
Feel free to contribute by submitting a **pull request** or reporting **issues**!

---
Give it a ⭐ if you find it useful! 🚀
