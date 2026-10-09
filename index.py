def task_1():
    countries = {"Україна", "Польща", "Німеччина", "Франція", "Італія"}

    while True:
        print("\nКраїни:", ", ".join(sorted(countries)))
        print("1. Додати країну")
        print("2. Видалити країну")
        print("3. Знайти країни за символами")
        print("4. Перевірити наявність країни")
        print("0. Повернутися до вибору завдання")
        choice = input("Ваш вибір: ").strip()

        if choice == "0":
            break

        if choice not in {"1", "2", "3", "4"}:
            print("Невірний вибір.")
            continue

        text = input("Введіть назву країни або символи для пошуку: ").strip()

        if not text:
            print("Введення не може бути порожнім.")
            continue

        if choice == "1":
            if text in countries:
                print("Країна вже є в множині.")
            else:
                countries.add(text)
                print("Країну додано.")
        elif choice == "2":
            if text in countries:
                countries.remove(text)
                print("Країну видалено.")
            else:
                print("Країну не знайдено.")
        elif choice == "3":
            found = sorted(country for country in countries if text.casefold() in country.casefold())
            print("Знайдені країни:", ", ".join(found) if found else "Нічого не знайдено.")
        elif choice == "4":
            print("Країна є в множині." if text in countries else "Країни немає в множині.")


def task_2():
    cities_1 = {"Київ", "Львів", "Одеса", "Харків"}
    cities_2 = {"Львів", "Одеса", "Дніпро", "Полтава"}
    cities_3 = cities_1 & cities_2

    print("\nПерша множина міст:", sorted(cities_1))
    print("Друга множина міст:", sorted(cities_2))
    print("Міста, які є в обох множинах:", sorted(cities_3))


def task_3():
    cities_1 = {"Київ", "Львів", "Одеса", "Харків"}
    cities_2 = {"Львів", "Одеса", "Дніпро", "Полтава"}
    cities_3 = cities_1 - cities_2

    print("\nПерша множина міст:", sorted(cities_1))
    print("Друга множина міст:", sorted(cities_2))
    print("Міста, які є лише в першій множині:", sorted(cities_3))


def task_6():
    capitals = {
        "Україна": "Київ",
        "Польща": "Варшава",
        "Німеччина": "Берлін",
        "Франція": "Париж",
        "Італія": "Рим",
    }

    while True:
        print("\nКраїни та столиці:")
        for country, capital in sorted(capitals.items()):
            print(f"{country}: {capital}")

        print("1. Додати країну та столицю")
        print("2. Видалити країну та столицю")
        print("3. Знайти столицю країни")
        print("4. Замінити столицю країни")
        print("0. Повернутися до вибору завдання")
        choice = input("Ваш вибір: ").strip()

        if choice == "0":
            break

        if choice not in {"1", "2", "3", "4"}:
            print("Невірний вибір.")
            continue

        country = input("Введіть назву країни: ").strip()

        if not country:
            print("Назва країни не може бути порожньою.")
            continue

        if choice == "1":
            if country in capitals:
                print("Країна вже є в словнику.")
            else:
                capital = input("Введіть назву столиці: ").strip()
                if capital:
                    capitals[country] = capital
                    print("Країну та столицю додано.")
                else:
                    print("Назва столиці не може бути порожньою.")
        elif country not in capitals:
            print("Країну не знайдено.")
        elif choice == "2":
            del capitals[country]
            print("Країну та столицю видалено.")
        elif choice == "3":
            print(f"Столиця країни {country}: {capitals[country]}")
        elif choice == "4":
            capital = input("Введіть нову назву столиці: ").strip()
            if capital:
                capitals[country] = capital
                print("Столицю замінено.")
            else:
                print("Назва столиці не може бути порожньою.")


def main():
    while True:
        print("\n1. Множина країн")
        print("2. Спільні міста двох множин")
        print("3. Міста лише з першої множини")
        print("6. Словник країн та столиць")
        print("0. Вихід")
        choice = input("Виберіть завдання: ").strip()

        if choice == "1":
            task_1()
        elif choice == "2":
            task_2()
        elif choice == "3":
            task_3()
        elif choice == "6":
            task_6()
        elif choice == "0":
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()
