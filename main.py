import numpy_financial as npf

from datetime import date, timedelta
from itertools import zip_longest
from investments import investments
from installments import installments

cashflow = {}


def get_dates() -> {}:
    """
    This method will query through both investments and installments lists
    and get the intial and the final date
    """
    initial_date = date.max
    final_date = date.min

    for investment, installment in zip_longest(investments, installments,
                                               fillvalue=False):

        if investment:
            current_date = get_current_date(investment["created_at"])

            if current_date < initial_date:
                initial_date = current_date
            if current_date > final_date:
                final_date = current_date

        if installment:
            current_date = get_current_date(installment["due_date"])

            if current_date > final_date:
                final_date = current_date

    return {
        "initial_date": initial_date,
        "final_date": final_date
    }


def get_current_date(received_date: str) -> date:
    """Sets the str date received as a datetime.date"""
    year = int(received_date.split("-")[0])
    month = int(received_date.split("-")[1])
    day = int(received_date.split("-")[2])

    current_date = date(year, month, day)

    return current_date


def initiate_cashflow(initial_date: date, final_date: date) -> None:
    """Will set 0.0 value to every day between initial and final date"""

    current_date = initial_date

    while current_date <= final_date:
        cashflow[str(current_date)] = 0.0
        current_date += timedelta(days=1)


def set_cashflow() -> None:
    """
    Will query through both investments and installments lists, and set the
    amount values to the correct date
    """

    for investment, installment in zip_longest(investments, installments,
                                               fillvalue=False):

        if investment:
            if investment["created_at"] in cashflow:
                cashflow[investment["created_at"]] -= \
                    float(investment["amount"])

        if installment:
            if installment["due_date"] in cashflow:
                cashflow[installment["due_date"]] += \
                    float(installment["amount"])


def calculate_irr() -> float:
    """Gets all cashflow and calculates the IRR"""
    data = []
    for amount in cashflow.values():
        data.append(amount)

    irr = round(npf.irr(data), 4)

    return irr


def get_invested_value() -> float:
    """Calculate all value invested"""
    invested_value = 0.0
    for amount in cashflow.values():
        if amount < 0:
            invested_value -= amount

    return invested_value


def get_returned_value() -> float:
    """Calculate all value returned"""
    returned_value = 0.0
    for amount in cashflow.values():
        if amount > 0:
            returned_value += amount

    return round(returned_value, 2)


def get_profit_percentage(invested_value: float, profit: float) -> str:
    """Calculates the percentage of the profit"""
    profit_percentage = round((profit * 100) / invested_value, 2)

    return f"{profit_percentage}%"


def set_extract(irr: float, invested_value: float, returned_value: float,
                profit: float, profit_percentage: str) -> str:
    """Builds an extract with all relevant information"""
    extract = f"""
        IRR: {irr}
        
        INVESTED VALUE: ${invested_value}
        RETURNED VALUE: ${returned_value}
        PROFIT: ${profit} ({profit_percentage})
        CASHFLOW DAYS: {len(cashflow)}
    """

    return extract


def main() -> None:
    dates = get_dates()
    initial_date = dates["initial_date"]
    final_date = dates["final_date"]

    initiate_cashflow(initial_date, final_date)
    set_cashflow()

    irr = calculate_irr()

    invested_value = get_invested_value()
    retuned_value = get_returned_value()

    profit = round(retuned_value - invested_value, 2)
    profit_percentage = get_profit_percentage(invested_value, profit)

    extract = set_extract(irr, invested_value, retuned_value, profit,
                          profit_percentage)

    print(extract)


if __name__ == "__main__":
    main()
