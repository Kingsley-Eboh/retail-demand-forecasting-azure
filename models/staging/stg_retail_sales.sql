with source as (

    select * from {{ source('raw', 'raw_retail_sales') }}

),

renamed as (

    select
        date as sale_date,
        store_id,
        item_id,
        cast(sales as int) as units_sold,
        cast(price as decimal(10,2)) as unit_price,
        promo as is_promo,
        weekday,
        month,
        cast(sales as int) * cast(price as decimal(10,2)) as revenue

    from source

)

select * from renamed