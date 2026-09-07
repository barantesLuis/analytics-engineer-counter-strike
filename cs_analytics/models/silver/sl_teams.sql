SELECT
    id AS team_id,
    name AS team_name
FROM {{ ref('br_teams') }}