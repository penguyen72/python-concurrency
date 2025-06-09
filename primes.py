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
        while self.running:
            self.condition.acquire()
            i = 1
            while not self.is_prime(i):
                i += 1

            self.condition.notify()
            self.found = True
            self.prime_num = i
            self.condition.release()

    def log(self):
        while self.running:
            self.condition.acquire()
            while not self.found and not self.prime_num:
                self.condition.wait()
                print(f"Found ${self.prime_num}")
                self.found = False
                self.prime_num = None
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


if __name__ == "__main__":
    primeFinder = PrimeFinder()
    primeFinder.run()
