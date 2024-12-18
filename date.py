import datetime
import calendar

class Date():
    def __init__(self):
        pass
    
    def enter_datetime(self, spec):
        print("Please enter {} time for recording".format(spec))
        today = datetime.datetime.now()
        result = {}
        result["year"] = self.get_year(today=today)
        result["month"] = self.get_month(today=today)
        result["day"] = self.get_day(
            calendar.monthrange(result["year"],result["month"])[1], today
            )
        result["hour"] = self.get_hour()
        result["minutes"] = self.get_minutes()
        result["meridian"] = self.get_meridian()
        return result
    
    
    def get_year(self,today):
        while True:
            result = input(
                "Enter year (default: {}): ".format(today.year)
                ) or today.year
            try:
                int(result)
                if 2100 > int(result) > 2023:
                    return result
                else:
                    print("invalid choice")
            except ValueError as e:
                # if result == "q":
                #     break
                print("invalid choice")
            except IndexError as e:
                print("invalid choice")

    def get_month(self,today):
        while True:
            result = input(
                "Enter month (default: {}): ".format(today.month)
                ) or today.month
            try:
                int(result)
                if 13 > int(result) > 0:
                    return result
                else:
                    print("invalid choice")
            except ValueError as e:
                # if result == "q":
                #     break
                print("invalid choice")
            except IndexError as e:
                print("invalid choice")

    def get_day(self,days, today):
        while True:
            result = input(
                "Enter day (default: {}): ".format(today.day)
                ) or today.day
            try:
                int(result)
                if days+1 > int(result) > 0:
                    return result
                else:
                    print("invalid choice")
            except ValueError as e:
                # if result == "q":
                #     break
                print("invalid choice")
            except IndexError as e:
                print("invalid choice")

    def get_hour(self):
        while True:
            result = input(
                "Enter hour: ")
            try:
                int(result)
                if 13 > int(result) > 0:
                    return result
                else:
                    print("invalid choice")
            except ValueError as e:
                # if result == "q":
                #     break
                print("invalid choice")
            except IndexError as e:
                print("invalid choice")

    def get_minutes(self):
        while True:
            result = input("Enter minutes: ")
            try:
                int(result)
                if 60 > int(result) > -1:
                    return result
                else:
                    print("invalid choice")
            except ValueError as e:
                # if result == "q":
                #     break
                print("invalid choice")
            except IndexError as e:
                print("invalid choice")

    def get_meridian(self):
        while True:
            result = input("Enter AM or PM: ")
            if result.lower() == "am" or result.lower() == "pm":
                return result.upper()
            else:
                print("invalid choice")
