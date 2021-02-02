import abc
import re

class Answerer:
    def __init__(self):
        self.dict = {}

    def __getitem__(self, data):
        for a in self.dict:
            if re.match(a, data):
                return self.dict[a]
        return Text_a


class AbstractProblem(abc.ABC):
    def __init__(self, ):
        self.name = name

    @abc.abstractmethod
    def proced(self, query):
        pass


problem

base_method = Answerer()
base_method[r'^Get problem$'] = Answer()
base_method[r'^Server$'] = Answer()