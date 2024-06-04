"""
    :Date: 2024-5-28
    :Author: linshukai
    :Description: about arithmetic formatter(算术格式化程序)
"""


def arithmetic_arranger(problems, show_answers=False):
    if len(problems) > 5:
        return "Error: Too many problems."

    first_column = []
    second_column = []
    third_column = []
    result_column = []
    for problem in problems:
        tmp_list = problem.split()
        number1 = tmp_list[0]
        symbol = tmp_list[1]
        number2 = tmp_list[2]

        print(number1, number1.isdigit(), number2, number2.isdigit())
        if not number1.isdigit() or not number2.isdigit():
            return "Error: Numbers must only contain digits."

        if len(number1) > 4 or len(number2) > 4:
            return "Error: Numbers cannot be more than four digits."
        if symbol not in "+-":
            return "Error: Operator must be '+' or '-'."

        max_length = len(number1) if len(number1) > len(number2) else len(number2)
        max_length += 2

        first_column.append((max_length - len(number1)) * " " + number1)
        second_column.append(symbol + (max_length - 1 - len(number2)) * " " + number2)
        third_column.append(max_length * "-")

        result = 0
        if symbol == "+":
            result = int(number1) + int(number2)
        elif symbol == "-":
            result = int(number1) - int(number2)
        result_column.append((max_length - len(str(result))) * " " + str(result))

    output = []
    for i in [first_column, second_column, third_column, result_column]:
        output.append("    ".join(i))

    if show_answers:
        return "\n".join(output)
    else:
        return "\n".join(output[:-1])


if __name__ == "__main__":
    result = arithmetic_arranger(["3801 - 2", "123 + 49"])
    print(result)

    result = arithmetic_arranger(["98 + 3g5", "3801 - 2", "45 + 43", "123 + 49"])
    print(result)
