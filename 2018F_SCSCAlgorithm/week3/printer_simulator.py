import random

from printer import Printer
from task import Task


def simulation(num_seconds, page_per_minute):
    lab_printer = Printer(page_per_minute)
    print_queue = list()  # Queue
    waiting_times = list()

    for current_second in range(0, num_seconds):
        if new_print_task():
            task = Task(current_second)
            print_queue.append(task)  # enqueue

        if (not lab_printer.busy()) and (len(print_queue) != 0):
            next_task = print_queue.pop(0)  # dequeue
            waiting_times.append(next_task.wait_time(current_second))
            lab_printer.start_next(next_task)

        lab_printer.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print('Average Wait {0:6.2f} secs {1:3d} tasks remaining.'.format(average_wait, len(print_queue)))


def new_print_task():
    num = random.randint(1, 181)
    if num == 180:
        return True
    else:
        return False


def main():
    for index in range(0, 10):
        simulation(3600, 5)


if __name__ == '__main__':
    main()