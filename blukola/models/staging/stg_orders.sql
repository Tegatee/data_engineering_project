SELECT
    order_id,
    customer_id,
    lower(trim(order_status)) as order_status,
    ordered_at 
FROM {{ source('blukola_raw', 'orders') }}