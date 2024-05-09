from pathlib import Path as _Path


class Path:
    def _resolve(self, path: _Path):
        return _Path(path).expanduser().resolve()