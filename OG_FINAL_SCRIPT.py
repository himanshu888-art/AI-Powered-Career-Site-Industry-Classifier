from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import pandas as pd
import undetected_chromedriver as uc
import pyperclip
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re
import os
import ctypes  # 🔥 ADDED: For sleep prevention

# ====== SLEEP PREVENTION SETUP 🔥 NEW ======
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def prevent_sleep():
    """Prevent system from sleeping while script runs"""
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )
    print("🛡️ System sleep PREVENTED while script runs")

def allow_sleep():
    """Allow system to sleep again"""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print("✅ System sleep ALLOWED again")

# ====== FIXED PATHS - Use RAW STRINGS (r"") ======
OUTPUT_BASE_PATH = r"C:\Users\Himanshu.tanwar\new+project"

# ====== CREDENTIALS ======
COPILOT_EMAIL = "*********************"
COPILOT_PASSWORD = "********************"
DASHBOARD_USERNAME = "******************"
DASHBOARD_PASSWORD = "****************"
LOGIN_URL = "*****************************"
BASE_URL = '*****************************************'
TOTAL_PAGES = 50
CHROME_DRIVER_PATH = r"***************************************************"
REFERENCE_PATH = r"******************************************************"

# 🔥 PREVENT SLEEP IMMEDIATELY AFTER IMPORTS
print("🚀 Initializing SINGLE WebDriver instance...")
prevent_sleep()  # 🛡️ PREVENT SLEEP FROM START

# ====== SINGLE WEBDRIVER SETUP (SHARED) ======
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

driver = uc.Chrome(version_main=139, driver_executable_path=CHROME_DRIVER_PATH, options=options)
driver.maximize_window()

# ====== FETCH DATE ======
def previous_date_from_today():
    today = datetime.today()
    previous_day = today - timedelta(days=0)
    day_name = previous_day.strftime("%A")
    date_str = previous_day.strftime("%Y-%m-%d")
    return day_name, date_str

day, date = previous_date_from_today()
print("Date:", date)

# ====== DASHBOARD LOGIN & DATA FETCH (SAME DRIVER) ======
def dashboard_login_and_fetch():
    print("🏢 Logging into Dashboard...")
    driver.get(LOGIN_URL)
    time.sleep(5)

    # Dashboard login
    username = driver.find_element(By.XPATH, "//input[@formcontrolname='username']")
    username.clear()
    username.send_keys(DASHBOARD_USERNAME)
    password_field = driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')
    password_field.clear()
    password_field.send_keys(DASHBOARD_PASSWORD)
    submit_btn = driver.find_element(By.XPATH, '//button[@class="btn btn-primary px-4"]')
    submit_btn.click()
    time.sleep(6)

    # Get token
    token = driver.execute_script("""
        var t = null;
        for (var i=0; i<localStorage.length; i++) {
            var key = localStorage.key(i);
            var val = localStorage.getItem(key);
            if (val && val.includes('.') && val.split('.').length === 3) {
                t = val;
                break;
            }
        }
        return t;
    """) or driver.execute_script("""
        var t = null;
        for (var i=0; i<sessionStorage.length; i++) {
            var key = sessionStorage.key(i);
            var val = sessionStorage.getItem(key);
            if (val && val.includes('.') && val.split('.').length === 3) {
                t = val;
                break;
            }
        }
        return t;
    """)

    print("Token obtained:", bool(token))
    
    # Navigate to mapping
    mapping = driver.find_element(By.XPATH, '//div/app-sidebar/app-sidebar-nav/app-sidebar-nav-items/app-sidebar-nav-dropdown[2]/a')
    mapping.click()
    time.sleep(2)
    oms = driver.find_element(By.XPATH, '//app-sidebar/app-sidebar-nav/app-sidebar-nav-items/app-sidebar-nav-dropdown[2]/app-sidebar-nav-items/app-sidebar-nav-link[2]/a')
    oms.click()
    time.sleep(2)
    
    return token

# ====== AUTO LOGIN TO COPILOT (SAME DRIVER) ======
def auto_login_copilot():
    wait = WebDriverWait(driver, 15)
    print("🔐 Auto-logging into Copilot...")
    
    driver.get("https://copilot.microsoft.com/")
    time.sleep(5)
    
    # 1️⃣ Click Settings (sidebar)
    try:
        sign_in_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='sidebar-settings-button']")))
        driver.execute_script("arguments[0].click();", sign_in_btn)
        print("✅ Clicked Settings")
    except:
        print("⚠️ Settings button not found, may already be logged in")
        return True
    
    # 2️⃣ Click "Sign in"
    try:
        sign_in_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space(text())='Sign in']")))
        driver.execute_script("arguments[0].click();", sign_in_button)
        print("✅ Clicked Sign in")
    except:
        print("⚠️ Sign in button not found")
        return False
    
    # 3️⃣ Click "Continue with Google"
    try:
        google_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space(text())='Continue with Google']")))
        driver.execute_script("arguments[0].click();", google_btn)
        print("✅ Clicked Google login")
    except:
        print("⚠️ Google button not found")
        return False
    
    # 4️⃣ Switch to Google popup & login
    try:
        driver.switch_to.window(driver.window_handles[-1])
        print("✅ Switched to Google login popup")
        
        # Email
        email_field = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_field.clear()
        email_field.send_keys(COPILOT_EMAIL)
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space(text())='Next']")))
        driver.execute_script("arguments[0].click();", next_btn)
        print("✅ Entered email")
        
        # Password
        password_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Passwd']")))
        password_field.send_keys(COPILOT_PASSWORD)
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space(text())='Next']")))
        driver.execute_script("arguments[0].click();", next_btn)
        print("✅ Entered password")
        
        # Switch back to main window
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(10)
        print("✅ Copilot login completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Login error: {e}")
        driver.switch_to.window(driver.window_handles[0])
        return False

