class Search_problem(object):
    def start_node(self):
        raise NotImplementedError("start_node")   
    
    def is_goal(self,node):
        raise NotImplementedError("is_goal")   

    def neighbors(self,node):
        raise NotImplementedError("neighbors")   

    def heuristic(self,n):
        return 0

class Arc(object):
    def __init__(self, from_node, to_node, cost=1, action=None):
        assert cost >= 0, ("Cost cannot be negative for"+
                           str(from_node)+"->"+str(to_node)+", cost: "+str(cost))
        self.from_node = from_node
        self.to_node = to_node
        self.action = action
        self.cost=cost

    def __repr__(self):
        if self.action:
            return str(self.from_node)+" --"+str(self.action)+"--> "+str(self.to_node)
        else:
            return str(self.from_node)+str(self.to_node)

class Path(object):
    def __init__(self,initial,arc=None):
        self.initial = initial
        self.arc=arc
        if arc is None:
            self.cost=0
        else:
            self.cost = initial.cost+arc.cost

    def end(self):
        if self.arc is None:
            return self.initial
        else:
            return self.arc.to_node

    def nodes(self):
        current = self
        while current.arc is not None:
            yield current.arc.to_node
            current = current.initial
        yield current.initial

    def initial_nodes(self):
        if self.arc is not None:
            yield from self.initial.nodes()
        
    def __repr__(self):
        if self.arc is None:
            return str(self.initial)
        elif self.arc.action:
            return (str(self.initial)+"\n   --"+str(self.arc.action)
                    +"--> "+str(self.arc.to_node))
        else:
            return str(self.initial)+str(self.arc.to_node)