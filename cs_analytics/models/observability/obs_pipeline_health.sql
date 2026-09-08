WITH pipeline_metrics AS (

    SELECT
        'matches' AS dataset,
        COUNT(*) AS row_count,
        MAX(match_date) AS latest_date
    FROM {{ ref('sl_matches') }}

    UNION ALL

    SELECT
        'rankings' AS dataset,
        COUNT(*) AS row_count,
        MAX(ranking_date) AS latest_date
    FROM {{ ref('sl_rankings') }}

    UNION ALL

    SELECT
        'player_stats' AS dataset,
        COUNT(*) AS row_count,
        MAX(api_consulted_date) AS latest_date
    FROM {{ ref('sl_player_stats') }}

),

health AS (

    SELECT
        dataset,
        row_count,
        latest_date,
        CURRENT_DATE AS check_date,

        DATE_DIFF(
            'day',
            latest_date,
            CURRENT_DATE
        ) AS days_since_update

    FROM pipeline_metrics

)

SELECT
    dataset,
    row_count,
    latest_date,
    check_date,
    days_since_update,

    CASE
        WHEN row_count = 0
            THEN 'CRITICAL'

        WHEN days_since_update <= 1
            THEN 'HEALTHY'

        WHEN days_since_update <= 7
            THEN 'WARNING'

        ELSE 'CRITICAL'

    END AS pipeline_status

FROM health