# ====== STEP 1: DASHBOARD DATA FETCH 🔥 ID COLUMN ADDED ======
token = dashboard_login_and_fetch()

all_data = []
if token:
    headers = {
        'Authorization': token,
        'Referer': 'https://naukrics.infoedge.com:8083/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
    }
    
    for page in range(0, TOTAL_PAGES + 1):
        params = {'date': date, 'page': page, 'size': 10, 'sort': 'createdOn,DESC'}
        response = requests.get(BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            json_data = response.json()
            page_content = json_data.get("content", [])
            if page_content:
                df = pd.json_normalize(page_content)
                all_data.append(df)
                print(f"✅ Page {page}: {len(page_content)} records")
        else:
            print(f"❌ Page {page} failed: {response.status_code}")
            break

# Process dashboard data 🔥 ID COLUMN INCLUDED
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(f"{OUTPUT_BASE_PATH}\\omsmapping_data_{date}.csv", index=False)
    
    # 🔥 CHANGED: Include "id" column
    finaldf1 = final_df[["id", "companyName","careerSiteUrl","mappingStatus"]].copy()
    finaldf1 = finaldf1[finaldf1['mappingStatus'].isin(["Workable", "Workable-No JD"])]
    executive_name = ["Himanshu","Gaurav","amit","prashant","shekhar"]
    n_exec = len(executive_name)
    finaldf1["Executive"] = [executive_name[i % n_exec] for i in range(len(finaldf1))]
    
    print(f"🎉 Fetched {len(finaldf1)} records assigned to executives")
    finaldf1.to_csv(f"{OUTPUT_BASE_PATH}\\executive_assignment_{date}.csv", index=False)
    
    executive_dfs = {}
    for exec_name in executive_name:
        # 🔥 CHANGED: Include "id" column in executive files
        exec_df = finaldf1[finaldf1['Executive'] == exec_name][['id', 'companyName', 'careerSiteUrl']]
        if not exec_df.empty:
            exec_df.to_excel(f"{OUTPUT_BASE_PATH}\\input_{exec_name.lower()}_{date}.xlsx", index=False)
            executive_dfs[exec_name] = exec_df
            print(f"📁 Created input file for {exec_name}: {len(exec_df)} companies")
else:
    print("❌ No data fetched from dashboard")
    driver.quit()
    allow_sleep()  # 🔥 Restore sleep on early exit
    exit()

# ====== STEP 2: COPILOT LOGIN (SAME DRIVER) ======
print("\n🔄 Switching to Copilot...")
login_success = auto_login_copilot()
if not login_success:
    print("❌ Copilot login failed!")
    driver.quit()
    allow_sleep()  # 🔥 Restore sleep on early exit
    exit()

# ====== LOAD REFERENCE DATA ======
ref_df = pd.read_excel(REFERENCE_PATH, usecols=[0, 1]).dropna()
industry_list_text = ""
for _, row in ref_df.iterrows():
    label = str(row["Industry Label"]).strip()
    if label:
        industry_list_text += f"- {label}\n"

# ====== COPILOT PROCESSING FUNCTIONS (SAME DRIVER) ======
def safe_paste(retries=10, delay=0.2):
    for i in range(retries):
        try:
            return pyperclip.paste()
        except:
            time.sleep(delay)
    return ""

def send_prompt(text, wait_time=11):
    try:
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        textarea.send_keys(Keys.CONTROL + "a")
        textarea.send_keys(Keys.DELETE)
        for line in text.split('\n'):
            textarea.send_keys(line)
            textarea.send_keys(Keys.SHIFT, Keys.ENTER)
            time.sleep(0.05)
        textarea.send_keys(Keys.ENTER)
        time.sleep(wait_time)
    except Exception as e:
        print(f"❌ Send prompt error: {e}")

def click_copy_button():
    try:
        btns = driver.find_elements(By.CSS_SELECTOR, "[data-testid='copy-message-button']")
        if btns:
            btn = btns[-1]
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.4)
            btn.click()
            time.sleep(0.8)
            return True
    except:
        pass
    return False

