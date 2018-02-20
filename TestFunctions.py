
class NumberSequences:

    MessageQueue = []
    id = ''

    def __init__(self):
        pass

    c_fib_num = 0
    c_fib_prev1 = 1
    c_fib_prev2 = 0

    def fibonacci(self):
        self.MessageQueue.append('{}'.format(self.c_fib_num))
        self.c_fib_prev2 = self.c_fib_prev1
        self.c_fib_prev1 = self.c_fib_num
        self.c_fib_num = self.c_fib_prev1+self.c_fib_prev2

    c_hail_num = 11

    def hailstorm(self):
        self.MessageQueue.append('{}'.format(self.c_hail_num))
        if self.c_hail_num % 2 == 0:
            self.c_hail_num = self.c_hail_num / 2
        else:
            self.c_hail_num = self.c_hail_num * 3 + 1

    c_square_num = 1

    def square(self):
        self.MessageQueue.append('{}'.format(self.c_square_num * self.c_square_num))
        self.c_square_num += 1

    c_triangle_num = 1

    def triangle(self):
        self.MessageQueue.append('{}'.format(((self.c_triangle_num * (self.c_triangle_num + 1)) / 2)))
        self.c_triangle_num += 1

    c_cube_num = 1

    def cube(self):
        self.MessageQueue.append('{}'.format(self.c_cube_num * self.c_cube_num * self.c_cube_num))
        self.c_cube_num += 1

    c_hex_num = 1

    def hex(self):
        self.MessageQueue.append('{}'.format(2 * (self.c_hex_num * self.c_hex_num) - self.c_hex_num))
        self.c_hex_num += 1

    c_msquare_num = 1

    def magic_square(self):
        self.MessageQueue.append('{}'.format((self.c_msquare_num * ((self.c_msquare_num*self.c_msquare_num)+1))/2))
        self.c_msquare_num += 1
