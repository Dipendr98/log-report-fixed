Parse the Apache-style access log at /app/access.log and write a summary report to
/app/report.json.

The report must be a JSON object with exactly these three keys:
1. "total_requests" - the total number of log lines (integer).
2. "unique_ips" - the count of distinct client IP addresses that appear (integer).
3. "top_path" - the request path (e.g. "/index.html") that appears most often across
all requests. If there is a tie, any of the tied paths is acceptable.

Do not modify /app/access.log.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
