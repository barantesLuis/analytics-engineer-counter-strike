SELECT
    match_id,
    map_id,
    COUNT(*) AS qtd
FROM {{ ref('sl_match_maps') }}
GROUP BY
    match_id,
    map_id
HAVING COUNT(*) > 1