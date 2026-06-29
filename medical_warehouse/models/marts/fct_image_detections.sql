SELECT
    m.message_pk,
    m.channel_fk,
    m.date_fk,
    y.image_category,
    y.detected_objects,
    m.view_count
FROM {{ ref('fct_messages') }} m
INNER JOIN {{ ref('stg_yolo_detections') }} y 
    ON m.message_id = y.message_id 
    AND m.channel_name = y.channel_name