import datetime
import os
from abc import ABC, abstractmethod
class Vehicle(ABC):

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def fuel_type(self):
        pass


class Car(Vehicle):
    def move(self):
        return "-> Car: Жолмен жоғары жылдамдықпен жүреді."

    def fuel_type(self):
        return "-> Car: Бензин/дизельді пайдаланады."


class Bicycle(Vehicle):
    def move(self):
        return "-> Bicycle: Велосипед жолымен ақырын жүреді."

    def fuel_type(self):
        return "-> Bicycle: Адам күшін пайдаланады."


def run_task1():
    print("--- ТАПСЫРМА 1: VEHICLE АБСТРАКЦИЯСЫ ---")
    my_car = Car()
    my_bicycle = Bicycle()

    print(f"\n[Car]: {my_car.move()}")
    print(f"[Car]: {my_car.fuel_type()}")

    print(f"\n[Bicycle]: {my_bicycle.move()}")
    print(f"[Bicycle]: {my_bicycle.fuel_type()}")
    print("-" * 50)

class DatabaseInterface(ABC):

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def disconnect(self): pass

    @abstractmethod
    def execute(self, query): pass


class MySQLDatabase(DatabaseInterface):
    def connect(self):
        print("-> MySQL: Қосылу орнатылды (порт 3306).")

    def disconnect(self):
        print("-> MySQL: Қосылым ажыратылды.")

    def execute(self, query):
        print(f"-> MySQL: Сұрау орындалды: '{query}'")


class PostgreSQLDatabase(DatabaseInterface):
    def connect(self):
        print("-> PostgreSQL: Қосылу орнатылды (порт 5432).")

    def disconnect(self):
        print("-> PostgreSQL: Қосылым жабылды.")

    def execute(self, query):
        print(f"-> PostgreSQL: Сұрау орындалды: '{query}'")


def run_task2():
    print("--- ТАПСЫРМА 2: DATABASE ИНТЕРФЕЙСІ ---")
    mysql_db = MySQLDatabase()

    mysql_db.connect()
    mysql_db.execute("SELECT * FROM users;")
    mysql_db.disconnect()

    print("-" * 50)

class Logger(ABC):

    def format_message(self, message: str) -> str:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        return f"{timestamp} - {message}"

    @abstractmethod
    def log(self, message: str):
        pass


class ConsoleLogger(Logger):
    def log(self, message: str):
        formatted_msg = self.format_message(f"[INFO] {message}")
        print(f"Консоль: {formatted_msg}")


class FileLogger(Logger):

    def __init__(self, filename="app_log.txt"):
        self.filename = filename
        if os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("")

    def log(self, message: str):
        formatted_msg = self.format_message(f"[FILE] {message}")
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(formatted_msg + "\n")
        print(f"Файлға жазылды: {message}")

def run_task3():
    print("--- ТАПСЫРМА 3: LOGGER ИШІНАРА АБСТРАКЦИЯСЫ ---")
    console_log = ConsoleLogger()
    file_log = FileLogger()

    console_log.log("Жүйе іске қосылды.")
    file_log.log("Қате анықталды: 404.")

    print(f"\n[{file_log.filename} файлының мазмұны]:")
    try:
        with open(file_log.filename, 'r', encoding='utf-8') as f:
            print(f.read().strip())
    except FileNotFoundError:
        pass
    print("-" * 50)

class Airplane(Vehicle):
    def move(self): return "-> Airplane: Әуеде ұшады."

    def fuel_type(self): return "-> Airplane: Авиациялық керосинді пайдаланады."


class Train(Vehicle):
    def move(self): return "-> Train: Рельстермен жүреді."

    def fuel_type(self): return "-> Train: Дизель немесе электр қуатын пайдаланады."


def run_task4():
    print("--- ТАПСЫРМА 4: ПОЛИМОРФИЗМ ---")
    vehicle_list = [Car(), Bicycle(), Airplane(), Train()]

    for vehicle in vehicle_list:
        print(f"{vehicle.__class__.__name__}: {vehicle.move()}")

    print("-" * 50)

class PaymentSystem(ABC):
    @abstractmethod
    def authorize(self, amount): pass

    @abstractmethod
    def process(self, amount): pass

    @abstractmethod
    def refund(self, transaction_id): pass


class PayPal(PaymentSystem):
    def authorize(self, amount):
        print(f"-> PayPal: {amount} KZT үшін авторизация сұралды.")

    def process(self, amount):
        print(f"-> PayPal: {amount} KZT төлемі өңделді.")

    def refund(self, transaction_id):
        print(f"-> PayPal: Транзакция ID {transaction_id} бойынша қайтару жүргізілді.")


class KaspiPay(PaymentSystem):
    def authorize(self, amount):
        print(f"-> KaspiPay: {amount} KZT үшін Kaspi QR арқылы авторизация.")

    def process(self, amount):
        print(f"-> KaspiPay: {amount} KZT төлемі Kaspi арқылы өңделді.")

    def refund(self, transaction_id):
        print(f"-> KaspiPay: Транзакция ID {transaction_id} бойынша қайтару сұранысы қабылданды.")

def run_task5():
    print("--- ТАПСЫРМА 5: PAYMENT SYSTEM ИНТЕРФЕЙСІ ---")

    paypal_processor = PayPal()
    kaspi_processor = KaspiPay()

    amount = 5500
    txn_id = "TXN_987654"

    print("\n[PayPal әрекеттері]:")
    paypal_processor.authorize(amount)
    paypal_processor.process(amount)
    paypal_processor.refund(txn_id)

    print("\n[KaspiPay әрекеттері]:")
    kaspi_processor.authorize(amount)
    kaspi_processor.process(amount)
    kaspi_processor.refund(txn_id)

    print("-" * 50)
if __name__ == "__main__":
    run_task1()
    print("\n")
    run_task2()
    print("\n")
    run_task3()
    print("\n")
    run_task4()
    print("\n")
    run_task5()