SELECT Name, Statistic, Team, "Statistic Value"
FROM hitter_stats
WHERE Statistic = 'Base on Balls'
ORDER BY "Statistic Value" DESC
LIMIT 10;
