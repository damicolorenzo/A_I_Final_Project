import random
import matplotlib.pyplot as plt

class Variable(object):
    def __init__(self, name, domain, position=None):
        self.name = name   
        self.domain = domain 
        self.position = position if position else (random.random(), random.random())
        self.size = len(domain) 

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name 

class Constraint(object):
    def __init__(self, scope, condition, string=None, position=None):
        self.scope = scope
        self.condition = condition
        if string is None:
            self.string = self.condition.__name__ + str(self.scope)
        else:
            self.string = string
        self.position = position

    def __repr__(self):
        return self.string

    def can_evaluate(self, assignment):
        return all(v in assignment for v in self.scope)
    
    def holds(self,assignment):
        return self.condition(*tuple(assignment[v] for v in self.scope))

class CSP(object):
    def __init__(self, title, variables, constraints):
        self.title = title
        self.variables = variables
        self.constraints = constraints
        self.var_to_const = {var:set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return f"CSP({self.title}, {self.variables}, {([str(c) for c in self.constraints])})"

    def consistent(self,assignment):
        return all(con.holds(assignment)
                    for con in self.constraints
                    if con.can_evaluate(assignment))

    def show(self):
        ax = plt.figure().gca()
        ax.set_axis_off()
        plt.title(self.title)
        var_bbox = dict(boxstyle="round4,pad=1.0,rounding_size=0.5")
        con_bbox = dict(boxstyle="square,pad=1.0",color="green")
        for var in self.variables:
            if var.position is None:
                var.position = (random.random(), random.random())
        for con in self.constraints:
            if con.position is None:
                con.position = tuple(sum(var.position[i] for var in con.scope)/len(con.scope) for i in range(2))
            for var in con.scope:
                ax.annotate(con.string, var.position, xytext=con.position, arrowprops={'arrowstyle':'-'}, bbox=con_bbox, ha='center')
        for var in self.variables:
            x,y = var.position
            plt.text(x,y,var.name,bbox=var_bbox,ha='center')
        plt.show()

