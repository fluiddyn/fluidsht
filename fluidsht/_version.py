__version__ = "0.0.1a0"

try:
    from pyfiglet import figlet_format

    __about__ = figlet_format("fluidsht", font="big")
except ImportError:
    __about__ = r"""
      __ _       _     _     _     _
     / _| |     (_)   | |   | |   | |
    | |_| |_   _ _  __| |___| |__ | |_
    |  _| | | | | |/ _` / __| '_ \| __|
    | | | | |_| | | (_| \__ \ | | | |_
    |_| |_|\__,_|_|\__,_|___/_| |_|\__|

"""

__about__ = __about__.rstrip() + "\n" + " " * 25 + "v. " + __version__ + "\n"
