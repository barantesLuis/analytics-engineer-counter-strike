SELECT
    r.date AS ranking_date,
    ranking.id AS team_id,
    ranking.name AS team_name,
    ranking.rank AS team_rank
FROM {{ ref('br_rankings') }} AS r
CROSS JOIN UNNEST(r.rankings) AS u(ranking)