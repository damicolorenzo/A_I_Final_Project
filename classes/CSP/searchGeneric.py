from classes.CSP.display import Displayable
from classes.CSP.searchProblem import Path

class Searcher1(Displayable):

    def __init__(self, problem):
        self.problem = problem
        self.initialize_frontier()
        self.num_expanded = 0
        self.add_to_frontier(Path(problem.start_node()))
        self.negative_frontier = []
        self.solution = set()
        super().__init__()

    def initialize_frontier(self):
        self.frontier = []
        
    def empty_frontier(self):
        return self.frontier == []
        
    def add_to_frontier(self,path):
        self.frontier.append(path)
    
    def add_to_negfrontier(self,path):
        self.negative_frontier.append(path)
        
    def search(self):
        while not self.empty_frontier():
            path = self.frontier.pop()
            if len(self.negative_frontier) > 0:
                for i in range(0, len(self.negative_frontier)):
                    string = self.negative_frontier.pop()
                    #print(string, "inconsistent")
                #print(path, "consistent")
            #else:
                #print(path, "consistent")
            self.num_expanded += 1
            if self.problem.is_goal(path.end()):  
                self.solution.update({path})  
                #print(path, "SOLUTION")
            else:
                neighs, others = self.problem.neighbors(path.end())
                if len(list(others)) > 0:  
                    for arc in reversed(list(others)):
                        self.add_to_negfrontier(Path(path,arc))
                for arc in reversed(list(neighs)):
                    self.add_to_frontier(Path(path,arc))
        #print(self.solution)
        return self.solution

