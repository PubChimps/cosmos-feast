{{ config(materialized='table') }}

select
    i.event_timestamp,
    i.driver_id,
    conv_rate,
    conv_rate_max_diff,
    acc_rate,
    acc_rate_max_diff,
    avg_daily_trips,
    created
from {{ ref('conv_rate') }} i
join {{ ref('acc_rate') }} j
    on (i.driver_id=j.driver_id) and (i.event_timestamp=j.event_timestamp)
