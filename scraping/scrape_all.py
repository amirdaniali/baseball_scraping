from .driver_setup import get_driver
from .scrape_links import get_league_year_links
from .scrape_year import scrape_year_page
from storage.save_load import save_year_data, is_year_saved


def scrape_all_leagues():
    driver = get_driver()
    league_years = get_league_year_links(driver)

    for league, years in league_years.items():
        for year_info in years:
            year = year_info["year"]
            url = year_info["url"]
            if is_year_saved(league, year):
                print(f"Skipping {league} {year}")
                continue

            print(f"Scraping {league} {year}...                        ", end="\r")
            # allows for the cool effect of updating lines.

            try:
                data = scrape_year_page(driver, url)
                data["league"] = league
                data["year"] = year
                save_year_data(league, year, data)
                print(f"Saved {league} {year} json data to disk.       ")
            except Exception as e:
                print(f"Error scraping {league} {year}: {e}")

    driver.quit()
    print("Finished Scraping All Data.")
