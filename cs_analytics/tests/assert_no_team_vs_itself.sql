SELECT
    match_id,
    team1_id,
    team1_name,
    team2_id,
    team2_name
FROM {{ ref('sl_matches') }}
WHERE team1_id = team2_id