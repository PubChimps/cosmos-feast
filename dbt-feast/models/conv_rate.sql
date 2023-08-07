{{ config(materialized='table') }}

select 
    event_timestamp, 
    i.driver_id, 
    conv_rate, 
    (conv_rate_max-conv_rate) as conv_rate_max_diff, 
    avg_daily_trips,
    created
from feast_driver_hourly_stats i 
join (
    select 
        driver_id, 
        max(conv_rate) as conv_rate_max 
    from feast_driver_hourly_stats 
    group by driver_id) j 
on (i.driver_id=j.driver_id) 
