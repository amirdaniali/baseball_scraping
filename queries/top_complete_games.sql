SELECT Name, Statistic, Team, "Statistic Value"
FROM pitcher_stats
WHERE Statistic = 'Complete Games'
ORDER BY "Statistic Value" DESC
LIMIT 10;
