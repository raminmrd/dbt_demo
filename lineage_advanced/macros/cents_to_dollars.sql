{% macro cents_to_dollars(column_name, decimal_places=2) %}
    -- MACRO: Format currency values
    round({{ column_name }}, {{ decimal_places }})
{% endmacro %}

