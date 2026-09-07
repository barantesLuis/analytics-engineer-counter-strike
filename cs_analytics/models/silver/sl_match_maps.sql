SELECT
    m.id AS match_id,
    map.id AS map_id,
    map.name AS map_name,
    map.team1_score,
    map.team2_score

FROM {{ ref('br_matches') }} AS m

CROSS JOIN UNNEST(m.maps) AS u(map)