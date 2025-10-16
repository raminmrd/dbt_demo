-- Staging layer: Clean and standardize raw product data
with source as (
    select * from {{ ref('raw_products') }}
),

cleaned as (
    select
        product_id,
        product_name,
        category,
        price
    from source
)

select * from cleaned

