import streamlit as st
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Add it to the .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def extract_elements(url):
    """Extract UI elements from a webpage."""
    options = Options()
    options.add_argument("--headless")  # Run headless Chrome
    service = Service("C:\\Users\\PRADEEPAN\\Downloads\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    elements = {
        "buttons": [btn.get_text() for btn in soup.find_all("button")],
        "links": [a.get("href") for a in soup.find_all("a") if a.get("href")],
        "inputs": [inp.get("name") for inp in soup.find_all("input") if inp.get("name")],
        "forms": [form.get("action") for form in soup.find_all("form") if form.get("action")]
    }
    
    with open("elements.json", "w") as f:
        json.dump(elements, f, indent=4)
    
    return elements

def generate_test_cases(elements):
    """Generate test cases using Gemini 1.5 Flash."""
    prompt = f"""Generate 3 to 5 test cases for a webpage containing these elements:
    {json.dumps(elements)}
    Each test case should have:
    - Test Case ID
    - Test Scenario
    - Steps to Execute
    - Expected Result
    """
    
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    
    test_cases = response.text
    structured_test_cases = extract_test_cases(test_cases)
    df = pd.DataFrame(structured_test_cases)
    df.to_excel("test_cases.xlsx", index=False)
    
    return df

def extract_test_cases(response_text):
    """Parses the Gemini response and extracts structured test cases."""
    test_cases = []
    
    # Split response into sections (each test case starts with **Test Case ID:**)
    raw_cases = response_text.split("**Test Case ID:**")[1:]  

    for case in raw_cases:
        lines = case.strip().split("\n")  # Split into lines
        test_case = {}

        # Extract values using simple patterns
        test_case["Test Case ID"] = lines[0].strip()
        
        scenario_match = re.search(r"\*\*Test Scenario:\*\* (.+)", case)
        test_case["Test Scenario"] = scenario_match.group(1) if scenario_match else ""

        steps_match = re.search(r"\*\*Steps to Execute:\*\*\n(.+?)\n\*\*Expected Result:\*\*", case, re.DOTALL)
        test_case["Steps to Execute"] = steps_match.group(1).strip() if steps_match else ""

        expected_match = re.search(r"\*\*Expected Result:\*\*\s*(.+)", case, re.DOTALL)
        test_case["Expected Result"] = expected_match.group(1).strip() if expected_match else ""

        test_cases.append(test_case)

    return test_cases

def generate_selenium_scripts(test_cases):
    """Generate Selenium scripts for test cases using AI."""
    prompt = f"""Generate Python Selenium scripts for these test cases:
    {test_cases.to_json(orient='records', indent=4)}
    The output should contain:
    - Test Case ID
    - Python Selenium Code (as a string)"""
    
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    
    scripts = response.text
    extracted_cases = extract_script_cases(scripts)
    
    df = pd.DataFrame(extracted_cases)
    df.to_excel("test_scripts.xlsx", index=False)
    
    return df

def extract_script_cases(response_text):
    """Extract structured test cases from Gemini's response."""
    test_cases = []
    
    # Regex pattern to extract test case sections
    pattern = r'{"Test Case ID": "(.*?)",\s*"Test Scenario": "(.*?)",\s*"Python Selenium Code":\s*"""(.*?)"""'
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    for match in matches:
        test_case = {
            "Test Case ID": match[0],
            "Test Scenario": match[1],
            "Python Selenium Code": match[2].strip()
        }
        test_cases.append(test_case)
    
    return test_cases

# Streamlit UI
st.title("AI-Powered Web Testing Tool")
url = st.text_input("Enter Website URL")

if st.button("Extract UI Elements"):
    elements = extract_elements(url)
    st.session_state["elements"] = elements
    
    # Save elements.json
    with open("elements.json", "w") as f:
        json.dump(elements, f, indent=4)
    st.session_state["elements_file"] = "elements.json"

    st.success("UI Elements extracted and saved as elements.json")

    test_cases = generate_test_cases(elements)
    st.session_state["test_cases"] = test_cases
    
    # Save test_cases.xlsx
    test_cases.to_excel("test_cases.xlsx", index=False)
    st.session_state["test_cases_file"] = "test_cases.xlsx"

    st.success("Test cases generated and saved as test_cases.xlsx")

    test_scripts = generate_selenium_scripts(test_cases)
    st.session_state["test_scripts"] = test_scripts
    
    # Save test_scripts.xlsx
    test_scripts.to_excel("test_scripts.xlsx", index=False)
    st.session_state["test_scripts_file"] = "test_scripts.xlsx"

    st.success("Selenium scripts generated and saved as test_scripts.xlsx")

# Ensure session state has data before allowing downloads
if "elements" in st.session_state and "elements_file" in st.session_state:
    st.json(st.session_state["elements"])
    with open(st.session_state["elements_file"], "rb") as f:
        st.download_button("Download elements.json", f, "elements.json")

if "test_cases" in st.session_state and "test_cases_file" in st.session_state:
    st.dataframe(st.session_state["test_cases"])
    with open(st.session_state["test_cases_file"], "rb") as f:
        st.download_button("Download test_cases.xlsx", f, "test_cases.xlsx")

if "test_scripts" in st.session_state and "test_scripts_file" in st.session_state:
    st.dataframe(st.session_state["test_scripts"])
    with open(st.session_state["test_scripts_file"], "rb") as f:
        st.download_button("Download test_scripts.xlsx", f, "test_scripts.xlsx")
