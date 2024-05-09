GRAPH.QUERY reserve_meeting "CREATE (:Begin {req_begin:'name', num_of_steps:5})-[:next]->(:First {req_first:'date', template_first:'reserve_meeting_first'})-[:next]->(:Second {req_second:'time', template_second:'reserve_meeting_second'})-[:next]->(:Third {req_third:'agenda', template_third:'reserve_meeting_third'})-[:next]->(:Fourth {req_fourth:'member', template_fourth:'reserve_meeting_fourth'})-[:next]->(:Fifth {req_fifth:'place', template_fifth:'reserve_meeting_fifth'})-[:next]->(:End {postcondition: 'name,date,time,agenda,member,place', template:'reserve_meeting_complete'})"