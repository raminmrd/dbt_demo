-- Fact table: Customer-level metrics combining multiple sources
with customer_dim as (
    select * from {{ ref('dim_customers') }}
),

order_facts as (
    select * from {{ ref('fct_orders') }}
),

customer_enriched as (
    select
        customer_dim.customer_id,
        customer_dim.first_name || ' ' || customer_dim.last_name as full_name,
        customer_dim.customer_segment,
        customer_dim.total_revenue,
        customer_dim.total_orders,
        avg(order_facts.order_total) as avg_order_value,
        avg(order_facts.total_items) as avg_items_per_order,
        max(order_facts.order_date) as latest_order_date,
        datediff('day', max(order_facts.order_date), current_date) as days_since_last_order
    from customer_dim
    left join order_facts on customer_dim.customer_id = order_facts.customer_id
    group by 1, 2, 3, 4, 5
)

select * from customer_enriched

