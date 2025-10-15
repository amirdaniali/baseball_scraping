SELECT p.Name, p.Statistic, p.Team, p."Statistic Value", r."Total Complete Games", r."Total Strikeouts", r."Total Wins"
FROM pitcher_stats p
JOIN team_review_pitcher r ON p.Team = r.Team AND p.year = r.year
WHERE p.Statistic = 'Complete Games'
ORDER BY p."Statistic Value" DESC;
