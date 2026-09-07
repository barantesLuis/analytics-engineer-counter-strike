SELECT
    match_id,
    team1_name,
    team2_name,
    match_winner_name
FROM {{ ref('sl_matches') }}
WHERE match_winner_name NOT IN (
    team1_name,
    team2_name
)