from threading import Lock, Thread


class Multithreading:

    def __init__(self):
        self.a = 0
        self.increment_lock = Lock()

    def function(self, arg):
        for _ in range(arg):
            with self.increment_lock:
                self.a += 1


def main():
    threads = []
    multithreading = Multithreading()
    for i in range(5):
        thread = Thread(target=multithreading.function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", multithreading.a)  # 5000000


main()
