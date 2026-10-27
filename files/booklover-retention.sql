-- BookLover retention case · diagnostic queries (PostgreSQL)
-- Training case: table and column names are assumptions for illustration.
--   users(id, created_at, channel, campaign, platform, app_version)
--   events(user_id, event_time, event_name, book_id)
--   event_name values: 'read_session', 'book_finished', 'book_started'

-------------------------------------------------------------------------------
-- 1. D30 retention by monthly cohort
--    "Active on day 30" = any reading session on days 28–30 after sign-up.
--    Agree this definition with the team before comparing numbers.
-------------------------------------------------------------------------------
WITH cohort AS (
  SELECT id AS user_id, created_at, DATE_TRUNC('month', created_at) AS cohort_month
  FROM users
  WHERE created_at < NOW() - INTERVAL '31 days'          -- only cohorts with a full 30 days
),
active_d30 AS (
  SELECT DISTINCT c.user_id
  FROM cohort c
  JOIN events e ON e.user_id = c.user_id
  WHERE e.event_name = 'read_session'
    AND e.event_time >= c.created_at + INTERVAL '28 days'
    AND e.event_time <  c.created_at + INTERVAL '31 days'
)
SELECT c.cohort_month,
       COUNT(*)                                      AS new_users,
       COUNT(a.user_id)                              AS active_d30,
       ROUND(100.0 * COUNT(a.user_id) / COUNT(*), 1) AS retention_d30
FROM cohort c
LEFT JOIN active_d30 a USING (user_id)
GROUP BY 1
ORDER BY 1;

-------------------------------------------------------------------------------
-- 2. Same, split by channel (tests hypothesis 2: acquisition quality)
--    If organic / early channels still retain ~45% and new channels are low,
--    the April drop is a mix problem. If every channel fell, look at the product.
-------------------------------------------------------------------------------
WITH cohort AS (
  SELECT id AS user_id, created_at, channel, DATE_TRUNC('month', created_at) AS cohort_month
  FROM users
  WHERE created_at < NOW() - INTERVAL '31 days'
),
active_d30 AS (
  SELECT DISTINCT c.user_id
  FROM cohort c
  JOIN events e ON e.user_id = c.user_id
  WHERE e.event_name = 'read_session'
    AND e.event_time >= c.created_at + INTERVAL '28 days'
    AND e.event_time <  c.created_at + INTERVAL '31 days'
)
SELECT c.cohort_month,
       c.channel,
       COUNT(*)                                      AS new_users,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY c.cohort_month), 1) AS share_of_cohort,
       ROUND(100.0 * COUNT(a.user_id) / COUNT(*), 1) AS retention_d30
FROM cohort c
LEFT JOIN active_d30 a USING (user_id)
GROUP BY 1, 2
ORDER BY 1, new_users DESC;

-------------------------------------------------------------------------------
-- 3. Retention by app version (tests the "core got worse" signal from May)
--    Swap app_version for platform or campaign to check other cuts.
-------------------------------------------------------------------------------
WITH cohort AS (
  SELECT id AS user_id, created_at, app_version
  FROM users
  WHERE created_at >= DATE '2026-03-01'
    AND created_at < NOW() - INTERVAL '31 days'
),
active_d30 AS (
  SELECT DISTINCT c.user_id
  FROM cohort c
  JOIN events e ON e.user_id = c.user_id
  WHERE e.event_name = 'read_session'
    AND e.event_time >= c.created_at + INTERVAL '28 days'
    AND e.event_time <  c.created_at + INTERVAL '31 days'
)
SELECT c.app_version,
       COUNT(*)                                      AS new_users,
       ROUND(100.0 * COUNT(a.user_id) / COUNT(*), 1) AS retention_d30
FROM cohort c
LEFT JOIN active_d30 a USING (user_id)
GROUP BY 1
HAVING COUNT(*) >= 500
ORDER BY 1;

-------------------------------------------------------------------------------
-- 4. Reading funnel by cohort: finished first book -> started a second within 7 days
--    The case gives 65% and 30% only as six-month totals. This query checks
--    whether they changed over time (chronic problem vs part of the April drop).
-------------------------------------------------------------------------------
WITH firsts AS (
  SELECT u.id AS user_id,
         DATE_TRUNC('month', u.created_at) AS cohort_month,
         MIN(e.event_time) FILTER (WHERE e.event_name = 'book_finished') AS first_finish
  FROM users u
  LEFT JOIN events e ON e.user_id = u.id
  GROUP BY 1, 2
),
second AS (
  SELECT DISTINCT f.user_id
  FROM firsts f
  JOIN events e ON e.user_id = f.user_id
  WHERE e.event_name = 'book_started'
    AND e.event_time >  f.first_finish
    AND e.event_time <= f.first_finish + INTERVAL '7 days'
)
SELECT f.cohort_month,
       COUNT(*)                                                         AS users,
       ROUND(100.0 * COUNT(f.first_finish) / COUNT(*), 1)               AS finished_first_pct,
       ROUND(100.0 * COUNT(s.user_id) / NULLIF(COUNT(f.first_finish), 0), 1) AS second_within_7d_pct_of_finishers,
       ROUND(100.0 * COUNT(s.user_id) / COUNT(*), 1)                    AS second_within_7d_pct_of_all
FROM firsts f
LEFT JOIN second s USING (user_id)
GROUP BY 1
ORDER BY 1;

-------------------------------------------------------------------------------
-- 5. Cost per retained reader by channel (hypothesis 2 primary money metric)
--    Requires a spend table: marketing_spend(month, channel, spend)
-------------------------------------------------------------------------------
WITH cohort AS (
  SELECT id AS user_id, created_at, channel, DATE_TRUNC('month', created_at) AS cohort_month
  FROM users
  WHERE created_at < NOW() - INTERVAL '31 days'
),
active_d30 AS (
  SELECT DISTINCT c.user_id
  FROM cohort c
  JOIN events e ON e.user_id = c.user_id
  WHERE e.event_name = 'read_session'
    AND e.event_time >= c.created_at + INTERVAL '28 days'
    AND e.event_time <  c.created_at + INTERVAL '31 days'
),
by_channel AS (
  SELECT c.cohort_month, c.channel, COUNT(*) AS new_users, COUNT(a.user_id) AS retained
  FROM cohort c
  LEFT JOIN active_d30 a USING (user_id)
  GROUP BY 1, 2
)
SELECT b.cohort_month,
       b.channel,
       b.new_users,
       b.retained,
       ROUND(m.spend / NULLIF(b.new_users, 0), 2) AS cac,
       ROUND(m.spend / NULLIF(b.retained, 0), 2)  AS cost_per_retained_reader
FROM by_channel b
JOIN marketing_spend m ON m.month = b.cohort_month AND m.channel = b.channel
ORDER BY 1, cost_per_retained_reader DESC;
