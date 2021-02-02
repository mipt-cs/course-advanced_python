class TextProblem(AbstractProblem):
    def __init__(self, request, answer, next_problem=None):
        self.request = request
        self.answer = answer
        self.next_problem = next_problem

    def proced(self, query):
        if query == request:
            return self.answer, self.next_problem

        else:
        	return f'\033[31mERROR\0330m "{query}" given. "{self.request}" expected', None