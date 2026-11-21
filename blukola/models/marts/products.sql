with

products as (

    select
        product_id,
        product_name,
        category,
        product_price
    from {{ ref('stg_products') }}

)

select * from products
