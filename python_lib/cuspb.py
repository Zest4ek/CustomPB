import ctypes
import os


class _C_BAR(ctypes.Structure):
    _fields_ = [
        ("PERCENT", ctypes.c_int),
        ("WIDTH", ctypes.c_int),
        ("FOREGROUND", ctypes.c_char*20),
        ("BACKGROUND", ctypes.c_char*20),
    ]


class Bar:
    def __init__(self, percent: int, width: int, fg: str, bg: str):
        self.pb = _C_BAR(
            PERCENT=percent if 0 <= percent <= 100 else 0,
            WIDTH=width if 0 <= width <= 1000 else 30,
            FOREGROUND=fg.encode("utf-8")[:19],
            BACKGROUND=bg.encode("utf-8")[:19]
        )

    @property
    def percent(self) -> int:
        return self.pb.PERCENT
    @percent.setter
    def percent(self, percent: int):
        self.pb.PERCENT = percent

    @property
    def width(self) -> int:
        return self.pb.WIDTH
    @width.setter
    def width(self, width: int):
        self.pb.WIDTH = width

    def setfgnul(self): _c_lib.setfgnul(ctypes.byref(self.pb))
    def setbgnul(self): _c_lib.setbgnul(ctypes.byref(self.pb))
    def fgstdcol(self, col: int): _c_lib.fgstdcol(ctypes.byref(self.pb), col)
    def bgstdcol(self, col: int): _c_lib.bgstdcol(ctypes.byref(self.pb), col)
    def fgextdcol(self, col: int): _c_lib.fgextdcol(ctypes.byref(self.pb), col)
    def bgextdcol(self, col: int): _c_lib.bgextdcol(ctypes.byref(self.pb), col)
    def fgtruecol(self, r: int, g: int, b: int): _c_lib.fgtruecol(ctypes.byref(self.pb), r,g,b)
    def bgtruecol(self, r: int, g: int, b: int): _c_lib.bgtruecol(ctypes.byref(self.pb), r,g,b)

    def getstrbar(self) -> str:
        res = _c_lib.getstrbar(ctypes.byref(self.pb))
        return res.decode('utf-8') if res else ""

    def getsmoothbar(self) -> str:
        res = _c_lib.getsmoothbar(ctypes.byref(self.pb))
        return res.decode('utf-8') if res else ""

    def printbar(self): print(self.getstrbar(),end="")
    def printsmbar(self): print(self.getsmoothbar(),end="")


def init_console(): return _c_lib.init_console()
def init_bar() -> Bar: return Bar(0,30,"\033[0m","\033[100m")


lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "custom_pb.dll"))
try:
    _c_lib = ctypes.CDLL(lib_path)
except OSError:
    _c_lib = ctypes.CDLL("custom_pb.dll")

_c_lib.init_console.restype = None
_c_lib.init_console.argtypes = []

_c_lib.init_bar.restype = _C_BAR
_c_lib.init_bar.argtypes = []

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
_c_lib.printbar.argtypes = [_C_BAR]

_c_lib.printsmbar.restype = None
_c_lib.printsmbar.argtypes = [_C_BAR]