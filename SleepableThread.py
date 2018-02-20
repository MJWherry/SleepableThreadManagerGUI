import threading
import time


class SleepableThread(threading.Thread):

    thread = None                   # The thread to be used for the work function
    work_function = None            # The function to be executed
    thread_command_mappings = {}    # Command mappings for available functions
    thread_state_mappings = {}      # State mappings for the thread

    thread_message_queue = []       # A Message queue for the thread to report to UI

    args = {}

    thread_state = 0                # The current thread state

    run_amount = 0                  # How many times the thread should run, if specified
    sleep_amount = 0                # How many iterations the thread should sleep, if specified

    work_count = -1                 # Run thread ? times
    max_work_count = -1             # Limit number of executions
    sleep_count = -1                # Sleep thread ? times
    max_sleep_count = -1            # Limit sleep

    sleep_wait_seconds = 3          # Wait ? seconds between sleep checks
    work_wait_seconds = 1           # Wait ? seconds between function executions

    def __init__(self, sleep_wait=3, work_wait=3, max_work=-1, max_sleep=-1, work=-1, sleep=-1):
        super(SleepableThread, self).__init__(target=self.run, args=())
        self.work_function = self.__default_work_function__
        self.thread_command_mappings = {'create': self.create_thread, 'start': self.start_thread,
                                        'sleep': self.sleep_thread, 'wake': self.wake_thread,
                                        'stop': self.stop_thread, 'restart': self.restart_thread}
        self.thread_state_mappings = {1: 'READY', 2: 'RUNNING', 3: 'SLEEPING', 4: 'ENDED'}
        self.work_wait_seconds = work_wait
        self.sleep_wait_seconds = sleep_wait
        self.max_work_count = max_work
        self.max_sleep_count = max_sleep
        self.work_count = work
        self.sleep_count = sleep
        self.create_thread()

    def __default_work_function__(self):
        print ' Running...'

    def set_thread_work(self, work):
        self.stop_thread()
        self.work_function = work
        self.create_thread()

    def create_thread(self):
        if self.thread_state == 1:
            print ' Thread already created.'
        else:
            print ' Creating thread.'
            self.thread = threading.Thread(target=self.work_function, args=())
            self.thread_state = 1

    def start_thread(self):
        if self.thread_state == 1:
            print ' Starting thread.'
            if self.isAlive() is False:
                self.start()
            self.thread_state = 2
        elif self.thread_state == 2:
            print ' The thread has already started.'
        elif self.thread_state == 3:
            print ' The thread has already started and is currently asleep.'
        elif self.thread_state == 4:
            print ' The thread is ended. Try restarting the thread.'

    def sleep_thread(self):
        if self.thread_state == 1:
            print ' The thread has not started yet.'
        elif self.thread_state == 2:
            print ' Sleeping thread.'
            self.thread_state = 3
        elif self.thread_state == 3:
            print ' The thread is already sleeping.'
        elif self.thread_state == 4:
            print ' The thread has already ended.'

    def wake_thread(self):
        if self.thread_state == 1:
            print ' The thread has not started yet.'
        elif self.thread_state == 2:
            print ' The thread is running and not sleeping.'
        elif self.thread_state == 3:
            print ' Waking thread.'
            self.thread_state = 2
        elif self.thread_state == 4:
            print ' The thread has already ended.'

    def stop_thread(self):
        if self.thread_state == 1:
            print ' The thread has not started yet.'
        elif self.thread_state == 2 or self.thread_state == 3:
            print ' Stopping thread.'
            self.thread_state = 4
        elif self.thread_state == 4:
            print ' The thread has already ended.'

    def restart_thread(self):
        if self.thread_state == 2 or self.thread_state == 3:
            self.stop_thread()
        if self.thread_state == 4:
            self.create_thread()
        if self.thread_state == 1:
            self.start_thread()

    def thread_status(self, include_settings=True):
        status = ' {}({}):{}'.format(self.name, self.work_function.im_func.__name__, self.sub_thread_status())
        if include_settings:
            status += '\n\t{}'.format(self.thread_settings())
        return status

    def thread_settings(self):
        return ' {}: {:>20}\n\t{}: {:>20}\n\t{}: {:>20}\n\t{}: {:>20}\n\t{}: {:>20}\n\t{}: {:>20}'.format(
            'Max Work Iterations', self.max_work_count, 'Max Sleep Iterations', self.max_sleep_count, 'Work Iterations'
            , self.work_count, 'Sleep Iterations', self.sleep_count, 'Work Wait Seconds', self.work_wait_seconds,
            'Sleep wait seconds', self.sleep_wait_seconds)

    def run(self):
        while self.thread_state != 5 or self.work_count < self.max_work_count:
            while self.thread_state != 4 or self.work_count < self.max_work_count:
                if self.thread_state == 2:
                    while self.thread_state == 2:
                        if self.thread.isAlive() is False:
                            self.thread = threading.Thread(target=self.work_function, args=())
                        self.thread.run()
                        self.run_amount += 1
                        time.sleep(self.work_wait_seconds)
                elif self.thread_state == 3:
                    while self.thread_state == 3:
                        self.sleep_amount += 1
                        time.sleep(self.sleep_wait_seconds)

    def parse_thread_command(self, cmd):
        cmd = cmd.lower()
        self.thread_command_mappings[cmd].__call__()

    def terminal(self):
        while True:
            print ' Master thread:{}:{}(State {})'.format(self.name, self.thread_status(), self.thread_state)
            print ' Baby thread:{}:{} (Total spawned: {}) '.format(self.thread.name, self.thread.isAlive(),
                                                                   self.total_babies)
            cmd = raw_input(' Enter command: ')
            self.parse_thread_command(cmd)


if __name__ == "__main__":
    t = SleepableThread()
    t.terminal()
