WITH raw_data AS (
    SELECT * FROM {{ source('raw', 'telegram_messages') }}
)
SELECT
    CAST(message_id AS INT) as message_id,
    TRIM(REPLACE(channel_name, '@', '')) as channel_name,
    CAST(message_date AS TIMESTAMP) as message_date,
    COALESCE(message_text, '') as message_text,
    has_media::BOOLEAN as has_image,
    CAST(views AS INT) as view_count,
    CAST(forwards AS INT) as forward_count,
    LENGTH(COALESCE(message_text, '')) as message_length
FROM raw_data
WHERE message_id IS NOT NULL