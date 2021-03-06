from datetime import datetime


def datetime_to_iso8601(my_datetime: datetime):
    return my_datetime.strftime("%Y-%m-%dT%H:%M:%S+00")


def iso8601_to_datetime(my_datetime: str):
    return datetime.strptime(my_datetime, "%Y-%m-%dT%H:%M:%S+00")
