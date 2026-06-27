SELECT
    {{ dbt_utils.generate_surrogate_key(['message_id', 'channel_name']) }} as message_pk,
    CAST(message_date AS DATE) as date_fk,
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} as channel_fk,
    message_text,
    view_count,
    forward_count,
    has_image,
    message_length
FROM {{ ref('stg_telegram_messages') }}