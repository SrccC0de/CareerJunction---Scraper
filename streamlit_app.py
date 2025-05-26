import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_jobs(search_term):
    # Setup headless Selenium for Streamlit
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.careerjunction.co.za")
    time.sleep(5)

    search_input = driver.find_element(By.ID, "Keywords")
    search_input.clear()
    search_input.send_keys(search_term)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)

    jobs = []

    while True:
        time.sleep(5)
        job_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'module-content')]")
        for card in job_cards:
            try:
                title = card.find_element(By.XPATH, ".//div[@class='job-result-title']/h2/a").text.strip()
            except:
                title = "N/A"

            try:
                recruiter = card.find_element(By.XPATH, ".//div[@class='job-result-title']/h3/a").text.strip()
            except:
                recruiter = "N/A"

            try:
                salary = card.find_element(By.XPATH, ".//ul[@class='job-overview']/li[contains(@class, 'salary')]").text.strip()
            except:
                salary = "N/A"

            try:
                position = card.find_element(By.XPATH, ".//ul[@class='job-overview']/li[contains(@class, 'position')]").text.strip()
            except:
                position = "N/A"

            try:
                location = card.find_element(By.XPATH, ".//ul[@class='job-overview']/li[contains(@class, 'location')]/a").text.strip()
            except:
                location = "N/A"

            try:
                date_posted = card.find_element(By.XPATH, ".//ul[@class='job-overview']/li[contains(@class, 'updated-time')]").text.strip()
            except:
                date_posted = "N/A"

            if title != "N/A":
                jobs.append({
                    "Title": title,
                    "Recruiter": recruiter,
                    "Salary": salary,
                    "Position": position,
                    "Location": location,
                    "Date Posted": date_posted
                })

        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'next')]")
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
        except:
            break

    driver.quit()
    return pd.DataFrame(jobs)

# Streamlit UI
st.title("CareerJunction Job Scraper")
job_title = st.text_input("Enter a job title", "")

if st.button("Search Jobs") and job_title:
    with st.spinner("Scraping job listings..."):
        df = scrape_jobs(job_title)
        if not df.empty:
            st.success(f"Found {len(df)} jobs for '{job_title}'")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, file_name=f"{job_title.lower().replace(' ', '-')}-jobs.csv")
        else:
            st.warning("No jobs found.")
