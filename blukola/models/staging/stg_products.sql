SELECT
    product_id,
    initcap(trim(product_name)) as product_name,
    lower(trim(category)) as category,
    unit_price as product_price
FROM {{ source('blukola_raw', 'products') }}
