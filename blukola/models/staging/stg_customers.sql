SELECT
    customer_id,
    initcap(trim(full_name)) as customer_name,
    lower(trim(email)) as email,
    initcap(trim(city)) as city,
    created_at as signed_up_at
FROM {{ source('blukola_raw', 'customers') }}