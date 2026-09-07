SELECT
    api_consulted_date,
    id AS player_id,
    name AS player_name,
    rank AS player_rank,
    k AS kills,
    d AS deaths,
    swing,
    adr,
    kast,
    rating,
    N AS matches_count
FROM {{ ref('br_player_stats') }}