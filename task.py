import uuid
import datetime
import pickle
from os import path
import json

#change the version only if some attributes are added to Activity, Schedule or Task classes
version = "1.0.6"

class Activity:
    def __init__(self, description="", hour=1):
        super().__init__()
        self.date = datetime.date.today()
        self.description = description
        self.hour = hour

class Schedule:
    def __init__(self,start_date="2000-01-01", hour="1", is_today=False, is_sticked=False):
        super().__init__()
        self.start_date = datetime.date.fromisoformat(start_date)
        self.is_sticked = is_sticked
        self.is_today = is_today
        self.hour = hour
        self.hour_old = None
        self.rescheduled = None

class Task:
    def __init__(self, name="", description="", start_date="2000-01-01", due_date="2000-01-01", hour=1, priority=1, is_today=False, tags=[], is_sticked=False) :
        super().__init__()
        self.name = name
        self.creation_date = datetime.date.today()
        self.priority = priority
        self.id = str(uuid.uuid4())
        self.schedule = Schedule(start_date,hour,is_today,is_sticked)
        self.description = description
        self.due_date = datetime.date.fromisoformat(due_date)
        self.activities = []
        self.tags = tags
        self.parents = []
        self.childs = []
        self.completed_date = None
        self.completed_comment = None

    def get_priority(self):
        if self.schedule.rescheduled == datetime.date.today() or self.completed_date == datetime.date.today():
            return -1
        elif self.schedule.is_today :
            return 0
        elif datetime.date.today() >= self.schedule.start_date and self.schedule.is_sticked:
            return 1
        elif datetime.date.today() >= self.schedule.start_date:
            return (self.due_date - datetime.date.today()).days * self.priority
        else :
            return -2

    def complete(self, comment: str):
        self.completed_date = datetime.date.today()
        self.completed_comment = comment
        self.schedule.hour_old = self.schedule.hour

    def reschedule(self, activity, hour: int, start_date, is_sticked: bool=False):
        self.schedule.rescheduled = datetime.date.today() 
        self.activities.append(activity)
        self.schedule.start_date = datetime.date.fromisoformat(start_date)
        self.schedule.hour_old = self.schedule.hour
        self.schedule.hour = hour
        self.schedule.is_sticked = is_sticked
    
    def get_status(self):
        status = ""
        if self.completed_date:
            status = "COMPLETED"
        elif self.get_priority() == -1:
            status = "NEXT"
        elif self.get_priority() > 0 and self.schedule.is_sticked:
            status = "STICKED"
        elif self.get_priority() > 0:
            status = "SCHEDULED"
        elif self.get_priority() == -2:
            status = "PENDING"
        elif self.get_priority() == 0:
            status = "TODAY"
        return status
    
    def __gt__(self, value):
        return self.get_priority() > value.get_priority()

    def __lt__(self, value):
        return self.get_priority() < value.get_priority()
    
    def __eq__(self, value):
        return self.get_priority() == value.get_priority()

    def __str__(self):
        return json.dumps(self.to_map())
    
    def to_map(self):
        return { "name" : self.name,
            "priority" : self.priority if "priotity" in dir(self) else 1, # added in version 1.0.1
            "id" : str(self.id),
            "creation_date" : str(self.creation_date),
            "childs": self.childs if "childs" in dir(self) else [],
            "parents": self.parents if "parents" in dir(self) else [],
            "schedule" : {
                "start_date" : str(self.schedule.start_date),
                "is_sticked" : self.schedule.is_sticked,
                "is_today" : self.schedule.is_today,
                "hour" : self.schedule.hour,
                "hour_old": self.schedule.hour_old if "hour_old" in dir(self.schedule) else 1, # added in version 1.0.3
                "rescheduled" : str(self.schedule.rescheduled) if self.schedule.rescheduled else self.schedule.rescheduled
            },
            "description" : self.description,
            "due_date" : str(self.due_date),
            "activities" : [ { "date": str(act.date), 
                               "description": act.description,
                               "hour": act.hour if "hour" in dir(act) else 1 # added in version 1.0.5
                            } for act in self.activities ], 
            "tags" : self.tags if "tags" in dir(self) else [],
            "completed_date" : str(self.completed_date) if self.completed_date else self.completed_date,
            "completed_comment" : self.completed_comment
        }

