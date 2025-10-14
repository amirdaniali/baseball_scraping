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
python cli.py import path table_name # import one csv file
python cli.py import --all
```


#### Run Custom Queries

```bash
python cli.py query "SELECT Name, Statistic, Team FROM hitter_stats WHERE Statistic = 'Batting Average' ORDER BY StatValue DESC LIMIT 10"
python cli.py query "SELECT Name, Statistic, Team FROM pitcher_stats WHERE Statistic = 'Complete Games' ORDER BY StatValue DESC LIMIT 10"
python cli.py query "SELECT title, paragraph FROM intro_content WHERE year = '1882'"
python cli.py query "SELECT Team, division, Payroll FROM team_standings WHERE division = 'East'"
python cli.py query "SELECT Team, Winning Percentage FROM other_stats ORDER BY Winning Percentage DESC"
python cli.py query "SELECT h.year, h.Name, h.Team, h.Statistic, r.title FROM hitter_stats h JOIN team_review_hitter r ON h.Team = r.Team AND h.year = r.year WHERE h.Statistic = 'Batting Average' ORDER BY h.StatValue DESC LIMIT 10"
python cli.py query "SELECT p.Name, p.Statistic, p.Team, r.subtitle FROM pitcher_stats p JOIN team_review_pitcher r ON p.Team = r.Team AND p.year = r.year WHERE p.Statistic = 'Complete Games' ORDER BY p.StatValue DESC"
python cli.py query "PRAGMA table_info(hitter_stats)"
python cli.py query "SELECT COUNT(*) FROM pitcher_stats"
python cli.py query "SELECT DISTINCT year FROM team_standings"
python cli.py query "SELECT * FROM other_stats WHERE guesses = '1'"
python cli.py query "SELECT Name, Statistic, Team FROM hitter_stats WHERE Statistic = 'Base on Balls' ORDER BY StatValue DESC LIMIT 10"
python cli.py query "SELECT Name, Statistic, Team FROM hitter_stats WHERE Statistic = 'Home Runs' ORDER BY StatValue DESC LIMIT 10"
python cli.py query "SELECT Team, Statistic, Total Hits FROM team_review_hitter WHERE Statistic = 'Hits' ORDER BY Total Hits DESC"
python cli.py query "SELECT Team, Statistic, Total Runs FROM team_review_hitter WHERE Statistic = 'Runs' ORDER BY Total Runs DESC"
python cli.py query "SELECT Team, Total Wins, division FROM team_standings ORDER BY Total Wins DESC"
python cli.py query "SELECT Team, Total Loses, division FROM team_standings ORDER BY Total Loses DESC"


```


#### Run Demo Queries

```bash

python cli.py demo top_hitters
python cli.py demo pitcher_review
python cli.py demo intro_year --year 1882
python cli.py demo metadata
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

`/data/csv/` : CSV exports
`/data/json/<LeagueName>/` : JSON files per league/year
`/data/sqlite.db` : SQLite database
