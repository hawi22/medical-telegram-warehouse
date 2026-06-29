
  create view "medical_warehouse"."public_staging"."stg_yolo_detections__dbt_tmp"
    
    
  as (
    WITH raw_yolo AS (
    SELECT * FROM "medical_warehouse"."raw"."yolo_detections"
)
SELECT
    CAST(message_id AS INT) as message_id,
    TRIM(REPLACE(channel_name, '@', '')) as channel_name,
    detected_objects,
    image_category
FROM raw_yolo
  );