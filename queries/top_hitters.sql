SELECT Name, Statistic, Team, "Statistic Value"
FROM hitter_stats
WHERE Statistic = 'Batting Average'
ORDER BY "Statistic Value" DESC
LIMIT 10;
