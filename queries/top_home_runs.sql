SELECT Name, Statistic, Team, "Statistic Value"
FROM hitter_stats
WHERE Statistic = 'Home Runs'
ORDER BY "Statistic Value" DESC
LIMIT 10;
