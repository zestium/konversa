import redis

r = redis.Redis()

the_query = r.graph('reserve_meeting').query("MATCH (n) RETURN n.order, n.req, n.tpl")

class ReserveMeeting:

    def __init__(self):

        self.the_result = the_query.result_set

    def num_of_steps(self):

        return len(self.the_result)-1

    def get_req(self, idx_req):

        return self.the_result[idx_req][1]

    def get_tpl(self, idx_tpl):

        return self.the_result[idx_tpl][2]

    def get_all_reqs(self):

        result = self.the_result[-1][1].split(',')
        
        z = {}
        
        for a in result:
            z[a] = ''
        
        return z
     
