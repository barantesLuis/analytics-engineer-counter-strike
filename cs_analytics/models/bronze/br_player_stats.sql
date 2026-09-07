SELECT
    *,
    '2026-09-06'::DATE AS api_consulted_date
FROM read_json_auto('../02-data/bronze/players_stats/2026-09-06.json')