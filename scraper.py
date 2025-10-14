from scraping.scrape_all import scrape_all_leagues
from storage.save_load import load_all_data
from storage.export_csv import export_to_csv

if __name__ == "__main__":
    """The entry point of the program
    First we check if we have ran any scraping before and if the json data is present in disk we don't need to run scraping anymore, saving on resources.
    Second we save all data we gatherred as csv
    Third we save all data to a sqlite database
    Forth we can analyse it with a dataframe."""
    scrape_all_leagues()
    all_data = load_all_data()
    export_to_csv(all_data)
