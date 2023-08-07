# This is an example feature definition file

from datetime import timedelta

import pandas as pd

from feast import Entity, FeatureService, FeatureView, Field, PushSource, RequestSource
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64

# Define an entity for the driver. You can think of an entity as a primary key used to
# fetch features.
driver = Entity(name="driver", join_keys=["driver_id"])

driver_stats_source = PostgreSQLSource(
    name="driver_hourly_stats_source",
    query="SELECT * FROM feast_driver_hourly_stats",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

driver_stats_push_source = PushSource(
    name="driver_stats_push_source",
    batch_source=driver_stats_source,
)
driver_stats_transform = PostgreSQLSource(
    name="driver_hourly_stats_transform",
    query="SELECT * FROM feast_driver_hourly_stats_transform",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

driver_stats_push_transform = PushSource(
    name="driver_stats_push_transform",
    batch_source=driver_stats_transform,
)

driver_stats_fresh_fv = FeatureView(
    name="driver_hourly_stats_fresh",
    entities=[driver],
    ttl=timedelta(days=1),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    online=True,
    source=driver_stats_push_source,  # Changed from above
    tags={"team": "driver_performance"},
)

driver_activity = FeatureService(
    name="driver_activity",
    features=[driver_stats_fresh_fv],
)

driver_stats_transform_fv = FeatureView(
    name="driver_hourly_stats_transform",
    entities=[driver],
    ttl=timedelta(days=1),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="conv_rate_max_diff", dtype=Float32),
        Field(name="acc_rate_max_diff", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    online=True,
    source=driver_stats_push_transform,  # Changed from above
    tags={"team": "driver_performance"},
)

driver_activity_transform = FeatureService(
    name="driver_activity_transform",
    features=[driver_stats_transform_fv],
)
