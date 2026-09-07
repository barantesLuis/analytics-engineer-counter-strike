import duckdb

con = duckdb.connect("analytics.duckdb")

result = con.sql("""
    SELECT
        m.id AS match_id,
        map.id AS map_id,
        map.name AS map_name,
        map.team1_score,
        map.team2_score
    FROM read_json_auto('02-data/bronze/matches/2026-09-06.json') AS m
    CROSS JOIN UNNEST(m.maps) AS u(map)
    LIMIT 10
""")

print(result)

con.close()
