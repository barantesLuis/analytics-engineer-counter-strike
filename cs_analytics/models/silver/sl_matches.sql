SELECT
date AS match_date,
event AS event_name,
id AS match_id,
team1.id AS team1_id,
team1.name AS team1_name,
team1.score AS team1_match_score,
team1.rank AS teams1_hltv_rank_match_date,
team2.id AS team2_id,
team2.name AS team2_name,
team2.score AS team2_match_score,
team2.rank AS teams2_hltv_rank_match_date,
winner.name AS match_winner_name,
best_of
FROM {{ ref('br_matches') }}
