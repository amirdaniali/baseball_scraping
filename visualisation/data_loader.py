import pandas as pd
from storage.save_load import CSV_DIR
from analysis.clean_intro_content import clean_intro_content
from analysis.clean_meta import clean_meta
from analysis.clean_hitter_stats import clean_hitter_stats
from analysis.clean_team_review_hitter import clean_team_review_hitter


def get_league_year_options(df):
    return [
        {
            "label": f"{row['league']} {row['year']}",
            "value": f"{row['league']}|{row['year']}",
        }
        for _, row in df[["league", "year"]].drop_duplicates().iterrows()
    ]


def load_all_data():
    return {
        "intro": clean_intro_content(),
        "meta": clean_meta(),
        "hitter": clean_hitter_stats(),
        "team": clean_team_review_hitter(),
    }
