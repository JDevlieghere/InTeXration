class Task():

    def run(self):
        pass


class CloneTask(Task):

    def __init__(self, manager, request):
        self.build_manager = manager
        self.build_request = request

    def run(self):

        return