WITH freshness AS (

    SELECT
        'matches' AS dataset,
        MAX(match_date) AS latest_date
    FROM {{ ref('sl_matches') }}

    UNION ALL

    SELECT
        'rankings' AS dataset,
        MAX(ranking_date) AS latest_date
    FROM {{ ref('sl_rankings') }}

    UNION ALL

    SELECT
        'player_stats' AS dataset,
        MAX(api_consulted_date) AS latest_date
    FROM {{ ref('sl_player_stats') }}

)

SELECT
    dataset,
    latest_date,
    CURRENT_DATE AS check_date,
    DATE_DIFF('day', latest_date, CURRENT_DATE) AS days_since_update,

    CASE
        WHEN DATE_DIFF('day', latest_date, CURRENT_DATE) <= 1
            THEN 'OK'
        WHEN DATE_DIFF('day', latest_date, CURRENT_DATE) <= 7
            THEN 'WARNING'
        ELSE 'CRITICAL'
    END AS freshness_status

FROM freshness