#!/usr/bin/env python

from abc import ABC, abstractmethod
from datetime import timedelta


class NotifcationException(BaseException):
    pass


class Notifier(ABC):
    def __init__(self) -> None:
        pass

    def notify_complete(self, total_time_taken: timedelta) -> None:
        """
        Notify the user that the entire process is complete.
        """
        try:
            self._notify_complete(total_time_taken)
        except NotifcationException as e:
            # TODO alert better on this
            print(e)

    @abstractmethod
    def _notify_complete(self, total_time_taken: total_time_taken) -> None:
        """
        Notify the user that the entire process is complete.
        """
        pass
