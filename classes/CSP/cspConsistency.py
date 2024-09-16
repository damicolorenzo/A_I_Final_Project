from classes.CSP.display import Displayable

class Con_solver(Displayable):
    def __init__(self, csp, **kwargs):
        self.csp = csp
        super().__init__(**kwargs)    

    def make_arc_consistent(self, orig_domains=None, to_do=None):
        if orig_domains is None:
            orig_domains = {var:var.domain for var in self.csp.variables}
        if to_do is None:
            to_do = {(var, const) for const in self.csp.constraints
                     for var in const.scope}
        else:
            to_do = to_do.copy()  
        domains = orig_domains.copy()
        self.display(2,"Performing AC with domains", domains)
        while to_do:
            var, const = self.select_arc(to_do)
            self.display(3, "Processing arc (", var, ",", const, ")")
            other_vars = [ov for ov in const.scope if ov != var]
            new_domain = {val for val in domains[var]
                            if self.any_holds(domains, const, {var: val}, other_vars)}
            if new_domain != domains[var]:
                self.display(4, "Arc: (", var, ",", const, ") is inconsistent")
                #Eliminazione dell'elemento dal dominio
                print("Deleted", str(domains[var].difference(new_domain)), "from", var) 
                self.display(3, "Domain pruned", "dom(", var, ") =", new_domain,
                                 " due to ", const)
                domains[var] = new_domain
                add_to_do = self.new_to_do(var, const) - to_do
                to_do |= add_to_do     
                self.display(3, "  adding", add_to_do if add_to_do else "nothing", "to to_do.")
            self.display(4, "Arc: (", var, ",", const, ") now consistent")
        self.display(2, "AC done. Reduced domains", domains)
        return domains

    def new_to_do(self, var, const):
        return {(nvar, nconst) for nconst in self.csp.var_to_const[var]
                if nconst != const
                for nvar in nconst.scope
                if nvar != var}

    def select_arc(self, to_do):
        return to_do.pop() 

    def any_holds(self, domains, const, env, other_vars, ind=0):
        if ind == len(other_vars):
            return const.holds(env)
        else:
            var = other_vars[ind]
            for val in domains[var]:
                env[var] = val
                if self.any_holds(domains, const, env, other_vars, ind + 1):
                    return True
            return False

    def solve_one(self, domains=None, to_do=None):
        new_domains = self.make_arc_consistent(domains, to_do)
        if any(len(new_domains[var]) == 0 for var in new_domains):
            return False
        elif all(len(new_domains[var]) == 1 for var in new_domains):
            self.display(2, "SOLUTION:", {var: select(
                new_domains[var]) for var in new_domains}, "\n")
            #rimozione del return che ritornerebbe una singola soluzione del problema
        else:
            var = self.select_var(x for x in self.csp.variables if len(new_domains[x]) > 1)
            if var:
                dom1, dom2 = partition_domain(new_domains[var])
                self.display(3, "...splitting", var, "into", dom1, "and", dom2)
                new_doms1 = copy_with_assign(new_domains, var, dom1)                
                new_doms2 = copy_with_assign(new_domains, var, dom2)
                to_do = self.new_to_do(var, None)
                self.display(3, " adding", to_do if to_do else "nothing", "to to_do.")
                return self.solve_one(new_doms1, to_do) or self.solve_one(new_doms2, to_do)

    def select_var(self, iter_vars):
        return select(iter_vars)

def partition_domain(dom):
    split = len(dom) // 2
    dom1 = set(list(dom)[:split])
    dom2 = dom - dom1
    return dom1, dom2
    
def copy_with_assign(domains, var=None, new_domain={True, False}):
    newdoms = domains.copy()
    if var is not None:
        newdoms[var] = new_domain
    return newdoms

def select(iterable):
    for e in iterable:
        return e  

from searchProblem import Arc, Search_problem

class Search_with_AC_from_CSP(Search_problem,Displayable):
    def __init__(self, csp):
        self.cons = Con_solver(csp)  
        self.domains = self.cons.make_arc_consistent()

    def is_goal(self, node):
        return all(len(node[var])==1 for var in node)
    
    def start_node(self):
        return self.domains
    
    def neighbors(self,node):
        neighs = []
        var = select(x for x in node if len(node[x])>1)
        if var:
            dom1, dom2 = partition_domain(node[var])
            self.display(2,"Splitting", var, "into", dom1, "and", dom2)
            to_do = self.cons.new_to_do(var,None)
            for dom in [dom1,dom2]:
                newdoms = copy_with_assign(node,var,dom)
                cons_doms = self.cons.make_arc_consistent(newdoms,to_do)
                if all(len(cons_doms[v])>0 for v in cons_doms):
                    neighs.append(Arc(node,cons_doms))
                else:
                    self.display(2,"...",var,"in",dom,"has no solution")
        return neighs


