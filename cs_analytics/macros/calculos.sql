{% macro calculate_kd(kills, deaths) %}

    {{ kills }} / NULLIF({{ deaths }}, 0)

{% endmacro %}