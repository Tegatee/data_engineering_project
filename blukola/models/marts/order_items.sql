select
    i.order_item_id,
    i.order_id,
    o.customer_id,
    i.product_id,
    o.ordered_at::date as order_date,
    o.order_status,
    i.quantity,
    i.unit_price
from {{ ref('stg_order_items') }} i
join {{ ref('stg_orders') }} o 
    on i.order_id = o.order_id
