from threading import Thread, current_thread


### Creating a Thread
def task1(
    task_id,
):
    print(f"Task {task_id}")


def main():
    thread = Thread(target=task1, args=(1,))

    thread.start()
    thread.join()


### Creating a Thread with subclass
class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self, name="subclassThread", args=(2, 3))

    def run(self):
        print("{0} is executing".format(current_thread().name))


if __name__ == "__main__":
    thread = MyThread()
    thread.start()
    thread.join()

    print("{0} exiting".format(current_thread().name))
    # main()
