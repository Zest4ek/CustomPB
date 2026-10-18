""" Requires: bin/custom_pb.dll """
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
    def percent(self) -> int: return self.pb.PERCENT
    
    @percent.setter
    def percent(self, percent: int):
        if not self.chkpercent():
            self.pb.PERCENT = percent
        else:
            raise ValueError("invalid percent value")

    @property
    def width(self) -> int: return self.pb.WIDTH
    
    @width.setter
    def width(self, width: int):
        if not self.chkwidth():
            self.pb.WIDTH = width
        else:
            raise ValueError("invalid width value")


    @property
    def fg(self) -> str: return self.pb.FOREGROUND.decode("utf-8")

    @fg.setter
    def fg(self, fg: str):
        if not fg.startswith("\033[") or not fg.endswith("m"):
            raise ValueError("foreground must be an ANSI-color")
        
        try:
            colstr = fg[2:-1]
            colors = [int(col) for col in colstr.split(';')]
        except ValueError:
            raise ValueError("invalid ANSI-color value")

        if colors[0] == 38:
            if len(colors) < 2:
                raise ValueError("invalid ANSI-color index value")
            
            if colors[1] == 2:
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
        return self.pb.BACKGROUND.decode("utf-8")
    
    @bg.setter
    def bg(self, bg: str):
        if not bg.startswith("\033[") or not bg.endswith("m"):
            raise ValueError("background must be an ANSI-color")
        
        try:
            colstr = bg[2:-1]
            colors = [int(col) for col in colstr.split(';')]
        except ValueError:
            raise ValueError("invalid ANSI-color value")

        if colors[0] == 48:
            if len(colors) < 2:
                raise ValueError("invalid ANSI-color index value")
            
            if colors[1] == 2:
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
        

    def chkpercent(self): _c_lib.chkpercent(ctypes.byref(self.pb))
    def chkwidth(self): _c_lib.chkwidth(ctypes.byref(self.pb))

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

def chkfgstdcol(col: int): return _c_lib.chkfgstdcol(col)
def chkbgstdcol(col: int): return _c_lib.chkfgstdcol(col)
def chkextdcol(col: int): return _c_lib.chkextdcol(col)
def chktruecol(r: int, g: int, b: int): return _c_lib.chktruecol(r,g,b)


lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "custom_pb.dll"))
try:
    _c_lib = ctypes.CDLL(lib_path)
except OSError:
    _c_lib = ctypes.CDLL("custom_pb.dll")

_c_lib.init_console.restype = None
_c_lib.init_console.argtypes = []

_c_lib.init_bar.restype = _C_BAR
_c_lib.init_bar.argtypes = []

_c_lib.chkpercent.restype = ctypes.c_bool
_c_lib.chkpercent.argtypes = [ctypes.POINTER(_C_BAR)]
_c_lib.chkwidth.restype = ctypes.c_bool
_c_lib.chkwidth.argtypes = [ctypes.POINTER(_C_BAR)]

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
