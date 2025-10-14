from .query_runner import run_query


def demo_top_hitters():
    sql = """
        SELECT Name, Statistic, Team, StatValue
        FROM hitter_stats
        WHERE Statistic = 'Batting Average'
        ORDER BY StatValue DESC
        LIMIT 10
    """
    columns, results = run_query(sql)
    print("Top Hitters by Batting Average")
    print(" | ".join(columns))
    for row in results:
        print(" | ".join(str(cell) for cell in row))


def demo_pitcher_team_review():

    sql = """
        SELECT p.Name, p.Statistic, p.Team, p.StatValue, r.title, r.subtitle
        FROM pitcher_stats p
        JOIN team_review_pitcher r
        ON p.Team = r.Team AND p.year = r.year
        WHERE p.Statistic = 'Complete Games'
        ORDER BY p.StatValue DESC
        LIMIT 10
    """
    columns, results = run_query(sql)
    print("Pitchers with Complete Games and Team Review")
    print(" | ".join(columns))
    for row in results:
        print(" | ".join(str(cell) for cell in row))


def demo_intro_by_year(target_year="1882"):

    sql = """
        SELECT type, title, paragraph
        FROM intro_content
        WHERE year = ?
        ORDER BY type, h2_index, para_index
    """
    columns, results = run_query(sql, [target_year])
    print(f"Intro Content for Year {target_year}")
    print(" | ".join(columns))
    for row in results:
        print(" | ".join(str(cell) for cell in row))


def demo_metadata_summary():

    sql = """
        SELECT league, year, title, quote
        FROM season_metadata
        ORDER BY league, year DESC
        LIMIT 10
    """
    columns, results = run_query(sql)
    print("Season Metadata Summary")
    print(" | ".join(columns))
    for row in results:
        print(" | ".join(str(cell) for cell in row))
