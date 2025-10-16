-- Intermediate layer: Join orders with order items and products
with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

joined as (
    select
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        orders.status,
        order_items.order_item_id,
        order_items.product_id,
        products.product_name,
        products.category,
        order_items.quantity,
        order_items.unit_price,
        order_items.quantity * order_items.unit_price as line_total
    from orders
    left join order_items on orders.order_id = order_items.order_id
    left join products on order_items.product_id = products.product_id
)

select * from joined