def extract_latest_raw_reply(timeout=40, stable_wait=3, prev_text=""):
    last_text = ""
    stable_count = 0
    for sec in range(timeout):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            spans = soup.select('span.font-ligatures-none')
            if spans:
                new_text = spans[-1].get_text(strip=True, separator="\n")
                if new_text.strip() == prev_text.strip():
                    continue
                if new_text != last_text:
                    last_text = new_text
                    stable_count = 0
                else:
                    stable_count += 1
                if stable_count >= stable_wait:
                    return last_text
        except:
            pass
        print(f"⏳ Waiting... {sec+1}/{timeout}", end="\r")
        time.sleep(1)
    return last_text

def extract_clean_response(raw_text):
    if not raw_text:
        return "", ""
    cleaned = raw_text.replace("**", "").replace("\r", "").replace("\n\n", "\n").strip()
    match = re.search(r'Industry:\s*(.*?)\s*Profile:\s*(.*)', cleaned, re.DOTALL | re.IGNORECASE)
    return (match.group(1).strip(), match.group(2).strip()) if match else ("", "")

# ====== PROCESS ALL EXECUTIVES (SINGLE DRIVER) 🔥 ID COLUMN PASSED THROUGH ======
print("\n🚀 Starting fully automated Copilot processing with SINGLE DRIVER...")

all_executive_responses = []

# Send initial instruction
initial_prompt = (
    "Here is a predefined list of valid industry types:\n\n" +
    industry_list_text +
    "\nFrom now on, I will give you one company and its website. "
    "You must respond ONLY with:\nIndustry: <name>\nProfile: <3–4 line summary>"
)
send_prompt(initial_prompt)

for exec_name, exec_df in executive_dfs.items():
    print(f"\n{'='*60}")
    print(f"👤 PROCESSING EXECUTIVE: {exec_name} ({len(exec_df)} companies)")
    print(f"{'='*60}")
    
    OUTPUT_PATH = f"{OUTPUT_BASE_PATH}\\output_{exec_name}_{date}.xlsx"
    response_list = []
    last_raw = ""
    
    company_col = [col for col in exec_df.columns if 'company' in col.lower()][0]
    url_col = [col for col in exec_df.columns if 'url' in col.lower()][0]
    id_col = [col for col in exec_df.columns if 'id' in col.lower()][0]  # 🔥 NEW: ID column
    
    for idx, row in exec_df.iterrows():
        company_id = str(row[id_col]).strip()  # 🔥 NEW: Extract ID
        company = str(row[company_col]).strip()
        url = str(row[url_col]).strip()
        
        if not company or not url:
            continue
            
        print(f"🧠 Processing: {company} (ID: {company_id})")
        
        q_prompt = (
            f"What industry from the list best fits \"{company}\" based on its website: {url}?\n"
            "Format:\nIndustry: <Industry from list>\nProfile: <3–4 line summary>"
        )
        
        send_prompt(q_prompt)
        raw_response = extract_latest_raw_reply(prev_text=last_raw)
        
        copied = click_copy_button()
        if copied:
            clip = safe_paste().strip()
            if clip:
                raw_response = clip
        
        last_raw = raw_response
        industry, profile = extract_clean_response(raw_response)
        print(f"   → {industry or '❌ Not Found'}")
        
        # 🔥 CHANGED: Include ID in response data
        response_data = {
            "ID": company_id,  # 🔥 NEW: ID column
            "Executive": exec_name,
            "Company Name": company,
            "URL": url,
            "Industry": industry,
            "Profile": profile,
            "Date": date
        }
        response_list.append(response_data)
        all_executive_responses.append(response_data)
    
    pd.DataFrame(response_list).to_excel(OUTPUT_PATH, index=False)
    print(f"✅ {exec_name} COMPLETE: {OUTPUT_PATH}")

# ====== FINAL CLEANUP ======
print(f"\n{'='*60}")
print("🔗 COMBINING ALL EXECUTIVE DATA...")
print(f"{'='*60}")

if all_executive_responses:
    combined_df = pd.DataFrame(all_executive_responses)
    combined_filename = f"{OUTPUT_BASE_PATH}\\combined_executive_data_{date}.xlsx"
    combined_df.to_excel(combined_filename, index=False)
    
    print(f"🎉 COMBINED FILE SAVED: {combined_filename}")
    print(f"📊 Total records: {len(combined_df)}")
    
    exec_summary = combined_df.groupby('Executive').agg({
        'ID': 'count',  # 🔥 CHANGED: Use ID count
        'Industry': lambda x: (x != '').sum()
    }).rename(columns={'ID': 'Total Companies', 'Industry': 'Matched Industries'})
    print("\n📈 Executive Summary:")
    print(exec_summary)

print("\n🎉 FULLY AUTOMATED PROCESS COMPLETE WITH SINGLE DRIVER! 🚀")
print("📁 All files saved in:", OUTPUT_BASE_PATH)

# Clean shutdown
# driver.quit()
# print("✅ WebDriver closed successfully!")

# 🔥 CRITICAL: ALLOW SLEEP AGAIN BEFORE EXIT
allow_sleep()  # ✅ RESTORE NORMAL SLEEP BEHAVIOR
print("🎬 Script fully completed - laptop can now sleep normally!")
