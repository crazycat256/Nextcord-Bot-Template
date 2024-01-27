import logging
from datetime import datetime
from typing import Literal

from utils.shared_functions import get_traceback


class Logger:
    
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    
    def __init__(
        self,
        name: str,
        filename: str,
        level: int = logging.INFO,
        mode: str = "a",
        format: str = "%(asctime)s:%(levelname)s:%(name)s: %(message)s",
        print_level: int = logging.INFO,
        colors: bool = True
    ):
        """A logger object that logs to a file and optionally prints to the console

        Parameters
        ----------
        name: :class:`str`
            The name of the logger
        filename : :class:`str`
            The name of the file to log to
        level: :class:`int`, optional
            The level of the logger, by default logging.INFO
        mode: :class:`str`, optional
            The mode to open the file in, by default "a"
        format: :class:`str`, optional
            The format of the log messages, by default "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
        print_level: :class:`int`, optional
            The level of the messages to print to the console, by default logging.INFO
        colors: :class:`bool`, optional
            Whether to use colors in the console, by default True
        """
        self.name = name
        self.filename = filename
        self.level = level
        self.mode = mode
        self.format = format
        self.print_level = print_level
        self.colors = colors
        
        self._handler = logging.FileHandler(filename, encoding="utf-8", mode=mode)
        self._handler.setFormatter(logging.Formatter(format))
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.addHandler(self._handler)
    
    
    def __str__(self):
        return f"Logger(name={self.name}, filename={self.filename}, level={self.level}, mode={self.mode}, format={self.format}, print_level={self.print_level}, colors={self.colors})"
    
        
    def log(self, *args: str, level: Literal["info", "warning", "error", "critical", "debug"] | int = logging.INFO, **kwargs):
        """Log a message
        
        Parameters
        ----------
        *args: :class:`str`
            The message to log
        level: :class:`int` or :class:`str`, optional
            The level of the message, by default logging.INFO
        **kwargs:
            The keyword arguments to pass to :meth:`logging.Logger.log`
        """
        
        msg = " ".join(str(arg) for arg in args)
        
        self._logger.log(level, msg, **kwargs)
        
        if isinstance(level, str):
            level = self.levels.get(level.lower(), logging.INFO)
        
        if self.print_level <= level:
            msg = f"[{self.name.upper()}] [{datetime.now().strftime('%H:%M:%S')}] [{logging.getLevelName(level)}] {msg}"
            
            if self.colors:
                
                if level == logging.WARNING:
                    msg = f"\033[0;33m{msg}\033[0m" # Yellow
                    
                elif level == logging.ERROR:
                    msg = f"\033[0;31m{msg}\033[0m" # Red
                    
                elif level == logging.CRITICAL:
                    msg = f"\033[1;31m{msg}\033[0m" # Bold red
                    
                elif level == logging.DEBUG:
                    msg = f"\033[0;30m{msg}\033[0m" # Black
                    
            print(msg)
            
    
    def info(self, *args: str, **kwargs):
        """Log an info message
        
        Parameters
        ----------
        *args: :class:`str`
            The message to log
        **kwargs:
            The keyword arguments to pass to :meth:`logging.Logger.log`
        """
        self.log(*args, level=logging.INFO, **kwargs)
        
    def warning(self, *args: str, **kwargs):
        """Log a warning message
        
        Parameters
        ----------
        *args: :class:`str`
            The message to log
        **kwargs:
            The keyword arguments to pass to :meth:`logging.Logger.log`
        """
        self.log(*args, level=logging.WARNING, **kwargs)
        
    def error(self, *args: str, **kwargs):
        """Log an error message
        
        Parameters
        ----------
        *args: :class:`str`
            The message to log
        **kwargs:
            The keyword arguments to pass to :meth:`logging.Logger.log`
        """
        self.log(*args, level=logging.ERROR, **kwargs)
        
    def critical(self, *args: str, **kwargs):
        """Log a critical message
        
        Parameters
        ----------
        *args: :class:`str`
            The message to log
        **kwargs:
            The keyword arguments to pass to :meth:`logging.Logger.log`
        """
        self.log(*args, level=logging.CRITICAL, **kwargs)
        
    def debug(self, *args: str, **kwargs):
        """Log a debug message
        
        Parameters
        ----------
        *args: :class:`str`
            The message to log
        **kwargs:
            The keyword arguments to pass to :meth:`logging.Logger.log`
        """
        self.log(*args, level=logging.DEBUG, **kwargs)
        
    def exception(self, exception: Exception, **kwargs):
        """Log an exception
        
        Parameters
        ----------
        exception: :class:`Exception`
            The exception to log
        **kwargs:
            The keyword arguments to pass to :meth:`logging.Logger.log`
        """
        self._logger.error(get_traceback(exception), **kwargs)
        if self.print_level <= logging.ERROR:
            print(get_traceback(exception))
        
    
