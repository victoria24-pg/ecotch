/* Requerimiento 1 */

SELECT UPPER(e.emp_nombre) AS EMPRENDIMIENTO,
       INITCAP(e.emp_rubro) AS RUBRO,
       LOWER('@' || SUBSTR(e.emp_instagram, INSTR(e.emp_instagram, '/', -1) + 1)) AS INSTAGRAM,
       LPAD(SUBSTR(e.emp_contacto, -4), LENGTH(e.emp_contacto), '*') AS CONTACTO,
       c.cna_nombre AS COMUNA
FROM   emprendimiento e
JOIN   comuna c ON e.cna_id = c.cna_id
WHERE  e.emp_created_at BETWEEN TO_DATE('01/04/2026', 'DD/MM/YYYY') 
                            AND TO_DATE('31/08/2026 23:59:59', 'DD/MM/YYYY HH24:MI:SS')
  AND  e.emp_instagram IS NOT NULL
ORDER BY c.cna_nombre ASC,
         UPPER(e.emp_nombre) ASC;

/*Requerimiento 2 */

SELECT d.deb_titulo AS TITULO,
       c.cat_nombre AS CATEGORIA,
       TO_CHAR(d.deb_created_at, 'DD/MM/YYYY HH24:MI') AS INICIO,
       TO_CHAR(d.deb_fecha_cierre, 'DD-MON-YYYY', 'NLS_DATE_LANGUAGE=SPANISH') AS CIERRE,
       'T' || TO_CHAR(d.deb_fecha_cierre, 'Q-YYYY') AS TRIMESTRE_CIERRE,
       TRUNC(d.deb_fecha_cierre - d.deb_created_at) AS DIAS_ABIERTO,
       ROUND((d.deb_fecha_cierre - d.deb_created_at) / 7, 1) AS SEMANAS_ABIERTO,
       TO_CHAR(LAST_DAY(d.deb_fecha_cierre), 'DD/MM/YYYY') AS PLAZO_RESULTADO
FROM   debate d
JOIN   categoria c ON d.cat_id = c.cat_id
WHERE  d.deb_cerrado = 1
ORDER BY DIAS_ABIERTO DESC;


/* Requerimiento 3 */

SELECT e.enc_pregunta AS ENCUESTA,
       NVL2(u.usu_id, INITCAP(u.usu_nombre || ' ' || u.usu_apellido), 'SIN AUTOR') AS CREADOR,
       TO_CHAR(e.enc_created_at, 'DD/MM/YYYY') AS FECHA_PUBLICACION,
       COUNT(DISTINCT o.oen_id) AS TOTAL_OPCIONES,
       COUNT(DISTINCT v.ven_id) AS TOTAL_VOTOS,
       TO_CHAR(NVL(COUNT(DISTINCT v.ven_id) / NULLIF(COUNT(DISTINCT o.oen_id), 0), 0), '990.00') AS VOTOS_POR_OPCION,
       NVL(TO_CHAR(MAX(v.ven_created_at), 'DD/MM/YYYY HH24:MI'), 'SIN VOTOS') AS ULTIMO_VOTO
FROM   encuesta e
LEFT JOIN usuario u ON e.usu_id = u.usu_id
LEFT JOIN opcion_encuesta o ON e.enc_id = o.enc_id
LEFT JOIN voto_encuesta v ON o.oen_id = v.oen_id
WHERE  e.enc_eliminada_at IS NULL
GROUP BY e.enc_id,
         e.enc_pregunta,
         u.usu_id,
         u.usu_nombre,
         u.usu_apellido,
         e.enc_created_at
HAVING COUNT(DISTINCT o.oen_id) >= 2
ORDER BY TOTAL_VOTOS DESC;

/*Requetimiento 4 */

SELECT c.cat_nombre AS CATEGORIA,
       COUNT(d.deb_id) AS TOTAL_DEBATES,
       COUNT(CASE WHEN d.deb_cerrado = 1 THEN 1 END) AS DEBATES_CERRADOS,
       COUNT(CASE WHEN d.deb_local = 1 THEN 1 END) AS DEBATES_LOCALES,
       NVL(ROUND(AVG(d.deb_fecha_cierre - d.deb_created_at), 1), 0) AS PROMEDIO_DIAS_CIERRE
FROM   categoria c
JOIN   debate d ON c.cat_id = d.cat_id
WHERE  d.deb_created_at BETWEEN TO_DATE('01/01/2026', 'DD/MM/YYYY') 
                            AND TO_DATE('31/12/2026 23:59:59', 'DD/MM/YYYY HH24:MI:SS')
GROUP BY c.cat_id,
         c.cat_nombre
HAVING COUNT(d.deb_id) > (
    SELECT AVG(cant_debates)
    FROM (
        SELECT COUNT(*) AS cant_debates
        FROM   debate
        WHERE  deb_created_at BETWEEN TO_DATE('01/01/2026', 'DD/MM/YYYY') 
                                  AND TO_DATE('31/12/2026 23:59:59', 'DD/MM/YYYY HH24:MI:SS')
        GROUP BY cat_id
    )
)
ORDER BY TOTAL_DEBATES DESC;


/* Requerimiento  5 */

SELECT c.cat_nombre AS CATEGORIA,
       COUNT(d.deb_id) AS TOTAL_DEBATES,
       COUNT(CASE WHEN d.deb_cerrado = 1 THEN 1 END) AS DEBATES_CERRADOS,
       COUNT(CASE WHEN d.deb_local = 1 THEN 1 END) AS DEBATES_LOCALES,
       NVL(ROUND(AVG(d.deb_fecha_cierre - d.deb_created_at), 1), 0) AS PROMEDIO_DIAS_CIERRE
FROM   categoria c
JOIN   debate d ON c.cat_id = d.cat_id
WHERE  d.deb_created_at BETWEEN TO_DATE('01/01/2026', 'DD/MM/YYYY') 
                            AND TO_DATE('31/12/2026 23:59:59', 'DD/MM/YYYY HH24:MI:SS')
GROUP BY c.cat_id,
         c.cat_nombre
HAVING COUNT(d.deb_id) > (
    SELECT AVG(cant_debates)
    FROM (
        SELECT COUNT(*) AS cant_debates
        FROM   debate
        WHERE  deb_created_at BETWEEN TO_DATE('01/01/2026', 'DD/MM/YYYY') 
                                  AND TO_DATE('31/12/2026 23:59:59', 'DD/MM/YYYY HH24:MI:SS')
        GROUP BY cat_id
    )
)
ORDER BY TOTAL_DEBATES DESC;


/*Requirimiento 5 */





