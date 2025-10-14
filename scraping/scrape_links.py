from typing import Dict, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def get_league_year_links(driver: webdriver) -> Dict[str, List[Dict]]:
    """
    Returns a dictionary where keys are league names and values are lists of dicts with year and URL.
    Only the first banner per league is used to extract metadata; the second is skipped.
    """
    driver.get("https://www.baseball-almanac.com/yearmenu.shtml")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.boxed"))
    )

    league_data: Dict[str:Dict] = {}
    league_table = driver.find_element(By.CSS_SELECTOR, "table.boxed > tbody")
    league_sections = league_table.find_elements(By.CSS_SELECTOR, "tr")

    current_league = None
    banner_count = 0

    for section in league_sections:
        td = section.find_element(By.TAG_NAME, "td")
        td_class = td.get_attribute("class")

        if td_class == "header":
            continue  # Skip logo/header rows

        elif td_class == "banner":
            banner_count += 1
            if banner_count % 2 == 1:  # Only process the first banner of each league
                text = td.text.strip()
                # Example: "The History of the American League From 1901 to 2025"

                if "From" in text and "to" in text:
                    parts = text.split("The History of the")[-1].split(
                        " From "
                    )  # "American League"," 1901 to 2025"
                    league_name = parts[0].strip()
                    year_range = parts[1].split(" to ")
                    current_league = league_name
                    league_data[current_league] = []
            else:
                continue  # Skip second banner

        elif td_class == "datacolBox" and current_league:
            # Find the nested table containing year links
            try:
                sub_table = td.find_element(By.CSS_SELECTOR, "table.ba-sub > tbody")
                year_rows = sub_table.find_elements(By.TAG_NAME, "tr")

                for row in year_rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    for cell in cells:
                        cell_class = cell.get_attribute("class") or ""
                        if "datacolBox" in cell_class:
                            links = cell.find_elements(By.TAG_NAME, "a")
                            for link in links:
                                year_text = link.text.strip()
                                year_url = link.get_attribute("href")
                                if year_text and year_url:
                                    league_data[current_league].append(
                                        {"year": year_text, "url": year_url}
                                    )
                                    print(
                                        f"succesfully loaded {current_league} year: {year_text} url into memory                         ",
                                        end="\r",
                                    )
            except Exception as e:
                print(f"Error parsing datacolBox for {current_league}: {e}")

    return league_data
