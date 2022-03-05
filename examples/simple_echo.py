#!/usr/bin/env python

from datetime import datetime

from orbiteer import orbiteer


def simple_echo() -> None:
    o = orbiteer.Orbiteer(
        target_type="command",
        target_command_line=["echo", "range:"],
        optimizer_type="ratio",
        optimizer_goal=0.5,
        optimizer_first_value=60,
        inputgenerator_type="datetime_range",
        inputgenerator_left=datetime.fromisoformat("2022-01-01T00:00:00+00:00"),
        inputgenerator_right=datetime.fromisoformat("2022-02-01T00:00:00+00:00"),
    )
    o.run()


if __name__ == "__main__":
    simple_echo()
