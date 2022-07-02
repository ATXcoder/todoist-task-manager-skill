from mycroft import MycroftSkill, intent_handler
import todoist


class TodoistTaskManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.todoist_api_key = "none"
        self.mycroft_label = "none"
        self.api = "none"
        self.todoist_api_key = self.settings.get('api_key')
        self.api = todoist.TodoistAPI(self.todoist_api_key)
        self.api.sync()

    # def initialize(self):
    #    self.check_for_mycroft_label()

    # This is called when a phrase in the 'manager.task.todoist.intent' file
    # is spoken by the user
    @intent_handler('manager.task.todoist.intent')
    def handle_manager_task_todoist(self, message):
        # List of responses for Mycroft to speak
        # self.speak_dialog('manager.task.todoist')
        full_name = self.api.state['user']['full_name']
        self.log.info("Grabbing tasks for: " + full_name)
        self.speak_dialog('manager.task.todoist')

    @intent_handler('add.task.intent')
    def handle_add_task(self, message):
        self.check_for_mycroft_label()
        task_name = message.data.get('task_name')
        item = self.api.items.add(task_name, labels=[self.mycroft_label])
        self.api.commit()
       # self.api.items.update(item['id'], )
       # self.log.info("Label: " + str(self.mycroft_label))
       # self.api.commit()
        # self.log.info("item: " + item['content'])
        self.speak_dialog('add.task', {'task_name': task_name})
       # self.api.sync()

    @intent_handler('complete.task.intent')
    def handle_complete_task(self, message):
        task_count = 0
        task_name = message.data.get('task_name')
        self.api.sync()
        for task in self.api.state['items']:
            if task['content'].lower() == task_name.lower():
                task_count += 1
                item = self.api.items.get_by_id(task['id'])
                item.complete()
                self.api.commit()
                self.log.info("Completed task '" + task['content'] + "'")
        self.speak_dialog('complete.task', {'task_count': task_count})

    def check_for_mycroft_label(self):
        self.mycroft_label = "none"
        self.api.sync()
        for label in self.api.state['labels']:
            if label['name'].lower() == "mycroft":
                self.log.info("Found 'mycroft' label")
                self.mycroft_label = label['id']

        if self.mycroft_label == "none":
            self.api.labels.add("mycroft")
            label = self.api.commit()
            self.mycroft_label = label['labels'][0]['id']
            self.log.info("Created 'mycroft' label, id: " + str(self.mycroft_label))

def create_skill():
    return TodoistTaskManager()

