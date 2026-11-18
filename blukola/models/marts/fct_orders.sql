with

orders as (

    select * from {{ ref('stg_orders') }}
),

customers as (

    select
        customer_id,
        customer_name
    from {{ ref('stg_customers') }}

),

order_items as (

    SELECT
        order_item_id,
        order_id,
        quantity,
        unit_price,
        quantity * unit_price as item_total
    from {{ ref('stg_order_items') }}

),

payment_summary as (

    select
        order_id,
        sum(case
            when payment_status = 'success' then amount
            else 0
        end) as total_successful_payments
    from {{ ref('stg_payments') }}
    group by 1

),

order_items_summary as (

    select
        o.order_id,
        c.customer_name,
        o.order_status,
        o.ordered_at as order_date,
        COALESCE(COUNT(distinct oi.order_item_id), 0) as order_item_lines,
        ROUND(COALESCE(SUM(oi.item_total), 0), 2) as order_items_subtotal,
        COALESCE(SUM(oi.quantity), 0) AS total_quantity
    from orders o
    LEFT JOIN order_items oi
        on o.order_id = oi.order_id
    LEFT JOIN customers c
        on o.customer_id = c.customer_id
    group by 1, 2, 3, 4

)

select
    ois.*,
    COALESCE(ps.total_successful_payments, 0) as total_successful_payments,
    ROUND(
        ois.order_items_subtotal - COALESCE(ps.total_successful_payments, 0),
        2
    ) AS outstanding_amount,
    CASE
        WHEN
            COALESCE(ps.total_successful_payments, 0) > ois.order_items_subtotal
            THEN 'overpaid'

        WHEN COALESCE(ps.total_successful_payments, 0) = 0
            THEN 'unpaid'

        WHEN
            (COALESCE(ps.total_successful_payments, 0) = ois.order_items_subtotal)
            THEN 'fully_paid'

        ELSE 'partially_paid'
    END AS payment_status
from order_items_summary ois
left join payment_summary ps
    on ois.order_id = ps.order_id
