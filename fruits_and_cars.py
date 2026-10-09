fruits = (
    "яблуко",
    "банан",
    "апельсин",
    "яблуко",
    "груша",
    "банан",
    "яблуко",
)

fruit_name = input("Введіть назву фрукта: ").strip()
fruit_count = fruits.count(fruit_name)
print(f"Кількість фруктів '{fruit_name}' у кортежі: {fruit_count}")

manufacturers = [
    "Toyota",
    "BMW",
    "Ford",
    "Toyota",
    "Audi",
    "BMW",
    "Tesla",
    "Toyota",
]

print("Початковий список автовиробників:", manufacturers)

manufacturer_name = input("Введіть назву автовиробника: ").strip()
replacement_word = input("Введіть слово для заміни: ").strip()

for index in range(len(manufacturers)):
    if manufacturers[index] == manufacturer_name:
        manufacturers[index] = replacement_word

print("Оновлений список автовиробників:", manufacturers)
