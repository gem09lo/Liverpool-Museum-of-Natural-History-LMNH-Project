
--Which exhibitions receive fewer assistance requests than the average?
WITH assistance_counts AS (
    SELECT e.exhibition_name, COUNT(r.request_value) AS count_assistance
    FROM exhibition e
    JOIN request_interaction ri ON e.exhibition_id = ri.exhibition_id
    JOIN request r ON ri.request_id = r.request_id
    WHERE r.request_value = 0
    GROUP BY e.exhibition_name
),
average_assistance AS (
    SELECT AVG(count_assistance) AS avg_assistance
    FROM assistance_counts)
SELECT ac.exhibition_name
FROM assistance_counts ac
JOIN average_assistance aa ON ac.count_assistance < aa.avg_assistance;

-- Are there particular times when assistance requests/emergencies are more likely?
SELECT EXTRACT(HOUR FROM ri.event_at) AS hour_of_day, r.request_description, COUNT(ri.request_id) AS count_requests
FROM request_interaction ri
JOIN request r ON r.request_id = ri.request_id
GROUP BY hour_of_day, r.request_description
ORDER BY count_requests DESC;