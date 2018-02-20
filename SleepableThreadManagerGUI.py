import ttk
from Tkinter import *
from ttk import Treeview
from SleepableThreadManager import *


class SleepableThreadManagerGUI:
    ui = None  # Main UI Window

    top = None  # Top UI frame
    bottom = None  # Bottom UI frame

    allow_scroll = True

    manager = None  # Sleepable thread manager

    iidList=[]

    ui_update_thread = None  # UI Update thread

    thread_dropdown = None  # Dropdown to select threads
    function_dropdown = None  # Dropdown to select functions

    thread_selected = None  # Variable for the thread selection
    threads_selected = []
    function_selected = None  # Variable for the function selection

    function_menu = None
    selection_context_menu = None
    empty_selection_context_menu = None

    info_tree_view = None  # Tree view for thread info
    output_textbox = None  # Output textbox for the UI thread to write to

    def __init__(self):
        self.manager = SleepableThreadManager()

        self.ui = Tk()
        self.ui.title('Sleepable Thread Manager')
        self.ui.geometry('550x600')

        self.function_selected = StringVar(self.ui)
        self.thread_selected = StringVar(self.ui)

        self.thread_selected.set('Select a Thread...')
        self.function_selected.set('Select a Function...')

        # create all of the main containers
        self.top = Frame(self.ui, width=300, height=50, pady=5)
        self.bottom = Frame(self.ui, bg='orange', width=300, height=20, pady=0)

        # main window
        self.ui.grid_columnconfigure(0, weight=1)  # expand main column when main ui resizes
        self.top.grid(row=0, sticky="ew")  # Stick top frame to east/west
        self.bottom.grid(row=1, sticky="nsew")  # Stick bottom frame to north/south/easy/west
        self.ui.grid_rowconfigure(1, weight=1)  # Expand bottom panel when main ui resizes

        # top frame component config
        self.top.grid_rowconfigure(0, weight=1)  # Expand first row when top frame resizes
        self.top.grid_rowconfigure(1, weight=1)  # Expand second row when top frame resizes
        self.top.grid_columnconfigure(1, weight=1)  # Expand second column when top frame resizes

        # bottom frame component config
        self.bottom.grid_rowconfigure(0, weight=1)  # Expand row 1 when bottom frame resizes
        self.bottom.grid_rowconfigure(1, weight=1)  # Expand row 2 when bottom frame resizes
        self.bottom.grid_columnconfigure(0, weight=1)  # Expand column 1 when bottom frame resizes
        self.bottom.grid_columnconfigure(0, weight=1)

        # create widgets for top frame
        function_label = Label(self.top, text='Function name:')
        self.function_dropdown = OptionMenu(self.top, self.function_selected, *self.manager.function_mappings.keys())

        # layout the widgets in the top frame
        function_label.grid(row=1, column=0)
        self.function_dropdown.grid(row=1, column=1, columnspan=3, sticky="ew")

        # create widgets for bottom frame
        self.selection_context_menu = Menu(self.info_tree_view)
        createMultiple = Menu(self.info_tree_view)
        functionMenu = Menu(self.selection_context_menu)
        functionMenu.add_command(label='Square', command = lambda : self.set_thread_function('Square'))
        functionMenu.add_command(label='Cube', command=lambda: self.set_thread_function('Cube'))

        self.selection_context_menu.add_cascade(label='Create...', menu=createMultiple)
        self.selection_context_menu.add_cascade(label='Set function...', menu=functionMenu)

        self.selection_context_menu.add_command(label='Start', command=self.start_thread)
        self.selection_context_menu.add_command(label='Sleep', command=self.sleep_thread)
        self.selection_context_menu.add_command(label='Wake', command=self.wake_thread)
        self.selection_context_menu.add_command(label='Stop', command=self.stop_thread)
        self.selection_context_menu.add_command(label='Restart', command=self.restart_thread)
        self.selection_context_menu.add_command(label='Remove', command=self.remove_thread)

        self.empty_selection_context_menu = Menu(self.info_tree_view)

        createMultiple.add_command(label='1', command=self.create_thread)
        createMultiple.add_command(label='5', command=lambda: self.create_thread(amount=5))
        createMultiple.add_command(label='10', command=lambda: self.create_thread(amount=10))
        createMultiple.add_command(label='20', command=lambda: self.create_thread(amount=20))

        self.empty_selection_context_menu.add_cascade(label='Create',menu=createMultiple)

        self.info_tree_view = Treeview(self.bottom, columns=('Function', 'Status'))
        self.info_tree_view.heading('#0', text='Thread Name')
        self.info_tree_view.heading('#1', text='Function Name')
        self.info_tree_view.heading('#2', text='Status')
        self.info_tree_view.column('#0', width=100, stretch=NO)
        self.info_tree_view.column('#1', width=75)
        self.info_tree_view.column('#2', width=100, stretch=NO)
        self.info_tree_view.bind('<Button-3>', self.popup)
        self.output_textbox = Text(self.bottom, background="white", font=("Helvetica", 8))

        self.output_scrollbar = Scrollbar(self.bottom, command=self.output_textbox.yview)
        self.info_scrollbar = Scrollbar(self.bottom, command=self.info_tree_view.yview)

        # layout for the widgets in the bottom frame
        self.info_tree_view.grid(row=0, column=0, sticky='nsew')
        self.info_scrollbar.grid(row=0, column=1, sticky="nse")
        self.info_tree_view.config(yscrollcommand=self.info_scrollbar.set)

        self.output_textbox.grid(row=1, column=0, sticky='nsew')
        self.output_scrollbar.grid(row=1, column=1, sticky="nse")
        self.output_textbox.config(yscrollcommand=self.output_scrollbar.set)

        self.ui_update_thread = SleepableThread(work_wait=0.5)
        self.ui_update_thread.set_thread_work(self.refresh_output)
        self.ui_update_thread.start_thread()

        # Mainloop
        self.ui.mainloop()

    # UI refresh
    def refresh_tree_view(self):
        self.info_tree_view.delete(*self.info_tree_view.get_children())
        for item in self.manager.threads.items():
            self.info_tree_view.insert('', 'end', text=item[0], values=
            (str(item[1].work_function), item[1].thread_state_mappings[item[1].thread_state]))


    def refresh_output(self):
        # function passed to ui thread, change to labels/gridview? need independent message queue on threads
        if self.manager.functions.MessageQueue.__len__() > 0:
            while self.manager.functions.MessageQueue.__len__() != 0:
                item = self.manager.functions.MessageQueue.pop()
                if len(item) >= 400:
                    raise Exception('Output too large')
                else:
                    self.output_textbox.delete('1.0',END)
                    self.output_textbox.insert(END, '{}\n'.format(item))
                    if self.manager.thread_stats()[1] > 0 and self.allow_scroll:
                        self.output_textbox.see('end')

    def popup(self, event):
        self.allow_scroll = False
        #iid = self.info_tree_view.identify_row(event.y)
        self.iidList = self.info_tree_view.selection()
        if self.iidList:
            if self.iidList > 0:
                for i in self.iidList:
                    self.threads_selected.append(self.info_tree_view.item(i)['text'])
            # self.info_tree_view.selection_set(iid)
            # self.thread_selected.set(self.info_tree_view.item(iid)['text'])
            self.selection_context_menu.post(event.x_root, event.y_root)
        else:
            self.empty_selection_context_menu.post(event.x_root, event.y_root)
            pass
        self.manager.functions.MessageQueue = []
        self.allow_scroll = True


    # Button functions
    def create_thread(self, amount=1):
        i = 0
        while i != amount:
            self.manager.control(command='create')
            i += 1
        self.refresh_tree_view()

    def remove_thread(self):
        while self.threads_selected.__len__() != 0:
            self.manager.control(thread=self.threads_selected.pop(), command='remove')
        self.refresh_tree_view()

    def start_thread(self):
        while self.threads_selected.__len__() != 0:
            self.manager.control(thread=self.threads_selected.pop(), command='start')
        self.refresh_tree_view()

    def restart_thread(self):
        while self.threads_selected.__len__() != 0:
            self.manager.control(thread=self.threads_selected.pop(), command='restart')
        self.refresh_tree_view()

    def sleep_thread(self):
        while self.threads_selected.__len__() != 0:
            self.manager.control(thread=self.threads_selected.pop(), command='sleep')
        self.refresh_tree_view()

    def wake_thread(self):
        while self.threads_selected.__len__() != 0:
            self.manager.control(thread=self.threads_selected.pop(), command='wake')
        self.refresh_tree_view()

    def stop_thread(self):
        while self.threads_selected.__len__() != 0:
            self.manager.control(thread=self.threads_selected.pop(), command='stop')
        self.refresh_tree_view()

    def set_thread_function(self, funct):
        while self.threads_selected.__len__() != 0:
            self.manager.set_function(self.threads_selected.pop(), funct)
        self.refresh_tree_view()


if __name__ == "__main__":
    ui = SleepableThreadManagerGUI()
