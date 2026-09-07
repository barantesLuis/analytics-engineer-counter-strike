SELECT
    api_consulted_date,
    player_id,
    player_name,
    player_rank,
    kills,
    deaths,

    ROUND(
        {{ calculate_kd('CAST(kills AS DOUBLE)', 'deaths') }},
        2
    ) AS kill_death_ratio,

    swing,
    adr,
    kast,
    rating,
    matches_count

FROM {{ ref('sl_player_stats') }}