WITH data_volume AS (

    SELECT
        'matches' AS dataset,
        COUNT(*) AS row_count
    FROM {{ ref('sl_matches') }}

    UNION ALL

    SELECT
        'match_maps' AS dataset,
        COUNT(*) AS row_count
    FROM {{ ref('sl_match_maps') }}

    UNION ALL

    SELECT
        'teams' AS dataset,
        COUNT(*) AS row_count
    FROM {{ ref('sl_teams') }}

    UNION ALL

    SELECT
        'players' AS dataset,
        COUNT(*) AS row_count
    FROM {{ ref('sl_player_stats') }}

    UNION ALL

    SELECT
        'rankings' AS dataset,
        COUNT(*) AS row_count
    FROM {{ ref('sl_rankings') }}

)

SELECT
    dataset,
    row_count,
    CURRENT_DATE AS check_date
FROM data_volume