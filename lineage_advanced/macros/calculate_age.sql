{% macro calculate_age(date_of_birth_column) %}
    -- MACRO: Calculate age from date of birth
    -- This is a reusable SQL function that can be called in any model
    date_diff('year', {{ date_of_birth_column }}::date, current_date)
{% endmacro %}

