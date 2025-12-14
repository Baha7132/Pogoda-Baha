
import csv
import json
from pathlib import Path



def text_file_example():
    print("\n=== TEXT FILE EXAMPLE ===")
    path = Path("example_text.txt")

    path.write_text("Hello, this is a text file!\nSecond line.", encoding="utf-8")

    content = path.read_text(encoding="utf-8")
    print("Файлдың ішіндегі мәтін:")
    print(content)


def csv_example():
    print("\n=== CSV EXAMPLE ===")
    path = Path("people.csv")

    rows = [
        {"name": "Alice", "age": 25, "city": "Astana"},
        {"name": "Bob", "age": 30, "city": "Almaty"},
        {"name": "Carol", "age": 22, "city": "Shymkent"},
    ]

    # CSV жазу
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
        writer.writeheader()
        writer.writerows(rows)

    # CSV оқу
    print("CSV файл içindegi malimet:")
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)



def json_example():
    print("\n=== JSON EXAMPLE ===")
    path = Path("config.json")

    data = {
        "app": "DemoProgram",
        "version": 1.0,
        "debug": True,
        "languages": ["kk", "ru", "en"]
    }


    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


    with path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)

    print("JSON içindegi malimet:")
    print(loaded)



def exception_example():
    print("\n=== EXCEPTION EXAMPLE ===")

    def divide(a, b):
        return a / b

    test_cases = [(10, 2), (10, 0), (10, -5)]

    for a, b in test_cases:
        try:
            result = divide(a, b)
            print(f"{a} / {b} = {result}")
        except ZeroDivisionError:
            print(f"Қате: {a} / {b} — 0-ге бөлуге болмайды!")
        except Exception as e:
            print(f"Басқа қате пайда болды: {e}")

class SafeWriter:

    def __init__(self, path):
        self.path = Path(path)
        self.temp = Path(str(path) + ".tmp")

    def __enter__(self):
        self.file = self.temp.open("w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc, tb):
        self.file.close()
        if exc_type is None:
            self.temp.replace(self.path)
        else:
            self.temp.unlink(missing_ok=True)
            print("Жазу кезінде қате шықты. Файл бүлінген жоқ.")
        return False


def context_manager_example():
    print("\n=== CONTEXT MANAGER EXAMPLE ===")

    with SafeWriter("safe_output.txt") as f:
        f.write("Бұл қауіпсіз жазылған мәтін.\n")
        f.write("Файл толық аяқталған соң ғана сақталады!")

    print("safe_output.txt файлы сәтті жасалды!")



def main():
    print("=== DEMO PROGRAM STARTED ===")

    text_file_example()
    csv_example()
    json_example()
    exception_example()
    context_manager_example()

    print("\n=== ALL EXAMPLES FINISHED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()
