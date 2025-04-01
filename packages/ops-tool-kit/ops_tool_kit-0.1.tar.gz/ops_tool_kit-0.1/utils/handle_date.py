from datetime import datetime, timedelta


class HandleDate:

    def format_date(self, date: datetime, date_type):
        if date_type == "weekly":
            date_format = self.get_ww(date)
        elif date_type == "monthly":
            date_format = date.strftime("%Y") + "_" + date.strftime("%m")
        elif date_type == "yearly":
            date_format = date.strftime("%Y")
        elif date_type == "hourly":
            date_format = date.strftime("%Y-%m-%d")
        elif date_type == "quarterly":
            date_format = date.strftime('%Y') + "Q" + str((int(date.strftime('%m')) - 1) // 3 + 1)
        else:
            date_format = date.strftime("%Y-%m-%d")
        # print(date_format)
        return date_format

    @staticmethod
    def get_ww(date: datetime):
        year, week_number, week_day = date.isocalendar()
        # print(year, week_number, week_day)
        if week_day == 7:
            year, week_number, _ = (date + timedelta(days=1)).isocalendar()
        return f"{year}WW{week_number:02}"


if __name__ == '__main__':
    now = datetime.now()
    handle_time = HandleDate()
    res = handle_time.get_ww(now)
    print(res)
    res = handle_time.format_date(now, 'quarterly')
    print(res)
