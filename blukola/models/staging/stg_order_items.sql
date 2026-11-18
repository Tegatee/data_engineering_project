SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    quantity * unit_price as total_price
FROM {{ source('blukola_raw', 'order_items') }}