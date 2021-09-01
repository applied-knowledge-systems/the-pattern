SELECT CONCAT( 
    "*3\r\n",
    '$',LENGTH(redis_cmd),'\r\n',redis_cmd,'\r\n',
    '$',LENGTH(redis_key),'\r\n',redis_key,'\r\n',
    '$',LENGTH(redis_val),'\r\n',redis_val,'\r'
) FROM (
    SELECT 'SET' as redis_cmd,
    CUI as redis_key,
    STR as redis_val
    FROM MRCONSO where LAT='ENG' AND TS='P' AND STT='PF' AND ISPREF='Y'
) AS tablez
