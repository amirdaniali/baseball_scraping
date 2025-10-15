from typing import Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from .header_map import HEADER_NORMALIZATION


def classify_team_review(title: str, subtitle: str) -> str | None:
    if "team review" in title.lower():
        if "hitting" in subtitle.lower():
            return "hitting"
        elif "pitching" in subtitle.lower():
            return "pitching"
    return None


def wait_for_wrapper(driver: webdriver) -> webdriver:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#wrapper"))
    )
    return driver.find_element(By.CSS_SELECTOR, "body").find_element(
        By.CSS_SELECTOR, "#wrapper"
    )


def extract_intro(wrapper) -> tuple[str, list]:
    title = ""
    intro_data = []
    containers = wrapper.find_elements(By.CSS_SELECTOR, "div.container")

    for container in containers:
        intros = container.find_elements(By.CSS_SELECTOR, "div.intro")
        for intro in intros:
            h1_elements = intro.find_elements(By.TAG_NAME, "h1")
            for h1 in h1_elements:
                clean_title = h1.text.strip()
                if clean_title.lower().startswith("year in review :"):
                    clean_title = clean_title.split(":", 1)[-1].strip()
                title = clean_title
                intro_data.append({"type": "h1", "text": clean_title})

            h2_elements = intro.find_elements(By.TAG_NAME, "h2")
            for h2 in h2_elements:
                h2_text = h2.text.strip().rstrip(". ")
                paragraphs = []
                sibling = h2
                while True:
                    try:
                        sibling = sibling.find_element(
                            By.XPATH, "following-sibling::*[1]"
                        )
                        if sibling.tag_name == "p":
                            paragraphs.append(sibling.text.strip())
                        else:
                            break
                    except:
                        break
                intro_data.append(
                    {"type": "h2", "title": h2_text, "paragraphs": paragraphs}
                )

    return title, intro_data


def extract_quote(wrapper) -> str:
    quote_divs = wrapper.find_elements(By.CSS_SELECTOR, "div.topquote")
    for quote_div in quote_divs:
        p_tags = quote_div.find_elements(By.TAG_NAME, "p")
        for p in p_tags:
            quote = p.text.strip()
            if quote:
                return quote
    return ""


def extract_tables(wrapper) -> tuple:
    containers = wrapper.find_elements(By.CSS_SELECTOR, "div.container")
    hitter_table = pitcher_table = team_standings = None
    team_review_pitcher = team_review_hitter = None
    other_tables = []
    table_index = 0

    for container in containers:
        table_divs = container.find_elements(By.CSS_SELECTOR, "div.ba-table")
        for div in table_divs:
            try:
                table = div.find_element(By.CSS_SELECTOR, "table.boxed")
                tbody = table.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")

                if not rows or len(rows) < 3:
                    continue

                try:
                    title = rows[0].find_element(By.TAG_NAME, "h2").text.strip()
                    subtitle = rows[0].find_element(By.TAG_NAME, "p").text.strip()
                except:
                    title = rows[0].text.strip()
                    subtitle = ""

                data_rows = []
                previous_row_data = {}
                rowspan_tracker = {}
                headers = []
                current_division = None

                row_index = 1
                while row_index < len(rows) - 2:
                    row = rows[row_index]
                    cells = row.find_elements(By.TAG_NAME, "td")
                    cell_classes = [cell.get_attribute("class") or "" for cell in cells]

                    # Detect banner row with division
                    if any("banner" in cls for cls in cell_classes):
                        headers = []
                        current_division = None
                        for cell in cells:
                            cls = cell.get_attribute("class") or ""
                            text = cell.text.strip()
                            if "banner middle" in cls and cell.get_attribute("rowspan"):
                                if "east" in text.lower() or "west" in text.lower():
                                    current_division = text
                                    headers.append("division")
                            elif "banner" in cls:
                                normalized = HEADER_NORMALIZATION.get(text, text)
                                headers.append(normalized)
                        row_index += 1
                        continue

                    # Parse data row
                    row_data = {}
                    cell_index = header_index = 0

                    while header_index < len(headers):
                        header = headers[header_index]

                        if header == "division" and current_division:
                            row_data["division"] = current_division
                            header_index += 1
                            continue

                        if (
                            header_index in rowspan_tracker
                            and rowspan_tracker[header_index]["remaining"] > 0
                        ):
                            row_data[header] = rowspan_tracker[header_index]["value"]
                            rowspan_tracker[header_index]["remaining"] -= 1
                            header_index += 1
                            continue

                        if cell_index >= len(cells):
                            row_data[header] = previous_row_data.get(header, "")
                            header_index += 1
                            continue

                        cell = cells[cell_index]
                        text = cell.text.strip()
                        rowspan = cell.get_attribute("rowspan")
                        if rowspan and rowspan.isdigit():
                            rowspan_tracker[header_index] = {
                                "value": text,
                                "remaining": int(rowspan) - 1,
                            }

                        row_data[header] = text
                        cell_index += 1
                        header_index += 1

                    previous_row_data = row_data.copy()
                    data_rows.append(row_data)
                    row_index += 1

                review_type = classify_team_review(title, subtitle)
                table_data = {
                    "title": title,
                    "subtitle": subtitle,
                    "headers": headers,
                    "rows": data_rows,
                }

                if review_type == "pitching":
                    team_review_pitcher = table_data
                elif review_type == "hitting":
                    team_review_hitter = table_data
                elif table_index == 0:
                    hitter_table = table_data
                elif table_index == 1:
                    pitcher_table = table_data
                elif (
                    table_index == 2
                    and "team standings" in title.lower() + subtitle.lower()
                ):
                    team_standings = table_data
                else:
                    other_tables.append(table_data)

                table_index += 1

            except Exception as e:
                print(f"Error parsing table {table_index}, {title}: {e}")
                continue

    return (
        hitter_table,
        pitcher_table,
        team_standings,
        team_review_pitcher,
        team_review_hitter,
        other_tables,
    )


def scrape_year_page(driver: webdriver, url: str) -> Dict:
    driver.get(url)
    wrapper = wait_for_wrapper(driver)

    title, intro = extract_intro(wrapper)
    quote = extract_quote(wrapper)

    (
        hitter_table,
        pitcher_table,
        team_standings,
        team_review_pitcher,
        team_review_hitter,
        other_tables,
    ) = extract_tables(wrapper)

    return {
        "title": title,
        "intro": intro,
        "quote": quote,
        "hitter_table": hitter_table,
        "pitcher_table": pitcher_table,
        "team_standings": team_standings,
        "team_review_pitcher": team_review_pitcher,
        "team_review_hitter": team_review_hitter,
        "other_tables": other_tables,
    }
