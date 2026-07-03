with staged as (

    select * from {{ ref('stg_retail_sales') }}

),

aggregated as (

    select
        sale_date,
        store_id,
        item_id,
        weekday,
        month,
        sum(units_sold) as total_units_sold,
        avg(unit_price) as avg_unit_price,
        sum(revenue) as total_revenue,
        max(is_promo) as had_promo

    from staged
    group by sale_date, store_id, item_id, weekday, month

)

select * from aggregated