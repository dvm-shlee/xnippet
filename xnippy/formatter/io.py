from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class IO:
    @staticmethod
    def yes_or_no(question):
        while True:
            reply = str(input(question + ' (y/n): ')).lower().strip()
            if reply[:1] == 'y':
                return True
            elif reply[:1] == 'n':
                return False
            else:
                print('  The answer is invalid!')

    @staticmethod
    def print_internal_error(io_handler=None):
        import traceback
        import sys
        if io_handler is None:
            io_handler = sys.stderr
        traceback.print_exception(*sys.exc_info(),
                                file=io_handler)