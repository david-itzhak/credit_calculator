from math import ceil, log, floor
import argparse

choices_list = ["annuity", "diff"]

parser = argparse.ArgumentParser()

parser.add_argument("--type", choices=choices_list, help="Incorrect parameters")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--payment")

args = parser.parse_args()
args_list = [args.type, args.principal, args.periods, args.interest, args.payment]
numeric_args = args_list[2:]

# count_none_numeric_args = 0
# for x in numeric_args:
#     if x is None:
#         count_none_numeric_args += 1
#
# if count_none_numeric_args > 1:
#     print("Incorrect parameters")
#     pass


loan_principal = None
monthly_payment = None
months_number = None
loan_interest = None
total_payment = 0
overpayment = 0

pyment_type = args.type
if args.principal is not None:
    loan_principal = float(args.principal)
if args.payment is not None:
    monthly_payment = float(args.payment)
if args.periods is not None:
    months_number = int(args.periods)
if args.interest is not None:
    loan_interest = float(args.interest)


def set_digital_value(message, min_value):
    while True:
        digital_str = input(f"{message}:\n")
        if digital_str.replace('.', '', 1).isnumeric():
            digital = float(digital_str)
        else:
            continue
        if digital < min_value:
            continue
        else:
            return digital


def set_loan_principal():
    global loan_principal
    loan_principal = set_digital_value("Enter the loan principal", 1)


def set_monthly_payment():
    global monthly_payment
    monthly_payment = set_digital_value("Enter the monthly payment", 1)


def set_annuity_payment():
    global monthly_payment
    monthly_payment = set_digital_value("Enter the annuity payment", 1)


def set_loan_interest():
    global loan_interest
    loan_interest = set_digital_value("Enter the loan interest", 0)


def set_months_number():
    global months_number
    months_number = set_digital_value("Enter the number of periods", 1)


def calculate_month():
    global months_number
    global overpayment
    interest_in_month = loan_interest / 1200
    months_number = ceil(log(monthly_payment / (monthly_payment - interest_in_month * loan_principal), 1 + interest_in_month))
    overpayment = round(monthly_payment * months_number - loan_principal)


def calculate_payment():
    global monthly_payment
    global overpayment
    interest_in_month = loan_interest / 1200
    monthly_payment = ceil(loan_principal * (interest_in_month * pow((1 + interest_in_month), months_number)) / (pow((1 + interest_in_month), months_number) - 1))
    overpayment = round(monthly_payment * months_number - loan_principal)


def calculate_loan_principal():
    global loan_principal
    global overpayment
    interest_in_month = loan_interest / 1200
    loan_principal = floor(monthly_payment / ((interest_in_month * pow((1 + interest_in_month), months_number)) / (pow((1 + interest_in_month), months_number) - 1)))
    overpayment = round(monthly_payment * months_number - loan_principal)


def get_calculation_type():
    if monthly_payment is None:
        return "a"
    if loan_principal is None:
        return "p"
    if months_number is None:
        return "n"


def calculate_differentiated_payments():
    global overpayment
    differentiated_payments = {}
    interest_in_month = loan_interest / 1200
    for x in range(1, months_number + 1):
        current_monthly_payment = loan_principal / months_number + interest_in_month * (loan_principal - loan_principal * (x - 1) / months_number)
        differentiated_payments[x] = ceil(current_monthly_payment)
    overpayment = round(sum(differentiated_payments.values()) - loan_principal)
    return differentiated_payments


def calculate():
    if pyment_type == "diff":
        payments_list = calculate_differentiated_payments()
        for month_number, payment in payments_list.items():
            print(f"Month {month_number}: payment is {payment}")
        print(f"\nOverpayment = {overpayment}")
    if pyment_type == "annuity":
        calculation_type = get_calculation_type()
        if calculation_type == "n":
            calculate_month()
            years = months_number // 12
            month = months_number % 12
            print(f"It will take {years if years > 0 else ''}{' year' if years > 0 else ''}{'s' if years > 1 else ''}{' and ' if years > 0 and month > 0 else ''}{month if month > 0 else ''}{' month' if month > 0 else ''}{'s' if months_number > 1 else ''} to repay this loan!")
            print(f"Overpayment = {overpayment}")
        if calculation_type == "a":
            calculate_payment()
            print(f"Your annuity payment = {monthly_payment}!")
            print(f"Overpayment = {overpayment}")
        if calculation_type == "p":
            calculate_loan_principal()
            print(f"Your loan principal = {loan_principal}!")
            print(f"Overpayment = {overpayment}")


def check_arguments():
    if pyment_type not in choices_list:
        return False
    if loan_interest is None:
        return False
    if pyment_type == "diff" and monthly_payment is not None:
        return False
    if len(numeric_args) > 3:
        return False
    return True


def main():
    is_arguments_valid = check_arguments()
    if is_arguments_valid:
        calculate()
    else:
        print("Incorrect parameters")


if __name__ == "__main__":
    main()
