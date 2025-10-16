-- Fact table: Order-level metrics with enriched data
with orders_with_items as (
    select * from {{ ref('int_orders_with_items') }}
),

order_aggregates as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        count(distinct product_id) as unique_products,
        sum(quantity) as total_items,
        sum(line_total) as order_total,
        count(distinct category) as unique_categories
    from orders_with_items
    group by 1, 2, 3, 4
)

select * from order_aggregates

