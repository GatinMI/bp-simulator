import json
from json import JSONEncoder


class Workflow:

    def __init__(self, name):
        self.steps = []
        self.name = name

    def add_step(self, step):
        self.steps.append(step)


class Step(JSONEncoder):

    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

class Action:

    def __init__(self, id, name, result_step_id):
        self.id = id
        self.name = name
        self.result_step_id = result_step_id



class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # if not isinstance(obj, Action):
        #     return super(MyEncoder, self).default(obj)

        return obj.__dict__

if __name__ == "__main__":
    action = Action(1, "action", 13)

    step = Step(1, "step")
    step.add_action(action)

    wf = Workflow("Bars Epic")
    wf.add_step(step)

    print json.dumps(wf, cls=MyEncoder)
