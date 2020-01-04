from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from task import *
import datetime


class TagLabel(Entry):
    def __init__(self, master=None, text="",clickdestroy=False, *cnf, **kw):
        super().__init__(master=master, *cnf, **kw)
        self.v = StringVar()
        self.v.set(text)
        self.config(state="readonly",textvariable=self.v, justify=CENTER)
        if clickdestroy:
             self.bind("<Button-1>",self.destroy)

    def destroy(self,event=None):
        return super().destroy()

    def get_text(self):
        return self.v.get()


class DText(Text):
    def __init__(self, master=None, text="", *cnf, **kw):
        super().__init__(master=master, *cnf, **kw)
        line = text.count("\n") + 1
        self.config(height=line)
        self.insert("1.0",text)
        self.config(state=DISABLED)

class app(Tk):
    def __init__(self, screenName=None, baseName=None, className="Doit!", useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)
        self.tcont = TaskContainer()
        #self.tcont.today = datetime.date.fromisoformat("2019-12-30") # enable just for test/debugging purpose
        self.current_task = None
        self.drow_menu_frame()
        self.drow_panel()
        self.drow_list()
        self.drow_task_frame()
        self.drow_reschedule_frame()
        self.drow_new_task_frame()
        self.drow_complete_frame()

        if len(self.tcont.task_list) > 0:
            self.fetch_list()
            if len(self.tcont.day_tasks_list) > 0:
                self.fetch_activities(self.tcont.day_tasks_list[0])
                self.update_task_frame(self.list_day)
                self.task_frame.pack(fill=BOTH, expand=True)
        
        if len(self.tcont.old_list) > 0:
            self.fetch_old()

    def drow_menu_frame(self):
        menu_frame = Frame(self, bg="gray")
        Button(menu_frame,text="new task", command=self.new_event).pack(side=LEFT, padx=5,pady=5)
        Button(menu_frame,text="save", command=self.save_event).pack(side=LEFT, padx=5,pady=5)
        menu_frame.pack(fill=X)

    def drow_panel(self):
        self.pw = ttk.PanedWindow(self, orient=HORIZONTAL)
        self.pw.pack(fill=BOTH, expand=True)
        self.list_frame = ttk.Frame(self.pw,width=150, height=300,relief=SUNKEN)
        self.main_frame = ttk.Frame(self.pw,width=150, height=300,relief=SUNKEN)
        self.pw.add(self.list_frame,weight=1)
        self.pw.add(self.main_frame,weight=6)
    
    def drow_complete_frame(self):
        self.complete_frame =  ttk.Frame(self.main_frame)

        self.title_complete_string = StringVar()
        self.title_complete_string.set("Completing task: {}")
        title_complete_label = Entry(self.complete_frame, textvariable=self.title_complete_string ,font="Keraleeyam-Regular 16 bold",bd=0,state="readonly", justify=CENTER)
        
        comment_label = Label(self.complete_frame,text="Comment" ,font="LiberationMono-Bold 10")
        self.complete_text = Text(self.complete_frame,height=10,font="FreeMono 10")

        cancel_button = ttk.Button(self.complete_frame ,text="cancel", command=self.cancel_event)
        complete_button = ttk.Button(self.complete_frame ,text="Complete", command=self.complete_task_event)
        
        title_complete_label.pack(fill=BOTH, padx=10,pady=15)
        comment_label.pack(fill=BOTH,padx=10)
        self.complete_text.pack(pady=5, fill=X)

        complete_button.pack(side=RIGHT, pady=15)
        cancel_button.pack(side=RIGHT, pady=15,padx=40)

    def drow_reschedule_frame(self):
        self.reschedule_frame = ttk.Frame(self.main_frame)

        self.title_reschedule_string = StringVar()
        self.title_reschedule_string.set("Reschedule task: {}")
        title_reschedule_label = Entry(self.reschedule_frame, textvariable=self.title_reschedule_string ,font="Keraleeyam-Regular 16 bold",bd=0,state="readonly", justify=CENTER)
        
        activity_label = Label(self.reschedule_frame,text="Description of the WIP" ,font="LiberationMono-Bold 10")
        self.reschedule_text = Text(self.reschedule_frame,height=10,font="FreeMono 10")

        calendar_frame = ttk.Frame(self.reschedule_frame)
        calendar_frame.grid_rowconfigure(0, weight=1)
        calendar_frame.grid_columnconfigure(0, weight=1)

        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        calendar_label = Label(calendar_frame,text="reschedule date" ,font="LiberationMono-Bold 10")
        self.calendar = Calendar(calendar_frame, date_pattern="y-mm-dd",
                   font="Arial 8", selectmode='day',
                   cursor="hand1", year=tomorrow.year, month=tomorrow.month, day=tomorrow.day)
        hour_label = Label(calendar_frame,text="expeted time to dedicate (unity is 10min)" ,font="LiberationMono-Bold 10")
        self.hour_string = StringVar() 
        hour_box = Spinbox(calendar_frame, from_=1, to=36, textvariable=self.hour_string, command=self.update_label_reschedule_time)
        self.hour_label = Label(calendar_frame,text="0h 10m" ,font="LiberationMono-Bold 10")
        self.stick = IntVar()
        stick_box = Checkbutton(calendar_frame, text="do not postpone", font="LiberationMono-Bold 10", variable=self.stick)
        
        calendar_label.grid(column=0,row=0)
        self.calendar.grid(column=0,row=1)
        hour_label.grid(column=1,row=0, rowspan=3, padx=50)
        hour_box.grid(column=2,row=0,rowspan=3)
        self.hour_label.grid(column=3,row=0,rowspan=3,padx=5)
        stick_box.grid(column=0,row=2, pady=5)

        cancel_button = ttk.Button(self.reschedule_frame ,text="cancel", command=self.cancel_event)
        reschedule_button = ttk.Button(self.reschedule_frame ,text="Reschedule", command=self.reschedule_task_event)

        title_reschedule_label.pack(pady=15,fill=X)
        activity_label.pack()
        self.reschedule_text.pack(pady=5, fill=X)
        calendar_frame.pack()
        reschedule_button.pack(side=RIGHT, pady=15)
        cancel_button.pack(side=RIGHT, pady=15,padx=40)

    def drow_new_task_frame(self):
        self.new_task_frame = ttk.Frame(self.main_frame)
        title_label = Label(self.new_task_frame,text="New Task" ,font="Keraleeyam-Regular 16 bold")
        
        container_frame = ttk.Frame(self.new_task_frame)
        name_label = Label(container_frame,text="task name" ,font="Keraleeyam-Regular 10")
        self.name_new_task_string = StringVar()
        self.name_new_task_string.set("")
        name_new_task_entry = Entry(container_frame, textvariable=self.name_new_task_string ,font="Keraleeyam-Regular 10")

        tags_frame = ttk.Frame(self.new_task_frame)
        tags_label = Label(tags_frame,text="tags" ,font="Keraleeyam-Regular 10")
        self.tags_new_task_string = StringVar()
        self.tags_new_task_string.set("")
        tags_new_task_entry = Entry(tags_frame, textvariable=self.tags_new_task_string ,font="Keraleeyam-Regular 10")
        tags_new_task_entry.bind("<Return>", self.add_new_tag)
        self.tags_container = ttk.Frame(tags_frame)
        tags_label.grid(column=0,row=0)
        tags_new_task_entry.grid(column=1,row=0)
        self.tags_container.grid(column=2,row=0)
        
        description_new_label = Label(container_frame,text="Description" ,font="LiberationMono-Bold 10")
        self.description_new_text = Text(container_frame,font="FreeMono 10")

        calendar_frame = ttk.Frame(container_frame)
        calendar_frame.grid_rowconfigure(0, weight=1)
        calendar_frame.grid_columnconfigure(0, weight=1)

        day = datetime.date.today()
        calendar_start_label = Label(calendar_frame,text="start date" ,font="LiberationMono-Bold 10")
        self.calendar_start = Calendar(calendar_frame, date_pattern="y-mm-dd",
                   font="Arial 8", selectmode='day',
                   cursor="hand1", year=day.year, month=day.month, day=day.day)
        calendar_end_label = Label(calendar_frame,text="due date" ,font="LiberationMono-Bold 10")
        self.calendar_due = Calendar(calendar_frame, date_pattern="y-mm-dd",
                   font="Arial 8", selectmode='day',
                   cursor="hand1", year=day.year, month=day.month, day=day.day)
        self.stick_new = IntVar()
        stick_box = Checkbutton(calendar_frame, text="do not postpone", font="LiberationMono-Bold 10", variable=self.stick_new)
        
        label_frame = ttk.Frame(self.new_task_frame)
        label_frame.grid_rowconfigure(0, weight=1)
        label_frame.grid_columnconfigure(0, weight=1)

        hour_label = Label(label_frame,text="expeted time to dedicate (unity is 10min)" ,font="LiberationMono-Bold 10")
        self.hour_new_string = StringVar() 
        hour_box = Spinbox(label_frame,width=3, from_=1, to=36, textvariable=self.hour_new_string, command=self.update_label_new_time)
        self.hour_new_label = Label(label_frame,text="0h 10m" ,font="LiberationMono-Bold 10")
        priority_new_label = Label(label_frame,text="priority 1-5 (1 is the highest)" ,font="LiberationMono-Bold 10")
        self.priority_new_string = StringVar() 
        priority_new_box = Spinbox(label_frame,width=3, from_=1, to=5, textvariable=self.priority_new_string)
        
        calendar_start_label.grid(column=0,row=0,pady=5)
        self.calendar_start.grid(column=0,row=1,pady=5)
        calendar_end_label.grid(column=0,row=2,pady=5)
        self.calendar_due.grid(column=0,row=3,pady=5)
        stick_box.grid(column=0,row=4,pady=5)

        hour_label.grid(column=0,row=0,pady=5)
        hour_box.grid(column=1,row=0,pady=5)
        self.hour_new_label.grid(column=2,row=0,pady=5)
        priority_new_label.grid(column=0,row=1,pady=5)
        priority_new_box.grid(column=1,row=1,pady=5)

        cancel_button = ttk.Button(self.new_task_frame ,text="cancel", command=self.cancel_event)
        create_button = ttk.Button(self.new_task_frame ,text="create", command=self.new_task_event)

        title_label.pack(pady=15,fill=X)
        container_frame.pack(fill=X,expand=True)
        name_label.grid(column=1,row=0,padx=15)
        name_new_task_entry.grid(column=1,row=1,padx=15,stick=N+E+S+W)
        description_new_label.grid(column=1,row=2,padx=15)
        self.description_new_text.grid(column=1,row=3,stick=N+E+S+W,padx=15)
        calendar_frame.grid(column=0,row=0, rowspan=5,padx=15)
        tags_frame.pack(padx=30,pady=10,fill=X)
        label_frame.pack(pady=5,padx=30)
        create_button.pack(side=RIGHT, pady=15)
        cancel_button.pack(side=RIGHT, pady=15,padx=40)

    
    def drow_task_frame(self):
        self.task_frame = ttk.Frame(self.main_frame)
        self.title_string = StringVar()
        self.title_string.set("Empty")
        title_label = Entry(self.task_frame , textvariable=self.title_string,font="Keraleeyam-Regular 16 bold",bd=0,state="readonly", justify=CENTER)
        self.id_string = StringVar()
        self.id_string.set("id")
        id_label = Entry(self.task_frame , textvariable=self.id_string,font="FreeMono 10",bd=0,state="readonly", justify=CENTER)

        ldabel_text_frame = Frame(self.task_frame )
        self.label_created = Label(ldabel_text_frame,text="created: {}",font="LiberationMono-Bold 10")
        self.label_due = Label(ldabel_text_frame,text="due date: {}",font="LiberationMono-Bold 10")
        self.label_state = Label(ldabel_text_frame,text="state: {}",font="LiberationMono-Bold 10")
        self.label_priority = Label(ldabel_text_frame,text="priority: {}",font="LiberationMono-Bold 10")
        self.label_time = Label(ldabel_text_frame,text="Time to dedicate: {}",font="LiberationMono-Bold 10")
        self.label_created.grid(column=0, row=0, padx=20)
        self.label_due.grid(column=1, row=0, padx=20)
        self.label_state.grid(column=2, row=0, padx=20)
        self.label_priority.grid(column=3, row=0, padx=20)
        self.label_time.grid(column=4,row=0,padx=20)


        tags_frame = ttk.Frame(self.task_frame)
        tags_label = Label(tags_frame,text="tags: " ,font="Keraleeyam-Regular 10")
        self.tags_frame = ttk.Frame(tags_frame)
        tags_label.grid(column=0,row=0)
        self.tags_frame.grid(column=1,row=0)

        main_task_frame = ttk.Frame(self.task_frame)
        tabs = ttk.Notebook(main_task_frame)

        activity_frame = ttk.Frame(tabs)
        activity_frame.grid_rowconfigure(0, weight=1)
        activity_frame.grid_columnconfigure(0, weight=1)
        self.activity_frame_main = Canvas(activity_frame)
        scroll1 = Scrollbar(activity_frame,orient=VERTICAL,command=self.activity_frame_main.yview)
        self.activity_frame_main.config(yscrollcommand=scroll1.set)
        self.activity_frame_main.grid(column=0, row=0, stick="news")
        scroll1.grid(column=1, row=0, stick="news")

        description_text_frame = Frame(tabs)
        description_text_frame.grid_rowconfigure(0, weight=1)
        description_text_frame.grid_columnconfigure(0, weight=1)
        self.description_text = Text(description_text_frame,font="FreeMono 10",wrap=WORD)
        self.description_text.insert('1.0', "description")
        self.description_text.bind('<FocusOut>',self.save_text)
        self.description_text.bind('<KeyPress>',self.save_new_desc)
        scroll = Scrollbar(description_text_frame,orient=VERTICAL,command=self.description_text.yview)
        self.description_text.config(yscrollcommand=scroll.set)

        tabs.add(description_text_frame,text="description")
        tabs.add(activity_frame,text="activities")
        tabs.pack(fill=BOTH, expand=True)

        self.complete_task_frame = ttk.Frame(self.task_frame)
        self.complete_task_frame.grid_rowconfigure(0, weight=1)
        self.complete_task_frame.grid_columnconfigure(0, weight=1)
        self.label_completed = Label(self.complete_task_frame,text="completed at: 0000-00-00",font="LiberationMono-Bold 10")
        self.description_completed_text = Text(self.complete_task_frame,font="FreeMono 10", height=10,wrap=WORD)
        self.description_completed_text.insert("1.0","completed")
        self.description_completed_text.config( state=DISABLED)
        self.label_completed.pack()
        self.description_completed_text.pack(fill=X)

        self.reschedule_button = ttk.Button(self.task_frame ,text="Reschedule", command=self.reschedule_event)
        self.complete_button = ttk.Button(self.task_frame ,text="Complete", command=self.complete_event)
        
        title_label.pack(fill=X,pady=5,padx=10)
        id_label.pack(fill=X,pady=5,padx=10)
        ldabel_text_frame.pack(pady=5,padx=10)
        tags_frame.pack(fill=X,pady=5,padx=100)
        main_task_frame.pack(fill=BOTH, expand=True, padx=100, pady=5)
        self.description_text.grid(column=0, row=0, stick="news")
        scroll.grid(column=1, row=0, stick="news")

        self.reschedule_button.pack(side=RIGHT, pady=15,padx=40)
        self.complete_button.pack(side=RIGHT, pady=15)        

    def drow_list(self):
        self.tabs = ttk.Notebook(self.list_frame)
        self.tabs.pack(fill=BOTH, expand=True)
        self.list_day = Listbox(self.tabs, selectmode=SINGLE)
        self.list_day.bind("<<ListboxSelect>>",self.update_main_frame_day)
        self.list_all = Listbox(self.tabs, selectmode=SINGLE)
        self.list_all.bind("<<ListboxSelect>>",self.update_main_frame_day)
        self.list_old = Listbox(self.tabs, selectmode=SINGLE)
        self.list_old.bind("<<ListboxSelect>>",self.update_main_frame_day)
        self.tabs.add(self.list_day,text="today")
        self.tabs.add(self.list_all,text="all")
        self.tabs.add(self.list_old,text="old")

    def fetch_activities(self,task):
        for w in self.activity_frame_main.winfo_children():
            w.destroy()
        for activity in task.activities:
            ttk.Label(self.activity_frame_main,text="date: {}".format(activity.date),font="LiberationMono-Bold 10",padding="0 25 0 10").pack(fill=X, padx=10)
            DText(self.activity_frame_main,activity.description,font="FreeMono 10",wrap=WORD).pack(fill=X,padx=10)

    def add_new_tag(self,event):
        TagLabel(self.tags_container,text=self.tags_new_task_string.get(),bg="yellow",clickdestroy=True).pack(padx=5,side=LEFT)

    def save_new_desc(self,event):
        self.current_task.description = self.description_text.get("1.0",END)

    def save_text(self,event):
        self.tcont.save()

    def save_event(self):
        self.current_task.description = self.description_text.get("1.0",END)
        self.tcont.save()

    def update_label_reschedule_time(self):
        self.hour_label.config(text="{}h {}m".format(int(int(self.hour_string.get())/6),int(int(self.hour_string.get())%6*10)))
    
    def update_label_new_time(self):
        self.hour_new_label.config(text="{}h {}m".format(int(int(self.hour_new_string.get())/6),int(int(self.hour_new_string.get())%6*10)))

    def fetch_old(self):
        count = 0
        for item in self.tcont.old_list:
            self.list_old.insert(count,item.name)
            count += 1

    def fetch_list(self):
        self.list_all.delete(0,END)
        self.list_day.delete(0,END)

        count = 0
        for item in self.tcont.day_tasks_list:
            self.list_day.insert(count,item.name)
            count += 1

        count = 0
        for item in self.tcont.task_list:
            self.list_all.insert(count, item.name)
            count += 1

        widget = self.tabs.winfo_children()[self.tabs.index(self.tabs.select())]
        widget.selection_set(0)

    def update_main_frame_day(self,event):
        widget = event.widget
        self.update_task_frame(widget)
        for w in self.main_frame.winfo_children():
            w.pack_forget()
        self.task_frame.pack(fill=BOTH, expand=True)

    def update_task_frame(self,widget=None,task=None):
        widget = self.tabs.winfo_children()[self.tabs.index(self.tabs.select())]
        if len(widget.curselection()) > 0 or task:
            if len(widget.curselection()):
                if self.tabs.index(self.tabs.select()) == 0:
                    self.current_task = self.tcont.day_tasks_list[widget.curselection()[0]] 
                elif self.tabs.index(self.tabs.select()) == 1:
                    self.current_task = self.tcont.task_list[widget.curselection()[0]]
            else:
                self.current_task = task
            self.title_string.set(self.current_task.name)
            self.id_string.set(self.current_task.id)
            self.description_text.config(state=NORMAL)
            self.description_text.delete(1.0,END)
            self.description_text.insert('1.0', self.current_task.description)

            for w in self.tags_frame.winfo_children():
                w.destroy()

            for tag in self.current_task.tags:
                TagLabel(self.tags_frame,text=tag,bg="yellow",clickdestroy=False).pack(padx=5,side=LEFT)

            if self.current_task.get_status() == "COMPLETED":
                self.description_text.config(state=DISABLED)
                self.reschedule_button.pack_forget()
                self.complete_button.pack_forget()
                self.description_completed_text.config(state=NORMAL)
                self.description_completed_text.delete("1.0",END)
                self.description_completed_text.insert("1.0",self.current_task.completed_comment)
                self.description_completed_text.config(state=DISABLED)
                self.label_completed.config(text="completed at: {}".format(self.current_task.completed_date.isoformat()))
                self.complete_task_frame.pack(fill=X,padx=100,pady=50) 
            else:
                self.description_text.config(state=NORMAL)
                self.complete_task_frame.pack_forget()
                self.reschedule_button.pack(side=RIGHT, pady=50,padx=40)
                self.complete_button.pack(side=RIGHT, pady=50)

            self.fetch_activities(self.current_task)        
            if self.current_task.get_status() == "NEXT" or self.current_task.get_status() == "PENDING":
                self.label_state.config(text="state: {} \u2192 {}".format(self.current_task.get_status(),str(self.current_task.schedule.start_date)))
            else:
                self.label_state.config(text="state: {}".format(self.current_task.get_status()))
            self.label_created.config(text="created: {}".format(str(self.current_task.creation_date)))
            self.label_due.config(text="due date: {}".format(self.current_task.due_date.isoformat()))
            self.label_priority.config(text="priotity: {}".format(int(self.current_task.priority)))
            self.label_time.config(text="Time to dedicate: {}h {}m".format(int(self.current_task.schedule.hour/6),int(self.current_task.schedule.hour%6*10)))

    def complete_event(self):
        self.task_frame.pack_forget()
        self.title_complete_string.set("Completing task: {}".format(self.current_task.id))
        self.complete_text.delete(1.0,END)
        self.complete_frame.pack(fill=X, padx=70)

    def complete_task_event(self):
        self.current_task.description = self.description_text.get("1.0",END)
        self.current_task.complete(self.complete_text.get("1.0",END))
        self.complete_frame.pack_forget()
        widget = self.tabs.winfo_children()[self.tabs.index(self.tabs.select())]
        self.update_task_frame(widget)
        self.task_frame.pack(fill=BOTH, expand=True)
        self.tcont.save()

    def cancel_event(self):
        childs = self.main_frame.winfo_children()
        for child in childs:
            child.pack_forget()
        self.task_frame.pack(fill=BOTH, expand=True)
    
    def new_event(self):
        self.name_new_task_string.set("")
        self.description_new_text.delete("1.0",END)
        self.calendar_due.selection_set(datetime.date.today())
        self.calendar_start.selection_set(datetime.date.today())
        self.stick_new.set(0)
        self.priority_new_string.set(1)
        self.hour_new_string.set(1)
        self.tags_new_task_string.set("")
        for w in self.tags_container.winfo_children():
            w.destroy()
        for w in self.main_frame.winfo_children():
            w.pack_forget()
        self.new_task_frame.pack(fill=X, padx=70)
    
    def new_task_event(self):
        istoday = False 
        if datetime.date.fromisoformat(self.calendar_start.get_date()) == datetime.date.today() and  datetime.date.fromisoformat(self.calendar_due.get_date()) == datetime.date.today():
            istoday = True
        tags = []
        for w in self.tags_container.winfo_children():
            tags.append(w.get_text())
        task = Task(name=self.name_new_task_string.get(),
            description=self.description_new_text.get("1.0",END),
            start_date=self.calendar_start.get_date(),
            due_date=self.calendar_due.get_date(),
            hour=int(self.hour_new_string.get()),
            priority=int(self.priority_new_string.get()),
            is_today=istoday,
            tags=tags,
            is_sticked=bool(self.stick_new.get())
            )
        self.tcont.add_task(task)
        self.tcont.save()
        self.fetch_list()
        self.new_task_frame.pack_forget()
        widget = self.tabs.winfo_children()[self.tabs.index(self.tabs.select())]
        self.update_task_frame(task=self.tcont.task_list[-1])     
        self.task_frame.pack(fill=BOTH, expand=True)

    def reschedule_event(self):
        self.title_reschedule_string.set("Reschedule task: {}".format(self.current_task.id))
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.calendar.selection_set(tomorrow)
        self.hour_string.set(1)
        self.reschedule_text.delete("1.0",END)
        self.stick.set(0)
        self.task_frame.pack_forget()
        self.reschedule_frame.pack(fill=X, padx=70)
        
    def reschedule_task_event(self):
        self.current_task.description = self.description_text.get("1.0",END)
        self.current_task.reschedule(Activity(self.reschedule_text.get("1.0",END)[:-1]),int(self.hour_string.get()), start_date = self.calendar.get_date(), is_sticked = bool(self.stick.get()))
        self.reschedule_frame.pack_forget()
        widget = self.tabs.winfo_children()[self.tabs.index(self.tabs.select())]
        self.update_task_frame(widget)
        self.task_frame.pack(fill=BOTH, expand=True)
        self.tcont.save()

if __name__ == "__main__":
    root = app()
    root.mainloop()
