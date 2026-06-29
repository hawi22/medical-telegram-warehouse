
  
    

  create  table "medical_warehouse"."public_marts"."fct_image_detections__dbt_tmp"
  
  
    as
  
  (
    SELECT
    m.message_pk,
    m.channel_fk,
    m.date_fk,
    y.image_category,
    y.detected_objects,
    m.view_count
FROM "medical_warehouse"."public_marts"."fct_messages" m
INNER JOIN "medical_warehouse"."public_staging"."stg_yolo_detections" y 
    ON m.message_id = y.message_id 
    AND m.channel_name = y.channel_name
  );
  