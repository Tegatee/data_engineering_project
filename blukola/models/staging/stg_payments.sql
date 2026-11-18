SELECT
    payment_id,
    order_id,
    lower(payment_method) as payment_method,
    amount,
    lower(status) as payment_status,
    paid_at
FROM {{ source('blukola_raw', 'payments') }}
