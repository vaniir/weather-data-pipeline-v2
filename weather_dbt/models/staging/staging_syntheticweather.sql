SELECT
    id,

    payload->>'name' AS city,
    payload->'sys'->>'country' AS country,

    (payload->'coord'->>'lat')::numeric AS latitude,
    (payload->'coord'->>'lon')::numeric AS longitude,

    (payload->'main'->>'temp')::numeric AS temperature,
    (payload->'main'->>'feels_like')::numeric AS feels_like,
    (payload->'main'->>'humidity')::numeric AS humidity,
    (payload->'main'->>'pressure')::integer AS pressure,

    (payload->'wind'->>'speed')::numeric AS wind_speed,
    (payload->'wind'->>'deg')::integer AS wind_direction,

    (payload->'clouds'->>'all')::integer AS cloud_coverage,

    payload->'weather'->0->>'main' AS weather_main,
    payload->'weather'->0->>'description' AS weather_description,

    (payload->>'dt')::bigint AS event_time,

    ingested_time

FROM raw_weather_data
WHERE source = 'Synthetic'