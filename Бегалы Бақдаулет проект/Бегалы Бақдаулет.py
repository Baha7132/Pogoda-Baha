from datetime import date, timedelta
import uuid


class Vehicle:
    def __init__(self, model, year, base_daily_rate):
        self.id = uuid.uuid4()
        self.model = model
        self.year = year
        self.base_daily_rate = base_daily_rate
        self.is_available = True

    def calculate_daily_price(self):
        return self.base_daily_rate

    def __str__(self):
        return f"{self.model} ({self.year}) | Rate: {self.base_daily_rate} | Available: {self.is_available}"


class Car(Vehicle):
    def __init__(self, model, year, rate, category="Economy"):
        super().__init__(model, year, rate)
        self.category = category

    def calculate_daily_price(self):
        if self.category == "Economy":
            multiplier = 1.0
        elif self.category == "SUV":
            multiplier = 1.3
        elif self.category == "Premium":
            multiplier = 1.5
        else:
            multiplier = 1.0

        return self.base_daily_rate * multiplier

    def __str__(self):
        return super().__str__() + f" | Category: {self.category}"


class Customer:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.id})"


class Tariff:
    def __init__(self, name, multiplier):
        self.name = name
        self.multiplier = multiplier


class Insurance:
    def __init__(self, name, daily_cost):
        self.name = name
        self.daily_cost = daily_cost


class Rental:
    def __init__(self, customer, vehicle, start, end, tariff, insurance):
        self.id = uuid.uuid4()
        self.customer = customer
        self.vehicle = vehicle
        self.start = start
        self.end = end
        self.tariff = tariff
        self.insurance = insurance
        self.active = True

        vehicle.is_available = False
        self.price = self.calculate_price()

    def calculate_price(self):
        days = (self.end - self.start).days + 1
        daily_price = self.vehicle.calculate_daily_price() * self.tariff.multiplier
        return daily_price * days + self.insurance.daily_cost * days

    def complete(self):
        self.active = False
        self.vehicle.is_available = True

    def __str__(self):
        return f"Rental {self.id}: {self.customer.name} -> {self.vehicle.model} | Price: {self.price} | Active: {self.active}"


class RentalManager:
    _instance = None

    def __init__(self):
        self.rentals = []

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_rental(self, customer, vehicle, start, end, tariff, insurance):
        if not vehicle.is_available:
            raise Exception("Vehicle is not available")

        rental = Rental(customer, vehicle, start, end, tariff, insurance)
        self.rentals.append(rental)
        return rental

    def active_rentals(self):
        return [r for r in self.rentals if r.active]

    def all_rentals(self):
        return self.rentals

    def complete_rental(self, rental_id):
        for r in self.rentals:
            if r.id == rental_id:
                r.complete()
                break


def main():
    car1 = Car("Toyota Camry", 2020, 50, "Economy")
    car2 = Car("BMW X5", 2022, 120, "SUV")

    cus1 = Customer("Axi")
    cus2 = Customer("Bektas")

    standard = Tariff("Standard", 1.0)
    weekend = Tariff("Weekend", 0.9)

    basic_ins = Insurance("Basic", 5)
    full_ins = Insurance("Full", 15)

    manager = RentalManager.instance()

    r1 = manager.create_rental(
        cus1, car1, date.today(), date.today() + timedelta(days=2), standard, basic_ins
    )
    r2 = manager.create_rental(
        cus2, car2, date.today(), date.today() + timedelta(days=4), weekend, full_ins
    )

    for r in manager.active_rentals():
        print(r)

    manager.complete_rental(r1.id)

    print("\nAfter completion:\n")
    for r in manager.all_rentals():
        print(r)


if __name__ == "__main__":
    main()
