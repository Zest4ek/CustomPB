""" 
Source: https://github.com/Zest4ek/CustomPB/python_lib/custom_pb.py
Requires: bin/custom_pb.dll
"""
import ctypes
from pathlib import Path


class _C_BAR(ctypes.Structure):
    _fields_ = [
        ("PERCENT", ctypes.c_int),
        ("WIDTH", ctypes.c_int),
        ("FOREGROUND", ctypes.c_char*20),
        ("BACKGROUND", ctypes.c_char*20),
    ]


class Bar:
    def __init__(self, percent: int, width: int, fg: str, bg: str):
        if not 0 <= percent <= 100: raise ValueError("invalid percent value")
        elif not 0 <= width <= 1000: raise ValueError("invalid width value")
        elif len(fg) > 19: raise MemoryError("foreground value is too large")
        elif len(bg) > 19: raise MemoryError("background value is too large")

        self.__bar = _C_BAR(
            PERCENT=percent,
            WIDTH=width,
            FOREGROUND=fg.encode("utf-8"),
            BACKGROUND=bg.encode("utf-8")
        )

    def __str__(self):
        return self.getsmoothbar()

    @property
    def percent(self) -> int: return self.__bar.PERCENT
    
    @percent.setter
    def percent(self, percent: int):
        if 0 <= percent <= 100:
            self.__bar.PERCENT = percent
        else:
            raise ValueError("invalid percent value")

    @property
    def width(self) -> int: return self.__bar.WIDTH
    
    @width.setter
    def width(self, width: int):
        if 0 <= width <= 1000:
            self.__bar.WIDTH = width
        else:
            raise ValueError("invalid width value")


    @property
    def fg(self) -> str: return self.__bar.FOREGROUND.decode("utf-8")

    @fg.setter
    def fg(self, fg: str):
        if len(fg) > 19: raise MemoryError("foreground value is too large")
        elif not fg.startswith("\033[") or not fg.endswith("m"):
            raise ValueError("foreground must be an ANSI-color")
        
        try:
            colstr = fg[2:-1] # throw \033[ and m
            colors = [int(col) for col in colstr.split(';')] # split a string into indexes
        except ValueError:
            raise ValueError("invalid ANSI-color value")

        if colors[0] == 38:
            if len(colors) < 3:
                raise ValueError("invalid non-standard color format (excepted 38;5;N or 38;2;R;G;B)")
            
            elif colors[1] == 2:
                if len(colors) == 5:
                    if chktruecol(colors[2],colors[3],colors[4]): self.fgtruecol(colors[2], colors[3], colors[4])
                    else: raise ValueError("invalid ANSI-color index value")
                else: 
                    raise ValueError("invalid true color format (expected 38;2;R;G;B)")

            elif colors[1] == 5:
                if len(colors) == 3:
                    if chkextdcol(colors[2]): self.fgextdcol(colors[2])
                    else: raise ValueError("invalid ANSI-color index value")
                else:
                    raise ValueError("invalid extended color format (expected 38;5;N)")
            else:
                raise ValueError("invalid ANSI-color index value")

        elif len(colors) == 1:
            if chkfgstdcol(colors[0]): self.fgstdcol(colors[0])
            else: raise ValueError("invalid ANSI-color index value")

        else:
            raise ValueError("invalid ANSI-color index value")

        
    @property
    def bg(self) -> str:
        return self.__bar.BACKGROUND.decode("utf-8")
    
    @bg.setter
    def bg(self, bg: str):
        if len(bg) > 19: raise MemoryError("background value is too large")
        elif not bg.startswith("\033[") or not bg.endswith("m"):
            raise ValueError("background must be an ANSI-color")
        
        try:
            colstr = bg[2:-1] # throw \033[ and m
            colors = [int(col) for col in colstr.split(';')] # split a string into indexes
        except ValueError:
            raise ValueError("invalid ANSI-color value")
        
        if colors[0] == 48:
            if len(colors) < 3:
                raise ValueError("invalid non-standard color format (excepted 48;5;N or 48;2;R;G;B)")
            
            elif colors[1] == 2:
                if len(colors) == 5:
                    if chktruecol(colors[2],colors[3],colors[4]): self.bgtruecol(colors[2], colors[3], colors[4])
                    else: raise ValueError("invalid ANSI-color index value")
                else: 
                    raise ValueError("invalid true color format (expected 48;2;R;G;B)")

            elif colors[1] == 5:
                if len(colors) == 3:
                    if chkextdcol(colors[2]): self.bgextdcol(colors[2])
                    else: raise ValueError("invalid ANSI-color index value")
                else:
                    raise ValueError("invalid extended color format (expected 48;5;N)")
            else:
                raise ValueError("invalid ANSI-color index value")

        elif len(colors) == 1:
            if chkbgstdcol(colors[0]): self.bgstdcol(colors[0])
            else: raise ValueError("invalid ANSI-color index value")

        else:
            raise ValueError("invalid ANSI-color index value")


    def setfgnul(self): _c_lib.setfgnul(ctypes.byref(self.__bar)) # clear foreground
    def setbgnul(self): _c_lib.setbgnul(ctypes.byref(self.__bar)) # clear background
    def fgstdcol(self, col: int): _c_lib.fgstdcol(ctypes.byref(self.__bar), col) # set foreground standard color
    def bgstdcol(self, col: int): _c_lib.bgstdcol(ctypes.byref(self.__bar), col) # set background standard color
    def fgextdcol(self, col: int): _c_lib.fgextdcol(ctypes.byref(self.__bar), col) # set foreground extended color
    def bgextdcol(self, col: int): _c_lib.bgextdcol(ctypes.byref(self.__bar), col) # set background extended color
    def fgtruecol(self, r: int, g: int, b: int): _c_lib.fgtruecol(ctypes.byref(self.__bar), r,g,b) # set foreground true color
    def bgtruecol(self, r: int, g: int, b: int): _c_lib.bgtruecol(ctypes.byref(self.__bar), r,g,b) # set background true color

    def getstrbar(self) -> str:
        """ Gets a string bar """
        res = _c_lib.getstrbar(ctypes.byref(self.__bar))
        return res.decode('utf-8') if res else ""

    def getsmoothbar(self) -> str:
        """ Gets a smooth string bar """
        res = _c_lib.getsmoothbar(ctypes.byref(self.__bar))
        return res.decode('utf-8') if res else ""

    def printbar(self): print(self.getstrbar(),end="")
    def printsmbar(self): print(self.getsmoothbar(),end="")


