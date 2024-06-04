"""
    :Date: 2024-5-30
    :Author: linshukai
    :Description: About Budget APP(预算应用)
"""

import json


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        output = []
        output.append(self.name.center(30, "*"))
        output.append(
            self.cate_format(self.ledger[0]["amount"], self.ledger[0]["description"])
        )
        for i in self.ledger[1:]:
            output.append(self.cate_format(i["amount"], i["description"]))

        output.append(f"Total: {self.get_balance()}")
        return "\n".join(output)

    @staticmethod
    def cate_format(amount, description):
        amount = "%.2f" % amount
        odd = 30 - len(amount)
        space = odd - len(description)

        if space > 0:
            return description + space * " " + amount
        else:
            return description[: odd - 1] + " " + amount

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        return self.check_funds(amount, description)

    def get_balance(self):
        return sum([item["amount"] for item in self.ledger])

    def transfer(self, amount, obj):
        if self.check_funds(amount, f"Transfer to {obj.name}"):
            obj.ledger.append(
                {"amount": amount, "description": f"Transfer from {self.name}"}
            )
            return True
        return False

    def check_funds(self, amount, description=""):
        if amount > self.get_balance():
            return False

        self.ledger.append({"amount": -amount, "description": description})
        return True


def create_spend_chart(categories):
    tmp = {
        i.name: sum([j["amount"] for j in i.ledger if j["amount"] < 0])
        for i in categories
    }
    sum_category = sum([v for v in tmp.values()])

    percentage_spent = []
    for name, v in tmp.items():
        percentage = v / sum_category * 100 // 10
        percentage_spent.append((name, percentage))

    output = [str(x * 10).rjust(3, " ") + "|" for x in range(11)]
    index = len(output) - 1
    while index >= 0:
        for p in percentage_spent:
            if p[1] >= index:
                output[index] += " o "
            else:
                output[index] += "   "
        output[index] += " "
        index -= 1

    output = ["Percentage spent by category"] + output[::-1]
    output.append("    " + len(percentage_spent) * 3 * "-" + "-")

    col = 0
    max_col = max([len(x[0]) for x in percentage_spent])
    while col < max_col:
        row = "     "
        for p in percentage_spent:
            if col < len(p[0]):
                row += p[0][col]
            else:
                row += " "
            row += "  "
        col += 1
        output.append(row)
    return "\n".join(output)


if __name__ == "__main__":
    food = Category("Food")
    entertainment = Category("Entertainment")
    business = Category("Business")

    food.deposit(900, "deposit")
    entertainment.deposit(900, "deposit")
    business.deposit(900, "deposit")
    food.withdraw(105.55)
    entertainment.withdraw(33.40)
    business.withdraw(10.99)
    actual = create_spend_chart([business, food, entertainment])
    print(json.dumps(actual))

    expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "

    print(actual == expected)
    print(json.dumps(expected))
