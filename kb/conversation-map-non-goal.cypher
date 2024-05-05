GRAPH.QUERY greetings_open "CREATE (:Begin {req_begin:'name', num_of_steps:0})-[:next]->(:End {req_end: 'name', template:'greet_with_name'})"