def init_console(): return _c_lib.init_console() # enable UTF-8 and support of ANSI-colors
def init_bar() -> Bar: return Bar(0,30,"\033[37m","\033[100m") # set default value for the bar

def chkfgstdcol(col: int): return _c_lib.chkfgstdcol(col) # standard color value check (foreground)
def chkbgstdcol(col: int): return _c_lib.chkfgstdcol(col) # standard color value check (background)
def chkextdcol(col: int): return _c_lib.chkextdcol(col) # extended color value check
def chktruecol(r: int, g: int, b: int): return _c_lib.chktruecol(r,g,b) # true color value check


""" Searching for the custom_pb.dll library """
script_dir = Path(__file__).resolve().parent
parent_dir = script_dir.parent
dll_name = "custom_pb.dll"

search_dirs = [script_dir, parent_dir] + [p for p in parent_dir.iterdir() if p.is_dir() and p != script_dir]

for folder in search_dirs:
    dll_path = folder / dll_name
    if dll_path.is_file():
        _c_lib = ctypes.CDLL(str(dll_path)) # load received dll
        break
else:
    raise FileNotFoundError("couldnt find the required library custom_pb.dll")


_c_lib.init_console.restype = None
_c_lib.init_console.argtypes = []

_c_lib.init_bar.restype = _C_BAR
_c_lib.init_bar.argtypes = []

_c_lib.chkfgstdcol.restype = ctypes.c_bool
_c_lib.chkfgstdcol.argtypes = [ctypes.c_int]
_c_lib.chkbgstdcol.restype = ctypes.c_bool
_c_lib.chkbgstdcol.argtypes = [ctypes.c_int]
_c_lib.chkextdcol.restype = ctypes.c_bool
_c_lib.chkextdcol.argtypes = [ctypes.c_int]
_c_lib.chktruecol.restype = ctypes.c_bool
_c_lib.chktruecol.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]

_c_lib.setfgnul.restype = None
_c_lib.setfgnul.argtypes = [ctypes.POINTER(_C_BAR)]
_c_lib.setbgnul.restype = None
_c_lib.setbgnul.argtypes = [ctypes.POINTER(_C_BAR)]

_c_lib.fgstdcol.restype = None
_c_lib.fgstdcol.argtypes = [ctypes.POINTER(_C_BAR), ctypes.c_int]
_c_lib.bgstdcol.restype = None
_c_lib.bgstdcol.argtypes = [ctypes.POINTER(_C_BAR), ctypes.c_int]

_c_lib.fgextdcol.restype = None
_c_lib.fgextdcol.argtypes = [ctypes.POINTER(_C_BAR), ctypes.c_int]
_c_lib.bgextdcol.restype = None
_c_lib.bgextdcol.argtypes = [ctypes.POINTER(_C_BAR), ctypes.c_int]

_c_lib.fgtruecol.restype = None
_c_lib.fgtruecol.argtypes = [ctypes.POINTER(_C_BAR), ctypes.c_int, ctypes.c_int, ctypes.c_int]
_c_lib.bgtruecol.restype = None
_c_lib.bgtruecol.argtypes = [ctypes.POINTER(_C_BAR), ctypes.c_int, ctypes.c_int, ctypes.c_int]

_c_lib.getstrbar.restype = ctypes.c_char_p
_c_lib.getstrbar.argtypes = [ctypes.POINTER(_C_BAR)]
_c_lib.getsmoothbar.restype = ctypes.c_char_p
_c_lib.getsmoothbar.argtypes = [ctypes.POINTER(_C_BAR)]

_c_lib.printbar.restype = None
_c_lib.printbar.argtypes = [ctypes.POINTER(_C_BAR)]
_c_lib.printsmbar.restype = None
_c_lib.printsmbar.argtypes = [ctypes.POINTER(_C_BAR)]

