WITH latest_ranking_date AS (

    SELECT
        MAX(ranking_date) AS ranking_date
    FROM {{ ref('sl_rankings') }}

)

SELECT
    r.ranking_date,
    r.team_id,
    r.team_name,
    r.team_rank
FROM {{ ref('sl_rankings') }} AS r
INNER JOIN latest_ranking_date AS l
    ON r.ranking_date = l.ranking_date