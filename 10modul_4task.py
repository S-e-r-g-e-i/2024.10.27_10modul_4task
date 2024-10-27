"""Домашнее задание по теме "Очереди для обмена данными между потоками." """

import threading
from random import randint
from time import sleep
from queue import Queue


class Table:
    def __init__(self, number: int, guest=None):
        self.number = number
        self.guest = guest


class Guest(threading.Thread):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def run(self):
        return sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        f1 = 0
        for i in range(0, len(guests)):
            for j in range(0, len(self.tables)):
                if self.tables[j].guest is None:
                    self.tables[j].guest = guests[i]
                    print(f'{guests[i].name} сел(-а) за стол номер {self.tables[j].number}')
                    f1 += 1
                    break
                else:
                    if guests[i] in self.queue.queue or f1 < len(self.tables):
                        continue
                    else:
                        self.queue.put(guests[i])
                        print(f'{guests[i].name} в очереди')

    def discuss_guests(self):
        for i in self.tables:
            i.guest.start()
        # for j in self.tables:
        #     j.guest.join()
        while not self.queue.empty() or sum([1 for i in self.tables if i.guest is not None]) > 0:
            for i in self.tables:
                if i.guest is None:
                    continue
                else:
                    if i.guest.is_alive() is False:
                        print(f'{i.guest.name} покушал(-а) и ушёл(ушла)')
                        print(f'Стол номер {i.number} свободен')
                        i.guest = None
                        if not self.queue.empty():
                            i.guest = self.queue.get()
                            print(f'{i.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {i.number}')
                            i.guest.start()





# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()



