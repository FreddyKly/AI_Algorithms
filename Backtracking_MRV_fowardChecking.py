
class CSP():
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should habe a domain")



    def backtracking():
        solution = ""
        

        return solution

    def solve():
        #"TWO" + "TWO" = "FOUR"
        null
    
    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable not in CSP")


if __name__ == "__main__":
    variables = ['T', 'W', 'O', 'F', 'U', 'R']
    domains = {}
    for variable in variables:
        domains[variable] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    csp = CSP(variables, domains)
    csp.solve()