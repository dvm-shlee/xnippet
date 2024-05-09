from __future__ import annotations
import os
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class Bytes:
    @staticmethod
    def convert_unit(size_in_bytes, unit):
        """ Convert the size from bytes to other units like KB, MB or GB"""
        size = float(size_in_bytes)
        if unit == 1:
            return size / 1024
        elif unit == 2:
            return size / (1024 * 1024)
        elif unit == 3:
            return size / (1024 * 1024 * 1024)
        elif unit == 4:
            return size / (1024**unit)
        else:
            return int(size)

    @staticmethod
    def get_dirsize(dir_path):
        unit_dict = {0: 'B',
                    1: 'KB',
                    2: 'MB',
                    3: 'GB',
                    4: 'TB'}
        dir_size = 0
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                fp = os.path.join(root, f)
                if not os.path.islink(fp):
                    dir_size += os.path.getsize(fp)

        unit = int(len(str(dir_size)) / 3)
        return Bytes.convert_unit(dir_size, unit), unit_dict[unit]

    @staticmethod
    def get_filesize(file_path):
        unit_dict = {0: 'B',
                    1: 'KB',
                    2: 'MB',
                    3: 'GB'}
        file_size = os.path.getsize(file_path)

        unit = int(len(str(file_size)) / 3)
        return Bytes.convert_unit(file_size, unit), unit_dict[unit]
