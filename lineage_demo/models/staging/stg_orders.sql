-- Staging layer: Clean and standardize raw order data
with source as (
    select * from {{ ref('raw_orders') }}
),

cleaned as (
    select
        order_id,
        customer_id,
        order_date::date as order_date,
        status,
        amount
    from source
)

select * from cleaned

