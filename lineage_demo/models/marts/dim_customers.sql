-- Dimension table: Customer information with metrics
with customer_data as (
    select * from {{ ref('int_customer_orders') }}
),

final as (
    select
        customer_id,
        first_name,
        last_name,
        email,
        signup_date,
        total_orders,
        total_revenue,
        first_order_date,
        last_order_date,
        case
            when total_orders >= 3 then 'High Value'
            when total_orders >= 1 then 'Active'
            else 'New'
        end as customer_segment
    from customer_data
)

select * from final

