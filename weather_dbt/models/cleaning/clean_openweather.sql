SELECT 
    id,
    LOWER(city) AS city,
    LOWER(country) AS country,
    latitude,
    longitude,
    ROUND(temperature, 2) AS temperature,
    ROUND(feels_like, 2) AS feels_like,
    humidity,
    pressure,
    ROUND(wind_speed, 2) AS wind_speed,
    wind_direction,
    cloud_coverage,
    LOWER(weather_main) AS weather_main,
    LOWER(weather_description) AS weather_description,
    to_timestamp(event_time) AS event_time,
    ingested_time,

    (city IS NOT NULL
    AND country IS NOT NULL
    AND latitude IS NOT NULL
    AND longitude IS NOT NULL) AS valid_location,

    (temperature > -100 
    AND temperature < 100 
    AND feels_like > -100 
    AND feels_like < 100 
    AND humidity >= 0 
    AND humidity <= 100) AS valid_weather,

    (wind_speed >= 0 
    AND wind_direction >= 0 
    AND wind_direction <= 360) AS valid_wind,

    (pressure > 0 
    AND pressure < 2000) AS valid_pressure,

    (cloud_coverage >= 0 
    AND cloud_coverage <= 100) AS valid_clouds

FROM {{ ref('staging_openweather') }}
