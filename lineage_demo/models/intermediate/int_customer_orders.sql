-- Intermediate layer: Aggregate customer order metrics
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_metrics as (
    select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customers.email,
        customers.signup_date,
        count(orders.order_id) as total_orders,
        sum(case when orders.status = 'completed' then orders.amount else 0 end) as total_revenue,
        min(orders.order_date) as first_order_date,
        max(orders.order_date) as last_order_date
    from customers
    left join orders on customers.customer_id = orders.customer_id
    group by 1, 2, 3, 4, 5
)

select * from customer_metrics

