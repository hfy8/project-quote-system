#!/bin/bash
DB_CID=$(docker ps -q --filter label=com.docker.swarm.service.name=quote-system_db | head -1)
echo "DB CID: $DB_CID"

echo "=== 杀掉阻塞查询 ==="
docker exec -i $DB_CID psql -U postgres -d quotation_db -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid != pg_backend_pid() AND datname='quotation_db' AND state != 'idle';"
sleep 3

echo "=== 开始通过 pipe 导入 331 条物料 ==="
cat ~/import_materials.sql | docker exec -i $DB_CID psql -U postgres -d quotation_db 2>&1 | tail -10

echo "=== 导入后统计 ==="
docker exec -i $DB_CID psql -U postgres -d quotation_db -c "SELECT category, COUNT(*) FROM materials GROUP BY category ORDER BY category;"