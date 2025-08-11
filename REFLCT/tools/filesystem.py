import os
import time
from typing import Dict, List

def list_files(directory: str = ".", include_hidden: bool = True) -> Dict:
    """List files and directories in a given folder."""
    try:
        entries = os.listdir(directory)
        if not include_hidden:
            entries = [e for e in entries if not e.startswith(".")]
        return {"ok": True, "files": entries}
    except Exception as e:
        return {"ok": False, "error": str(e), "files": []}

def read_file(path: str, encoding: str = "utf-8") -> Dict:
    """Read the entire contents of a text file."""
    try:
        with open(path, "r", encoding=encoding) as f:
            return {"ok": True, "text": f.read()}
    except Exception as e:
        return {"ok": False, "error": str(e), "text": ""}

def head_file(path: str, n: int = 10, encoding: str = "utf-8") -> Dict:
    """Read the first n lines of a text file."""
    try:
        with open(path, "r", encoding=encoding) as f:
            lines = [next(f).rstrip("\n") for _ in range(n)]
        return {"ok": True, "lines": lines}
    except StopIteration:
        return {"ok": True, "lines": lines}
    except Exception as e:
        return {"ok": False, "error": str(e), "lines": []}

def file_info(path: str) -> Dict:
    """Get metadata about a file or directory."""
    try:
        stat = os.stat(path)
        return {
            "ok": True,
            "size_bytes": stat.st_size,
            "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime)),
            "is_file": os.path.isfile(path),
            "is_dir": os.path.isdir(path)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