class container:
    def __init__(self,task_list=[],day_task_list=[]):
        super().__init__()
        self.task_list = task_list
        self.day_task_list = day_task_list
        self.today: datetime.date = datetime.date.today()
        self.version = version

class TaskContainer():
    def __init__(self):
        super().__init__()
        # default values
        self.old_list = []
        self.day_tasks_list = []
        self.today = datetime.date.today()
        self.task_list = []

        # load history
        if path.exists("./old"):
            with open("old","rb") as db_old:
                self.old_list = pickle.load(db_old)
        
        # load the data
        if path.exists("./db"):
            with open("db","rb") as db:
                db = pickle.load(db)
                if db.version != version:
                    self.task_list = self.update_db(db.task_list)
                    self._del_completed_task()
                    self.refresh_day_tasks()
                    self.save()
                else:
                    self.day_tasks_list = db.day_task_list
                    self.today = db.today
                    self.task_list = db.task_list
                    self.refresh_day_tasks()
        
        #check if it needs a refresh
        if datetime.date.today() != self.today:
            self._del_completed_task()
            self.today = datetime.date.today()
            self.refresh_day_tasks()
            self.save()
        
    def update_db(self, task_list):
        t_list = []
        for task in task_list:
            tmap = task.to_map()
            t = Task(name=tmap["name"],description=tmap["description"],start_date=tmap["schedule"]["start_date"],
                    due_date=tmap["due_date"],hour=tmap["schedule"]["hour"],priority=int(tmap["priority"]),is_today=tmap["schedule"]["is_today"],
                    tags=tmap["tags"],is_sticked=tmap["schedule"]["is_sticked"])
            t.id = tmap["id"]
            t.creation_date = datetime.date.fromisoformat(tmap["creation_date"])
            for item in range(len(tmap["activities"])):
                a = Activity(description=tmap["activities"][item]["description"], hour=tmap["activities"][item]["hour"])
                a.date = datetime.date.fromisoformat(tmap["activities"][item]["date"])
                t.activities.append(a)
            t.childs = tmap["childs"]
            t.parents = tmap["parents"]
            t.schedule.rescheduled = datetime.date.fromisoformat(tmap["schedule"]["rescheduled"]) if tmap["schedule"]["rescheduled"] else None
            t.schedule.hour_old = tmap["schedule"]["hour_old"]
            t.completed_comment = tmap["completed_comment"]
            t.completed_date = datetime.date.fromisoformat(tmap["completed_date"]) if tmap["completed_date"] else None
            t_list.append(t)
        return t_list

    def save(self):
        with open("db","bw") as db:
            c = container(self.task_list,self.day_tasks_list)
            pickle.dump(c, db)

    def _del_completed_task(self):
        # iterate throught all task on task list and if it find some completed task move them on history
        count_pop = 0
        old_task_list = []
        for taskid in range(len(self.task_list)):
            if self.task_list[taskid-count_pop].get_status() == "COMPLETED":
                old_task_list.append(self.task_list[taskid-count_pop])
                self.task_list.pop(taskid-count_pop)
                count_pop += 1

        # if there are some new completed task save the updated history
        if len(old_task_list) > 0:
            self.__save_old__(old_task_list)

    def serach_task(self,uuid):
        for task in self.task_list:
            if task.id == uuid:
                return task
        for task in self.old_list:
            if task.id == uuid:
                return task
        return None

    def __save_old__(self, old_task_list):
        with open("old","bw") as db_old:
            self.old_list += old_task_list
            pickle.dump(self.old_list, db_old)

    def add_task(self, task: Task):
        self.task_list.append(task)
        self.refresh_day_tasks()

    def _calc_hcount(self):
        hcount = 0
        for task in self.day_tasks_list:
            hcount += task.schedule.hour
        return hcount

    def refresh_day_tasks(self):
        self.task_list.sort()
        hcount = 0
        self.day_tasks_list = []
        for task in self.task_list:
            if task.get_priority() != -2:
                if task.get_priority() == -1:
                    self.day_tasks_list.append(task)
                    hcount += task.schedule.hour_old
                elif task.get_priority() == 0 or task.get_priority() == 1:
                    self.day_tasks_list.append(task)
                    hcount += task.schedule.hour
                elif hcount + task.schedule.hour < 40:
                    self.day_tasks_list.append(task)
                    hcount += task.schedule.hour

    def _print_task_list(self):
        for task in self.task_list:
            print(task)

    def _print_day_list(self):
        for task in self.day_tasks_list:
            print(task)
