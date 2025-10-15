from analysis.clean_intro_content import clean_intro_content
from analysis.clean_meta import clean_meta
from analysis.clean_hitter_stats import clean_hitter_stats
from analysis.clean_pitcher_stats import clean_pitcher_stats
from analysis.clean_team_standings import clean_team_standings


def load_all_data():
    """Load and clean all datasets"""
    return {
        "intro": clean_intro_content(),
        "meta": clean_meta(),
        "hitter": clean_hitter_stats(),
        "pitcher": clean_pitcher_stats(),
        "team": clean_team_standings(),
    }


def get_league_options(df):
    """Return unique league names"""
    return sorted(df["league"].dropna().unique())


def get_year_options(df, league):
    """Return sorted years for a given league"""
    return sorted(df[df["league"] == league]["year"].dropna().unique())
