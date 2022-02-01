from mycroft import MycroftSkill, intent_handler
import todoist


class TodoistTaskManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.todoist_api_key = self.settings.get('api_key')

    # This is called when a phrase in the 'manager.task.todoist.intent' file
    # is spoken by the user
    @intent_handler('manager.task.todoist.intent')
    def handle_manager_task_todoist(self, message):
        # List of responses for Mycroft to speak
        # self.speak_dialog('manager.task.todoist')
        api = todoist.TodoistAPI(self.todoist_api_key)
        api.sync()
        full_name = api.state['user']['full_name']
        self.log.info("Grabbing tasks for: " + full_name)
        self.speak_dialog('manager.task.todoist')


def create_skill():
    return TodoistTaskManager()

