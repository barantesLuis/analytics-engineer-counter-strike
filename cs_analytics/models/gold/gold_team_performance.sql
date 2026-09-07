WITH team_matches AS (

    SELECT
        match_id,
        match_date,
        event_name,
        team1_id AS team_id,
        team1_name AS team_name,
        team1_match_score AS maps_won,
        team2_match_score AS maps_lost,
        teams1_hltv_rank_match_date AS hltv_rank,
        CASE
            WHEN match_winner_name = team1_name THEN 1
            ELSE 0
        END AS match_win
    FROM {{ ref('sl_matches') }}

    UNION ALL

    SELECT
        match_id,
        match_date,
        event_name,
        team2_id AS team_id,
        team2_name AS team_name,
        team2_match_score AS maps_won,
        team1_match_score AS maps_lost,
        teams2_hltv_rank_match_date AS hltv_rank,
        CASE
            WHEN match_winner_name = team2_name THEN 1
            ELSE 0
        END AS match_win
    FROM {{ ref('sl_matches') }}
),

team_performance AS (

    SELECT
        team_id,
        team_name,
        COUNT(*) AS matches_played,
        SUM(match_win) AS matches_won,
        COUNT(*) - SUM(match_win) AS matches_lost,
        SUM(maps_won) AS maps_won,
        SUM(maps_lost) AS maps_lost,
        ROUND(
            100.0 * SUM(match_win) / COUNT(*),
            2
        ) AS win_rate,
        ROUND(AVG(hltv_rank), 2) AS avg_hltv_rank
    FROM team_matches
    GROUP BY
        team_id,
        team_name
)

SELECT *
FROM team_performance