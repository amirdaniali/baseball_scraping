# Baseball Scraper & CLI Analysis Tool

This project scrapes historical baseball data from league pages, stores it in structured CSV and JSON formats, and provides a command-line interface (CLI) for querying and analyzing the data via SQLite.

It's built for people who like their baseball stats clean, queryable, and not buried in HTML spaghetti.

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

All output files live in the `/data` directory:

`/data/csv/` : CSV exports
`/data/json/<LeagueName>/` : JSON files per league/year
`/data/season_data.db` : SQLite database


### 4. CLI usage

Run the cli:
```bash
python cli.py <command> [options]
```

some commands that are available are:

#### Import CSVs into SQLite

```bash
# Import all CSVs
python cli.py import --all

# Import a single CSV
python cli.py import data/csv/hitter_stats.csv hitter_stats
```

#### CLI Usage


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


#### Debugging
```bash
python cli.py query "PRAGMA table_info(hitter_stats)"
python cli.py query "SELECT COUNT(*) FROM pitcher_stats"
python cli.py query "SELECT DISTINCT year FROM team_standings"
```


## Technologies

- Python
- Selenium
- SQLite
- CSV/JSON


## Thanks

Special thanks to Code the Dream, Eric Thomson, Sushmitha Sai Niharika Matcha, and Josh Sternfeld.



## Architecture Overview

The project is organized into three main modules:

`scraping/`: Contains all logic for extracting data from the web using Selenium. It parses HTML tables, normalizes headers, and handles quirks like division banners and malformed rows. 

`storage/`: Responsible for exporting scraped data into structured CSV and JSON files. It also handles header normalization and ensures consistent formatting across seasons and leagues.

`analysis/`: Imports CSVs into a SQLite database and provides a CLI for running queries. It includes schema inference, table creation, and flexible querying. 

All output files live in the `/data` directory:



The `scraper.py` script is responsible for collecting baseball data from external source (https://www.baseball-almanac.com/), transforming it into structured formats, and saving it locally for analysis.