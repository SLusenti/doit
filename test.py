from task import *
import random
import datetime

base = "c"

def test_task_generation():
    tcont.today = datetime.date(2019,12,22)
    for i in range(3):
        smonth = random.randint(1,6)
        sday = random.randint(1,22)
        plus = random.randint(0,6)
        hour = float(random.randint(1,5))/2 * 4
        tcont.add_task(Task("task-"+base+str(i),i,"2019-12-20","2020-{:02d}-{:02d}".format(smonth+plus,sday+plus),hour))

    for i in range(2):
        smonth = random.randint(1,6)
        sday = random.randint(1,22)
        plus = random.randint(0,6)
        hour =  float(random.randint(1,5))/2 * 4
        tcont.add_task(Task("task-"+base+str(i+10),i,"2020-{:02d}-{:02d}".format(smonth,sday),"2020-{:02d}-{:02d}".format(smonth+plus,sday+plus),hour))

    for i in range(2):
        smonth = random.randint(1,6)
        sday = random.randint(1,22)
        plus = random.randint(0,6)
        hour =  float(random.randint(1,5))/2 * 4
        tcont.add_task(Task("task-"+base+str(i+14),i,"2019-12-20","2020-{:02d}-{:02d}".format(smonth+plus,sday+plus),hour,1,False,[],True))

    smonth = random.randint(1,6)
    sday = random.randint(1,22)
    plus = random.randint(0,6)
    tcont.add_task(Task("task-"+base+str(i+17),i,"2019-12-20","2020-{:02d}-{:02d}".format(smonth+plus,sday+plus),plus+0.5,1,True))

    print("\ntasks:")
    tcont._print_task_list()

    print("\nday:")
    day = tcont.day_tasks_list
    tcont._print_day_list()

    #day[0].complete("ok")
    #day[1].reschedule(Activity("done my job!"),1)
    #day[2].reschedule(Activity("done my job!"),1)
    tcont.save()

    print("\nday:")
    tcont._print_day_list()



if __name__ == "__main__":
    tcont = TaskContainer()
    test_task_generation()
    #tcont.export_db()
    #for t in tcont.task_list:
    #    print(t.name,"\t",t.id)
    #print("\nimport")
    #tcont.import_db()
    #for t in tcont.task_list:
    #    print(t.name,"\t",t.id)