import datetime
import task

def name_contain(task_list: list, text: str) -> list:
    ret = []
    for task in task_list:
        if text in task.name:
            ret.append(task)
    return ret

def description_contain(task_list: list, text: str) -> list:
    ret = []
    for task in task_list:
        if text in task.description:
            ret.append(task)
    return ret

def id_contain(task_list: list, text: str) -> list:
    ret = []
    for task in task_list:
        if text in str(task.id):
            ret.append(task)
    return ret

def tags_contain(task_list: list, text: str) -> list:
    ret = []
    for task in task_list:
        for tag in task.tags:
            if text in tag:
                ret.append(task)
                break    
    return ret

def activities_contain(task_list: list, text: str) -> list:
    ret = []
    for task in task_list:
        for act in task.activities:
            if text in act.description:
                ret.append(task)
                break    
    return ret

def priority_lt(task_list: list, priority: str):
    ret = []
    for task in task_list:
        if task.priority < int(priority):
            ret.append(task)
    return ret

def priority_gt(task_list: list, priority: str):
    ret = []
    for task in task_list:
        if task.priority > int(priority):
            ret.append(task)
    return ret

def priority_eq(task_list: list, priority: str):
    ret = []
    for task in task_list:
        if task.priority == int(priority):
            ret.append(task)
    return ret

def created_lt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.creation_date < datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def created_gt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.creation_date > datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def created_eq(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.creation_date == datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def due_date_lt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.due_date < datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def due_date_gt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.due_date > datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def due_date_eq(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.due_date == datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def start_date_lt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.schedule.start_date < datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def start_date_gt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.schedule.start_date > datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def start_date_eq(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        if task.schedule.start_date == datetime.date.fromisoformat(date_str):
            ret.append(task)
    return ret

def activity_date_lt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        for act in task.activities:
            if act.date < datetime.date.fromisoformat(date_str):
                ret.append(task)
                break
    return ret

def activity_date_gt(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        for act in task.activities:
            if act.date > datetime.date.fromisoformat(date_str):
                ret.append(task)
                break
    return ret

def activity_date_eq(task_list: list, date_str: str):
    ret = []
    for task in task_list:
        for act in task.activities:
            if act.date == datetime.date.fromisoformat(date_str):
                ret.append(task)
                break
    return ret

map_filter = {
    "name =": name_contain,
    "description =": description_contain,
    "id =": id_contain,
    "tag =": tags_contain,
    "activity =": activities_contain,
    "priority <": priority_lt,
    "priority >": priority_gt,
    "priority =": priority_eq,
    "created <": created_lt,
    "created >": created_gt,
    "created =": created_eq,
    "due_date <": due_date_lt,
    "due_date >": due_date_gt,
    "due_date =": due_date_eq,
    "start_date <": start_date_lt,
    "start_date >": start_date_gt,
    "start_date =": start_date_eq,
    "activity_date <": activity_date_lt,
    "activity_date >": activity_date_gt,
    "activity_date =": activity_date_eq,
}
