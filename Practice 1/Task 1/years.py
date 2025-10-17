"""
Write a function that tells us if the given input is a leap-year or not.
Read the years from a file.
Definition of a leap-year: A year is a leap year if it's divisible by 4, unless it is also divisible by 100.
The only exception is if it's divisible by 400. Then it's a leap year again :)
 Examples:
Leap-year: 1992, 1996, 2000, 2400
Not leap-year: 1993, 1900
"""


def is_leap_year_dumb(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True
    return False


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def check_leap_years_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    year = int(line.strip())
                    result = is_leap_year(year)
                    print(f"{year} is {'a leap year' if result else 'not a leap year'}")
                except ValueError:
                    print(f"Invalid year in file: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error reading file: {e}")


if __name__ == "__main__":
    check_leap_years_from_file("years.txt")
