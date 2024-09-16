from classes.CSP.searchProblem import Arc, Search_problem

class Search_from_CSP(Search_problem):
    def __init__(self, csp, variable_order=None):
        self.csp=csp
        if variable_order:
            assert set(variable_order) == set(csp.variables)
            assert len(variable_order) == len(csp.variables)
            self.variables = variable_order
        else:
            self.variables = list(csp.variables)

    def is_goal(self, node):
        return len(node)==len(self.csp.variables)
    
    def start_node(self):
        return {}
    
    def neighbors(self, node):
        var = self.variables[len(node)] 
        res = []
        others = []
        for val in var.domain:
            new_env = node|{var:val}
            if self.csp.consistent(new_env):
                res.append(Arc(node,new_env))
            else:
                others.append(Arc(node, new_env)) #Frontiera negativa
        return res, others


