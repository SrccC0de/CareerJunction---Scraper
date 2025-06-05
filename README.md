# CareerJunction---Scraper

This project uses **Selenium** to scrape job listings from [CareerJunction](https://www.careerjunction.co.za) based on user-provided keywords.

## Features
- Automated browser control using Selenium
- Extracts job title, recruiter, salary, position type, location, and posting date
- Saves results to a structured CSV file

## Technologies
- Python
- Selenium WebDriver
- Pandas

## How to Run
1. Clone this repo.
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Make sure your ChromeDriver path is correctly set in the script.
4. Run the script:  
   `python job_scraper.py`

## Example
Search term: `"Data Analyst"`  
Output: `data-analyst-job-results.csv`

---
