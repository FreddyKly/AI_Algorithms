
class TwoTwoFourConstraint():
    def __init__(self, variables) -> None:
        self.variables = variables

    def satisfied(self, assignment):
        if len(set(assignment.values())) < len(assignment):
            return False

        if len(assignment) == len(self.variables):
            t = assignment['T']
            w = assignment['W']
            o = assignment['O']
            f = assignment['F']
            u = assignment['U']
            r = assignment['R']
            two = t * 100 + w * 10 + o
            four = f * 1000 + o * 100 + u * 10 + r

            return two + two == four
        return True


class CSP():
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should habe a domain")

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for costraint in self.constraints[variable]:
            if not costraint.satisfied(assignment):
                return False
        return True

    def backtracking(self, assignment = {}):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]

        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result = self.backtracking(local_assignment)
                if result is not None:
                    return result
        return None


if __name__ == "__main__":
    variables = ['T', 'W', 'O', 'F', 'U', 'R']
    domains = {}
    for variable in variables:
        domains[variable] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    domains['F'] = [1]
    csp = CSP(variables, domains)
    csp.add_constraint(TwoTwoFourConstraint(variables))
    solution = csp.backtracking()
    if solution is None: 
        print("No Solution found")
    else:
        print(solution)