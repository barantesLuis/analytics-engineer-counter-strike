SELECT
    player_id,
    player_name,
    deaths
FROM {{ ref('sl_player_stats') }}
WHERE deaths < 0