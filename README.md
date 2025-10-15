# Baseball Scraper & CLI Analysis Tool

This project scrapes historical baseball data from league pages, stores it in structured CSV and JSON formats, and provides a command-line interface (CLI) for querying and analyzing the data via SQLite.

It's built for people who like their baseball stats clean, queryable, and not buried in HTML spaghetti.

[Demo Link: Baseball Stats Dashboard](https://baseball-kj3k.onrender.com/) You might have to wait upto 1 minute for the server to start.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/amirdaniali/baseball-scraper.git
cd baseball-scraper
```

### 2. Install Dependencies and Create Virtual Environment

```bash
uv venv .venv
.venv/Scripts/activate
uv pip install -r requirements.txt
```


### 3. Run Scraper

```bash
python scraper.py
```

Once the data is downloaded into json formats the program will be able to generate csv files from the saved data. So if you accidently delete the csv files you can just run the scraper again and it will create the csv files very fast.

## CLI usage

Once the scraper module finishes storing data you are free to either play around with the cli query module or use the visualisation dashboard directly.

To Run the cli:
```bash
python cli.py <command> [options]

python cli.py import --all

python cli.py import data/csv/hitter_stats.csv hitter_stats
```

The cli works by either supplying it with a sql file or giving it a query directly. Querying with a string doesn't work very well because alot of column names have white space in them and managing the whitespace within a string within your shell environemnt is painful.

To write your own queries place your query script in the `./queries` directory and run it like the queries below.


```bash
python cli.py query --file ./queries/top_hitters.sql

# Most complete games
python cli.py query --file ./queries/top_complete_games.sql

# Intro content for 1882
python cli.py query --file queries/intro_1882.sql
```bash


```bash
# Run SQL from file: Standings by division
python cli.py query --file queries/standings_east.sql

# Run SQL from file: Other stats with winning percentage
python cli.py query --file queries/other_stats_wp.sql
```

```bash

# Run SQL from file: Join pitcher stats with team review
python cli.py query --file queries/join_pitcher_review.sql
```


```bash
# Run SQL from file: Standings queries
python cli.py query --file queries/team_standings_wins.sql
python cli.py query --file queries/team_standings_losses.sql
```


### Debugging
```bash
python cli.py query "PRAGMA table_info(hitter_stats)"
python cli.py query "SELECT COUNT(*) FROM pitcher_stats"
python cli.py query "SELECT DISTINCT year FROM team_standings"
```

## Dashboard and visualisations

Once the data is downloaded you can run the following console command to start the Flask server on localhost:8050

```bash
python ./run_dashbpard.py
```

## Technologies

- Python
- Selenium
- SQLite
- CSV/JSON
- Plotly
- Dash

## Thanks

Special thanks to Code the Dream, Eric Thomson, Sushmitha Sai Niharika Matcha, and Josh Sternfeld.

[Baseball Alamnac](https://www.baseball-almanac.com/)

## Legal

[Baseball alamnac robots.txt](https://www.baseball-almanac.com/robots.txt)


## Architecture Overview

The project is organized into 6 main directories:

### `scraping/`:

Contains all logic for extracting data from the web using Selenium. It parses HTML tables, normalizes headers, and handles quirks like division banners and malformed rows. 

The `scraper.py` script is responsible for collecting baseball data from external source (https://www.baseball-almanac.com/), transforming it into structured formats, and saving it locally for analysis.

The main logic of scraping comes from the `scrape_all.py` file which calls the `driver_setup.py` module, then calls the `scrape_links` module to get the latest page links from the website and finally for any league-year pair whose local data doesn't exist, it calls the `scrape_year.py` file to scrape the final details.

Some noteworthy considerations of the code in this phase are the following:

- The data within the baseball alamnac website is very messy. Many column names are abbreviated. Many column names exist in multiple shapes such as `Team(s)`, `Team [Click for roster]`, `Team | Roster` , `Team | Roster]`, `TEAM` all refering to the `Team` column name. As such we need to have a dictionary to translate the representation of data in the website into predictable formats for our usage. Check `header_map.py` file for more of these time consuming examples. Each entry coresponds with me running the scraping logic once, waiting an hour for the scraping to finish, seeing the erros, correcting the code, and running again. 
- Each page of the website has an intro section with some `h1` and `h2` tags, a quote section and some data table sections. Each table has its own potentially different convoluted mess of a html with a typical xpath looking like this: `/html/body/div[2]/div[2]/div[4]/table/tbody/tr[10]/td[5]/a` for just one element. These elements sometimes exist and sometimes don't because a previous row has a class tag like this: `<td rowspan="2" class="datacolBlue middle"><a href="../pitching/piwins4.shtml" title="YEAR BY YEAR LEADERS FOR WINS">Wins</a></td>` Thats right. the html has a cell that has an attribute that changes whether or not a cell in an upcoming row will be present or not. I went through countless time-consuming iterations on these parsing logics and I don't wish them on my worst enemy.
- After parsing the data we store the page data into many dictionaries and pass them to the `storage/save_load.py` module to save to disk.

### `storage/`:

Responsible for exporting scraped data into structured CSV and JSON files. It also handles header normalization and ensures consistent formatting across seasons and leagues. There are two main files here. `save_load.py` handles working with json cache in our file system to avoid redownloading the data. The other file is `exort_csv.py` which handles exporting the data to the csv format once scraping is finished.


### `analysis/`: 

Imports CSVs into a SQLite database and provides a CLI for running queries. It includes schema inference, table creation, and flexible querying. It also contains the pandas dataframes files used for furthur analysis. These pandas dataframes are loaded by the `visualisation/data_loader` module later to produce a nice looking dashboard.



### `data/`:

All output files live in the `/data` directory. 

`/data/csv/` : CSV exports
`/data/json/<LeagueName>/<Year>.json` : JSON files per league/year
`/data/season_data.db` : SQLite database


### `queries/`:

This directory is meant to contain the user generated query scripts used with the cli tool to analyse and work with the data.

### `visualisation/`:

This directory is responsible for loading, processing and visualising the insights gained from the analysis phase in a beautiful and interactive Dash frontend. `app.py` is the main driver of the logic. `callbnacks.py` is the data controller. `data_loader.py` handles loading the data from various modules in the analysis phase and `layout.py` handles displaying all results in the frontend.  