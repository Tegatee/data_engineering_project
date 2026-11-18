with

customers_order as (
    select
        customer_id,
        customer_name,
        email,
        city,
        signed_up_at
    from {{ ref('stg_customers') }}

),

order_payment as (

    select
        o.customer_id,
        count(distinct o.order_id) as count_lifetime_orders,
        min(o.ordered_at) as first_order_date,
        max(o.ordered_at) as last_order_date,
        sum(case
            when p.payment_status = 'success' then p.amount
            else 0
        end) as lifetime_successful_payments,
        sum(case
            when p.payment_status = 'failed' then p.amount
            else 0
        end) as total_failed_payment_amount
    from {{ ref('stg_orders') }} o
    left join {{ ref('stg_payments') }} p
        on o.order_id = p.order_id
    group by 1

),

customer_orders_summary as (

    select
        c.customer_id,
        c.customer_name,
        c.email,
        c.city,
        c.signed_up_at,
        COALESCE(o.count_lifetime_orders, 0) AS count_lifetime_orders,
        o.first_order_date,
        o.last_order_date,
        COALESCE(o.lifetime_successful_payments, 0)
            AS lifetime_successful_payments,
        COALESCE(o.total_failed_payment_amount, 0)
            AS total_failed_payment_amount,
        case
            when COALESCE(o.count_lifetime_orders, 0) > 1 then 'returning'
            when COALESCE(o.count_lifetime_orders, 0) = 1 then 'new'
            else 'prospective'
        end as customer_type
    from customers_order c
    left join order_payment o
        on c.customer_id = o.customer_id

)

select * from customer_orders_summary
