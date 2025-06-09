from threading import Thread, Lock, Condition
import time


class PrimeFinder:
    def __init__(self):
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.running = True
        self.found = False
        self.prime_num = None

    def is_prime(self, num):
        if num == 2 or num == 3:
            return True
        div = 2
        while div <= num / 2:
            if num % div == 0:
                return False
            div += 1
        return True

    def find(self):
        i = 1
        while self.running:
            while not self.is_prime(i):
                i += 1
                time.sleep(0.5)

            self.condition.acquire()
            self.prime_num = i
            self.found = True
            self.condition.notify()
            self.condition.release()

            self.condition.acquire()
            while self.found and self.running:
                self.condition.wait()
            self.condition.release()

            i += 1

    def log(self):
        while self.running:
            self.condition.acquire()
            while not self.found and self.running:
                self.condition.wait()
            self.condition.release()

            if self.found:
                self.condition.acquire()
                print(self.prime_num)
                self.prime_num = None
                self.found = False
                self.condition.notify()
                self.condition.release()

    def run(self):
        find_thread = Thread(target=self.find)
        log_thread = Thread(target=self.log)

        find_thread.start()
        log_thread.start()

        time.sleep(3)
        self.running = False

        find_thread.join()
        log_thread.join()


class PollingPrimeFinder:
    def __init__(self):
        self.running = True
        self.found = False
        self.prime_num = None

    def is_prime(self, num):
        if num == 2 or num == 3:
            return True
        div = 2
        while div <= num / 2:
            if num % div == 0:
                return False
            div += 1
        return True

    def find(self):
        i = 1
        while self.running:
            while not self.is_prime(i):
                i += 1
            self.prime_num = i
            self.found = True

            time.sleep(0.5)

            i += 1

    def log(self):
        while self.running:
            time.sleep(0.5)

            if self.found:
                print(self.prime_num)
                self.prime_num = None
                self.found = False

    def run(self):
        find_thread = Thread(target=self.find)
        log_thread = Thread(target=self.log)

        find_thread.start()
        log_thread.start()

        time.sleep(3)
        self.running = False

        self.condition.acquire()
        self.condition.notifyAll()
        self.condition.release()

        find_thread.join()
        log_thread.join()


if __name__ == "__main__":
    # pollingPrimeFinder = PollingPrimeFinder()
    primeFinder = PrimeFinder()
    primeFinder.run()
