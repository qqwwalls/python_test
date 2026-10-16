class MyIntArray:
    def __init__(self, values):
        values = list(values)
        for value in values:
            if type(value) is not int:
                raise TypeError("Масив має містити лише цілі числа.")
        self.__values = values

    def __str__(self):
        return "\n".join(f"{index}: {value}" for index, value in enumerate(self.__values))

    def __add__(self, other):
        if isinstance(other, MyIntArray):
            if len(self.__values) != len(other.__values):
                raise ValueError("Масиви повинні мати однаковий розмір.")
            for index in range(len(self.__values)):
                self.__values[index] += other.__values[index]
        elif type(other) is int:
            for index in range(len(self.__values)):
                self.__values[index] += other
        else:
            return NotImplemented
        return self

    def __mul__(self, other):
        if isinstance(other, MyIntArray):
            if len(self.__values) != len(other.__values):
                raise ValueError("Масиви повинні мати однаковий розмір.")
            for index in range(len(self.__values)):
                self.__values[index] *= other.__values[index]
        elif type(other) is int:
            for index in range(len(self.__values)):
                self.__values[index] *= other
        else:
            return NotImplemented
        return self

    def __eq__(self, other):
        if isinstance(other, MyIntArray):
            return self.__values == other.__values
        return NotImplemented


if __name__ == "__main__":
    arr1 = MyIntArray([1, 2, 3])
    arr2 = MyIntArray([4, 5, 6])

    print("Додавання масивів:")
    print(arr1 + arr2)
    print("Додавання числа:")
    print(arr1 + 2)
    print("Множення масивів:")
    print(arr1 * arr2)
    print("Множення на число:")
    print(arr1 * 2)
    print("Порівняння різних масивів:", arr1 == arr2)
    print("Порівняння однакових масивів:", arr1 == MyIntArray([56, 90, 132]))
