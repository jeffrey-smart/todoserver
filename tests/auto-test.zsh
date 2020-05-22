#!/bin/zsh

echo "-- expect empty list of tasks (1)"
curl http://127.0.0.1:5000/tasks/
echo ""
echo ""

echo "-- expect empty list of tasks (2)"
curl -I http://127.0.0.1:5000/tasks/
echo ""
echo ""

echo "-- create a task (3)"
curl -d '{"summary": "Get milk", "description": "One gallon whole milk"}' http://127.0.0.1:5000/tasks/
echo ""
echo ""

echo "-- create a task (4)"
curl -d '{"summary": "Post Office", "description": "Mail package"}' http://127.0.0.1:5000/tasks/
echo ""
echo ""

echo "-- get list of tasks (5)"
curl http://127.0.0.1:5000/tasks/
echo ""
curl -I http://127.0.0.1:5000/tasks/
echo ""
echo ""

echo "-- modify task #2 (6)"
curl -X PUT '{"summary": "Return shoes", "description": "Get refund"}' http://127.0.0.1:5000/tasks/2/
echo ""
echo ""

echo "-- get list of tasks (7)"
curl http://127.0.0.1:5000/tasks/
echo ""
curl -I http://127.0.0.1:5000/tasks/
echo ""
echo ""

echo "-- get details of Task 2 (8)"
curl http://127.0.0.1:5000/tasks/2/
echo ""
curl -I http://127.0.0.1:5000/tasks/2/
echo ""
echo ""

echo "-- delete task #1 (9)"
curl -X DELETE http://127.0.0.1:5000/tasks/1/
echo ""
echo ""

echo "-- get list of tasks (10)"
curl http://127.0.0.1:5000/tasks/
echo ""
echo ""

echo "-- get list of tasks (11)"
curl -I http://127.0.0.1:5000/tasks/
echo ""
echo ""
