GRAPH.QUERY reserve_meeting "CREATE (:Step {order: 0, req: '', tpl:'reserve_meeting_begin'})-[:next]->(:Step {order: 1, req:'title', tpl:'reserve_meeting_1'})-[:next]->(:Step {order: 2, req:'date', tpl:'reserve_meeting_2'})-[:next]->(:Step {order: 3, req:'time', tpl:'reserve_meeting_3'})-[:next]->(:Step {order: 4, req:'agenda', tpl:'reserve_meeting_4'})-[:next]->(:Step {order: 5, req:'attendees', tpl:'reserve_meeting_5'})-[:next]->(:Step {order: 6, req:'place', tpl:'reserve_meeting_6'})-[:next]->(:Step {order: 7, req: 'title,date,time,agenda,attendees,place', tpl:'reserve_meeting_end'})"
