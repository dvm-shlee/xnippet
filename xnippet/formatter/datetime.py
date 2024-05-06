from __future__ import annotations
import datetime as dt
import re
import warnings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union


class DateTime:
    @staticmethod
    def string_to_datetime(datetime_str):
        """Convert a datetime string into separate date and time objects.

        Args:
            datetime_str (str): The datetime string to convert. Supports two patterns:
                1. "HH:MM:SS dd Mon YYYY" (e.g., "12:34:56 1 Jan 2021")
                2. "YYYY-MM-DDTHH:MM:SS" (e.g., "2021-01-01T12:34:56")

        Returns:
            tuple or None: A tuple containing a `datetime.date` and `datetime.time` object if successful, or None if no matching pattern is found.
        """
        ptrns = [r'(\d{2}:\d{2}:\d{2})\s+(\d+\s\w+\s\d{4})',
                r'(\d{4}-\d{2}-\d{2})[T](\d{2}:\d{2}:\d{2})']
        matched = {i: re.match(p, datetime_str) for i, p in enumerate(ptrns) if re.match(p, datetime_str)}
        if matched:
            idx, _ = matched.popitem()
            date = dt.datetime.strptime(re.sub(ptrns[idx], r'\2', datetime_str), '%d %b %Y').date()
            time = dt.time(*map(int, re.sub(ptrns[idx], r'\1', datetime_str).split(':')))
            return date, time
        warnings.warn(f"Cannot find a matching pattern for the provided datetime string: {datetime_str}")
        return None

    @staticmethod
    def unix_timestanp_to_datetime(unix_timestamp: Union[str, int]):
        return dt.datetime.fromtimestamp(unix_timestamp)



