#!/usr/bin/env python

import typing as t

import orbiteer.inputgenerators as inputgenerators
import orbiteer.optimizers as optimizers
import orbiteer.runner as runner
import orbiteer.targets as targets


class Orbiteer:
    input_generator_name_map = {
        "range": inputgenerators.NumericalRangeGenerator,
        "datetime_range": inputgenerators.DatetimeRangeGenerator,
    }

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        self.target = self.make_target(**self._filter_kwargs("target", **kwargs))
        self.optimizer = self.make_optimizer(**self._filter_kwargs("optimizer", **kwargs))
        self.inputgenerator = self.make_inputgenerator(**self._filter_kwargs("inputgenerator", **kwargs))

        self.runner = runner.OrbiteerRunner(self.inputgenerator, self.target)

    def run(self) -> None:
        self.runner.run()

    def make_target(self, **kwargs: t.Any) -> targets.AbstractTarget:
        target_type = self._get_required_kwarg_or_raise("target_type", **kwargs)

        if target_type.lower() == "command":
            target_class = targets.CommandTarget
        else:
            raise RuntimeError(f"Invalid target_type: {target_type}")

        return target_class(**kwargs)

    def make_optimizer(self, **kwargs: t.Any) -> optimizers.AbstractOptimizer:
        optimizer_type = self._get_required_kwarg_or_raise("optimizer_type", **kwargs)

        if optimizer_type.lower() == "ratio":
            optimizer_class = optimizers.RatioOptimizer
        else:
            raise RuntimeError(f"Invalid optimizer_type: {optimizer_type}")

        return optimizer_class(**kwargs)

    def make_inputgenerator(self, **kwargs: t.Any) -> inputgenerators.AbstractInputGenerator[t.Any]:
        inputgenerator_type = self._get_required_kwarg_or_raise("inputgenerator_type", **kwargs)

        name = inputgenerator_type.lower()
        if name in self.input_generator_name_map:
            inputgenerator_class = self.input_generator_name_map[name]
        else:
            raise RuntimeError(f"Invalid inputgenerator_type: {inputgenerator_type}")

        return inputgenerator_class(**kwargs)

    def _filter_kwargs(self, prefix: str, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        return {key: value for key, value in kwargs.items() if key.startswith(prefix)}

    def _get_required_kwarg_or_raise(self, key: str, **kwargs: t.Any) -> t.Any:
        value = kwargs.get(key)
        if value is None:
            raise RuntimeError(f"Missing required argument: {key}")
        return value
