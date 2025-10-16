-- Staging layer: Clean and standardize raw customer data
with source as (
    select * from {{ ref('raw_customers') }}
),

cleaned as (
    select
        customer_id,
        first_name,
        last_name,
        email,
        signup_date::date as signup_date
    from source
)

select * from cleaned

