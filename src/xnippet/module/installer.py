from __future__ import annotations
import sys
import subprocess
import warnings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal, Optional


class Installer:
    _cmd: list
    _proc: Optional[subprocess.Popen]
    _mode: Optional[Literal['install', 'uninstall', 'list']]
    _counter: int
    _module: str
    
    def __init__(self):
        self._reset()
    
    def install(self, 
                module_name: Optional[str], 
                version: Optional[str] = None, 
                version_constraint: Literal['==', '!=', '>=', '<='] = "==",
                upgrade: bool = False):
        self._mode = 'install'
        self._module = f"{module_name}{version_constraint}{version}"
        cmd = [sys.executable, "-m", "pip", "install"]
        if upgrade:
            cmd.append("--upgrade")
        cmd.append(self._module)
        self._cmd = cmd
        self._exec()
        self._reset()
    
    def _reset(self):
        self._cmd = [sys.executable, '-m', 'pip']
        self._proc = None
        self._mode = None
        self._module = None
        self._counter = 0
    
    def _exec(self):
        with subprocess.Popen(self._cmd, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              text=True, 
                              bufsize=1, 
                              universal_newlines=True) as proc:
            self._proc = proc
            for line in self._proc.stdout:
                self._line_capture(line)
            proc.wait()
            if self._proc.returncode != 0:
                warnings.warn(f"'Errors during resolving dependencies': {''.join(proc.stderr)}")

    def _line_capture(self, line):
        if self._mode == 'install':
            self._line_case_install(line)
            
    def _line_case_install(self, line):
        if 'satisfied' in line.lower():
            if not self._counter:
                print(f" + Required already satisfied: {self._module}")
            self._counter += 1
        elif 'collecting' in line.lower():
            if not self._counter:
                print(f" + Installing '{self._module}' to resolve dependencies.")
            self._counter += 1
