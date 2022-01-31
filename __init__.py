from mycroft import MycroftSkill, intent_file_handler


class TodoistTaskManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('manager.task.todoist.intent')
    def handle_manager_task_todoist(self, message):
        self.speak_dialog('manager.task.todoist')


def create_skill():
    return TodoistTaskManager()

