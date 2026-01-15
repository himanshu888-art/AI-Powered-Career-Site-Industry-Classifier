This project automates the extraction of company data from an internal dashboard, classifies career site industries using Microsoft Copilot AI via Selenium automation, and generates executive-assigned Excel reports with sleep-proof execution.
​

Key Features
Single undetected ChromeDriver instance handles dashboard login, API token extraction, and Copilot interactions without restarts.
​

Fetches paginated OMS mapping data (up to 50 pages), filters Workable statuses, and round-robin assigns to 5 executives (Himanshu, Gaurav, Amit, Prashant, Shekhar).
​

Auto-logs into Copilot, sends company URL prompts against a predefined industry reference list, extracts structured "Industry: <name>\nProfile: <summary>" responses using BeautifulSoup and clipboard.
​

Prevents laptop sleep during long runs via Windows API (ctypes), ensuring uninterrupted processing.
​

Outputs individual executive inputs/outputs, combined summary Excel, and executive performance stats.

Tech Stack
Core: Selenium with undetected-chromedriver, BeautifulSoup, Pandas

AI: Microsoft Copilot for zero-shot industry classification from career sites

Utils: Pyperclip, WebDriverWait, Requests for API, XPath/CSS selectors

OS: Windows-specific sleep prevention; Chrome v139 compatible
​

Quick Setup
Install dependencies: pip install selenium undetected-chromedriver pandas beautifulsoup4 pyperclip webdriver-manager openpyxl requests

Update credentials in script (COPILOT_EMAIL, DASHBOARD_USERNAME/PASSWORD, URLs, paths).

Set REFERENCE_PATH to your industry Excel sheet.

Run: python main.py

Files generate in C:\Users\Himanshu.tanwar\new+project dated folders.
​

Output Files
Executive	Input File	Output File
himanshu	input_himanshu_YYYY-MM-DD.xlsx	output_himanshu_YYYY-MM-DD.xlsx
gaurav	input_gaurav_YYYY-MM-DD.xlsx	output_gaurav_YYYY-MM-DD.xlsx
amit	input_amit_YYYY-MM-DD.xlsx	output_amit_YYYY-MM-DD.xlsx
prashant	input_prashant_YYYY-MM-DD.xlsx	output_prashant_YYYY-MM-DD.xlsx
shekhar	input_shekhar_YYYY-MM-DD.xlsx	output_shekhar_YYYY-MM-DD.xlsx
Combined: combined_executive_data_YYYY-MM-DD.xlsx

Raw: omsmapping_data_YYYY-MM-DD.csv
​

Usage Notes
Script processes ~500 companies daily across executives, matching against your industry reference for HR-tech efficiency. Customize TOTAL_PAGES or executive list as needed. Handles Google OAuth popups robustly
