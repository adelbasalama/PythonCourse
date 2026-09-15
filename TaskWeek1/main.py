from math import pi


# Task 1
def calculate_area_of_circle():
    r = float(input("Input the radius of the circle : "))
    print("The area of the circle with radius " + str(r) + " is: " + str(round(pi * r ** 2, 2)))


# Task 2
def declare_variable():
    number = 10
    decimal_number = 10.5
    text = "Hello, World!"
    boolean = True

    print("Declared Variables:\n"
          "integer number: "
          + str(number)
          + " (" + str(type(number).__name__) + " type)\n"
                                                "decimal number: "
          + str(decimal_number)
          + " (" + str(type(decimal_number).__name__) + " type)\n"
                                                        "text: "
          + str(text)
          + " (" + str(type(text).__name__) + " type)\n"
                                              "boolean: "
          + str(boolean)
          + " (" + str(type(boolean).__name__) + " type)\n")


# Task 3
def cnvert_data_type():
    data = int(input("Input an int data: "))
    to_float = float(data)
    to_string = str(data)
    to_bool = bool(data)
    print("data: " + str(data) + " -> " + str(to_float) + " ( " + str(type(data).__name__) + " -> " + str(
        type(to_float).__name__) + " )\n" + "data: " + str(data) + " -> " + str(to_string) + " ( " + str(
        type(data).__name__) + " -> " + str(
        type(to_string).__name__) + " )\n" "data: " + str(data) + " -> " + str(to_bool) + " ( " + str(
        type(data).__name__) + " -> " + str(
        type(to_bool).__name__) + " )\n")

    data = float(input("Input a float data: "))
    to_int = int(data)
    print("data: " + str(data) + " -> " + str(to_int) + " ( " + str(type(data).__name__) + " -> " + str(
        type(to_int).__name__) + " )\n")

    data = str(input("Input a string data: "))
    if data.isdigit():
        to_int = int(data)
        print("data: " + str(data) + " -> " + str(to_int) + " ( " + str(type(data).__name__) + " -> " + str(
            type(to_int).__name__) + " )\n")


# Task 4
def calculate_factorial(number):
    if number > 1:
        return number * calculate_factorial(number - 1)

    return number


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # calculate_area_of_circle()
    # declare_variable()
    # cnvert_data_type()

    number = int(input("Input a number: "))
    result = calculate_factorial(number)
    print("The factorial of " + str(number) + " is: " + str(result))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
