import redis

r = redis.Redis()

reply = r.graph('reserve_meeting').query("MATCH (n) RETURN n.order, n.req, n.tpl")

print(reply.result_set)

for x in range(len(reply.result_set)):
    print(reply.result_set[x])
    print(reply.result_set[x][0])
    print(reply.result_set[x][1])
    print(reply.result_set[x][2])
