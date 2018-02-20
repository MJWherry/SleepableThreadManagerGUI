import threading
from SleepableThread import SleepableThread
from TestFunctions import NumberSequences

class SleepableThreadManager:

    threads = {str: SleepableThread}
    thread = None

    functions = NumberSequences()
    function_mappings = {}

    def __init__(self):
        self.thread = threading.Thread(target=self.terminal, args=())
        self.threads.popitem()
        self.function_mappings = {'Fibonacci': self.functions.fibonacci, 'Hailstorm': self.functions.hailstorm,
                                  'Square': self.functions.square, 'Triangle':self.functions.triangle,
                                  'Cube': self.functions.cube, 'Magic Square': self.functions.magic_square,
                                  'Hex': self.functions.hex}
        self.thread.start()

    def control(self, thread='', command=''):
        if thread == 'all':
            if command == 'remove':
                for item in self.threads.values():
                    item.stop_thread()
            else:
                for item in self.threads.values():
                    item.parse_thread_command(command)
        else:
            if command == 'create':
                s = SleepableThread(work_wait=0.1)
                self.threads[s.name] = s
            elif command == 'remove':
                if thread == 'all':
                    for item in self.threads.values():
                        item.stop_thread()
                    self.threads.clear()
                else:
                    self.threads[thread].stop_thread()
                    self.threads.pop(thread)
            else:
                self.threads[thread].parse_thread_command(command)

    def thread_stats(self):
        ready, running, sleeping, ended = 0, 0, 0, 0
        for item in self.threads.values():
            if item.thread_state==1:
                ready += 1
            elif item.thread_state==2:
                running += 1
            elif item.thread_state == 3:
                sleeping += 1
            elif item.thread_state ==4:
                ended += 1
        return ready, running, sleeping, ended

    def list(self):
        ret = ''
        for item in self.threads.values():
            ret += '{}{}'.format(item.thread_status(include_settings=False), '\n')
        print ret
        return ret

    def terminal(self):
        while True:
            x = raw_input(' Enter a command: ')
            if x == 'list':
                self.list()
            elif x == 'create':
                self.create_thread()
            else:
                self.threads[x.split(' ')[1]].parse_thread_command(x.split(' ')[0])

    def set_function(self, thread_name='', function_name=''):
        if thread_name=='all':
            for item in self.threads.values():
                item.set_thread_work(self.function_mappings[function_name])
        else:
            self.threads[thread_name].set_thread_work(self.function_mappings[function_name])


if __name__ == "__main__":
    man = SleepableThreadManager()
    man.terminal()
