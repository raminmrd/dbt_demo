-- Staging layer: Clean and standardize raw order items data
with source as (
    select * from {{ ref('raw_order_items') }}
),

cleaned as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price
    from source
)

select * from cleaned

