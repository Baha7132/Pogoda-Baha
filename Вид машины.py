
class LowStockError(Exception):

    pass


class Car:

    def __init__(self, brand, model, year, price):
        self.brand = brand  # Маркасы (Мысалы: Toyota)
        self.model = model  # Моделі (Мысалы: Camry)
        self.year = year  # Шығарылған жылы
        self.price = price  # Бағасы (integer)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} - {self.price} KZT"


class Dealership:

    def __init__(self, name="Luxury Motors"):
        self.name = name

        self.inventory = {}

    def add_car_to_stock(self, car_object, quantity):
        if quantity <= 0:
            print("❗ Қате: Қосу үшін мөлшер оң сан болуы керек.")
            return

        if car_object in self.inventory:
            self.inventory[car_object] += quantity
            print(
                f"✅ Қойма жаңартылды: {car_object.brand} {car_object.model} +{quantity} дана. Жалпы: {self.inventory[car_object]}")
        else:
            self.inventory[car_object] = quantity
            print(f"✅ Жаңа көлік қосылды: {car_object.brand} {car_object.model}, {quantity} дана.")

    def sell_car(self, car_object, quantity):
        """Көлікті сатады және қоймадан алып тастайды, ерекше жағдайларды өңдейді."""
        print(f"\n--- Сату операциясы: {car_object.brand} {car_object.model} ({quantity} дана) ---")
        try:
            # 1. Көліктің қоймада бар-жоғын тексеру
            if car_object not in self.inventory:
                raise LowStockError("❌ Сату мүмкін емес: Бұл көлік қоймада жоқ.")

            current_stock = self.inventory[car_object]

            # 2. Сату мөлшерінің қоймадағы мөлшерден аз-көбін тексеру
            if current_stock < quantity:
                # Арнайы қатені шығару
                raise LowStockError(
                    f"❌ Сату мүмкін емес: Қоймада тек {current_stock} дана бар, сұралғаны {quantity} дана.")

            # 3. Сату сәтті болса
            self.inventory[car_object] -= quantity
            total_price = car_object.price * quantity

            print(f"🎉 Сәтті сатылды! {quantity} дана {car_object.brand} {car_object.model}.")
            print(f"💰 Жалпы сома: {total_price} KZT.")

            # Егер қоймадағы сан 0 болса, көлікті сөздіктен алып тастау
            if self.inventory[car_object] == 0:
                del self.inventory[car_object]
                print(f"❕ Ескерту: {car_object.model} моделінің қоры таусылды.")

        except LowStockError as e:
            # LowStockError ерекшелігін өңдеу
            print(f"❗ Қате (LowStockError): {e}")

        except Exception as e:
            # Басқа күтілмеген қателерді өңдеу
            print(f"❗ Күтілмеген жүйелік қате: {e}")

    def display_inventory(self):
        """Қоймадағы барлық көліктер мен олардың санын шығарады."""
        print(f"\n======================================")
        print(f"🏢 Автосалон қоймасы: {self.name}")
        print(f"======================================")

        if not self.inventory:
            print("Қойма бос.")
            return

        for car, quantity in self.inventory.items():
            print(f"[{quantity} дана] | {car}")

        print(f"======================================\n")




if __name__ == "__main__":
    # 1. Автосалон объектісін құру
    diler = Dealership("Astana Motors LUX")

    # 2. Қоймаға көліктерді қосу (Car объектілерін жасау)
    toyota_camry = Car("Toyota", "Camry 75", 2024, 18_000_000)
    hyundai_elantra = Car("Hyundai", "Elantra", 2023, 11_500_000)
    bmw_x7 = Car("BMW", "X7", 2024, 45_000_000)

    diler.add_car_to_stock(toyota_camry, 5)
    diler.add_car_to_stock(hyundai_elantra, 10)
    diler.add_car_to_stock(bmw_x7, 2)

    # Бар көлікке қосымша көлік қосу
    diler.add_car_to_stock(toyota_camry, 3)

    # 3. Қойманы көрсету
    diler.display_inventory()

    # 4. Сату операцияларын тексеру (Сәтті сату)
    diler.sell_car(hyundai_elantra, 4)  # Сәтті сатылады
    diler.display_inventory()

    # 5. Сату операцияларын тексеру (Қателерді өңдеу)

    # Қате 1: Қоймадағы саннан көп сату (LowStockError)
    diler.sell_car(bmw_x7, 5)  # Қоймада тек 2 дана бар

    # Қате 2: Жоқ көлікті сату (LowStockError)
    audi_a8 = Car("Audi", "A8", 2024, 35_000_000)
    diler.sell_car(audi_a8, 1)  # Audi қоймада жоқ

    # 6. Қалған қойманы көрсету
    diler.display_inventory()