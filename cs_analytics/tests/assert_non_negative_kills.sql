SELECT
    player_id,
    player_name,
    kills
FROM {{ ref('sl_player_stats') }}
WHERE kills < 0