from __future__ import annotations
import datetime as dt
import re
import warnings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union


class DateTime:
    def __init__(self, dt_string):
        self.tzcode = None
        if isinstance(dt_string, int):
            # unit time only
            self.datetime = self.unix_timestanp_to_datetime(dt_string)
        elif isinstance(dt_string, str):
            # string pattern
            self.datetime = self.string_to_datetime(dt_string)
        else:
            # assume the dt_string is list
            if all(isinstance(e, str) for e in dt_string):
                self.datetime = self.string_to_datetime(dt_string[0])
                self.apply_residuals(dt_string[1])

            elif all(isinstance(e, int) for e in dt_string):
                self.datetime = self.unix_timestanp_to_datetime(dt_string[0])
                self.apply_residuals(''.join(map(str, dt_string[1:])))
           
    def apply_residuals(self, residual_str: str):
        ptrn = r'^(\d{3})([+-]{1})(\d{3,4})$'
        if matched := re.match(ptrn, residual_str):
            ms, side, tz = matched.groups()
            self.datetime.replace(microsecond=int(ms))
            if len(tz) == 3:
                ftz = float(tz)
                tzcode = str(ftz / 60).split('.')[0].zfill(2) + ":" + str(ftz % 60).split('.')[0].zfill(2)
            else:
                tzcode = tz[:2] + ":" + tz[2:]
            self.tzcode = f'{side}{tzcode}'

    def get(self):
        datetime = self.datetime.strftime('%Y-%m-%d %H:%M:%S')
        return f"{datetime} UTC{self.tzcode}" if self.tzcode else datetime 
        
    @staticmethod
    def string_to_datetime(datetime_str: str):
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
            if idx == 0:
                date = dt.datetime.strptime(re.sub(ptrns[idx], r'\2', datetime_str), '%d %b %Y').date()
                time = dt.time(*map(int, re.sub(ptrns[idx], r'\1', datetime_str).split(':')))
            else:
                date = dt.date(*map(int, re.sub(ptrns[idx], r'\1', datetime_str).split('-')))
                time = dt.time(*map(int, re.sub(ptrns[idx], r'\2', datetime_str).split(':')))
            return dt.datetime.combine(date, time)
        warnings.warn(f"Cannot find a matching pattern for the provided datetime string: {datetime_str}")
        return None

    @staticmethod
    def unix_timestanp_to_datetime(unix_timestamp: Union[str, int]):
        return dt.datetime.fromtimestamp(unix_timestamp)



