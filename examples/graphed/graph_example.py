#!/usr/bin/env python

import typing as t
from functools import partial

import matplotlib.pyplot as plt

from orbiteer import orbiteer

# Bigger plot
plt.rcParams["figure.figsize"] = [10, 7]
plt.rcParams["figure.dpi"] = 400


def make_underlying(
    formula: t.Callable[[int], float],
    xmin: int = 0,
    xmax: int = 100,
    xstep: int = 1,
) -> t.Dict[int, float]:
    return {x: formula(x) for x in range(xmin, xmax, xstep)}


def calculate_static_buckets(x: t.Sized, num_buckets: int) -> t.List[t.Tuple[int, int]]:
    size = round(len(x) / num_buckets)
    if size * num_buckets != len(x):
        raise RuntimeError("Need perfectly divisible bucket counts")

    buckets = list(range(0, len(x) + 1, size))

    # Convert the single list of buckets to a list of edge pairs, ie, buckets
    return list(zip(buckets, buckets[1:]))


def sample_callable(
    data_source: t.Dict[int, int],
    bucket_history: t.List[t.Tuple[int, int]],
    raw_left: str,
    raw_right: str,
) -> float:
    left = int(float(raw_left))
    right = int(float(raw_right))
    bucket_history.append((left, right))

    total = 0
    for i in range(left, right):
        total += data_source[i]

    return total


def offset_buckets(buckets: t.List[t.Tuple[int, int]], offset_distance: float) -> t.List[t.Tuple[float, float]]:
    return [(left + offset_distance, right - offset_distance) for left, right in buckets]


def simple_decrease_graph_example() -> None:
    """
    An ugly example of how buckets can change over time depending on a hidden underlying data source
    """
    simple_decrease = make_underlying(lambda x: 1000 - x, 0, 1000, 1)

    static_buckets = calculate_static_buckets(simple_decrease.keys(), 20)
    static_bucket_width = static_buckets[0][1] - static_buckets[0][0]

    bucket_visual_shrink_width = 2.5

    orbiteer_buckets: t.List[t.Tuple[int, int]] = []

    o = orbiteer.Orbiteer(
        target_type="callable",
        target_to_call=partial(sample_callable, simple_decrease, orbiteer_buckets),
        target_measurement_strategy="OUTPUT",
        optimizer_type="ratio",
        optimizer_goal=50000,
        optimizer_first_value=50,
        inputgenerator_type="range",
        inputgenerator_left=0,
        inputgenerator_right=1000,
    )
    o.run()

    # Modified buckets with some visual space for readability
    mod_static_buckets = offset_buckets(static_buckets, bucket_visual_shrink_width)
    static_bucket_y = (1050, 1050)

    mod_orbiteer_buckets = offset_buckets(orbiteer_buckets, bucket_visual_shrink_width)
    orbiteer_bucket_y = (1100, 1100)

    fig = plt.figure()
    fig.patch.set_facecolor("white")
    plt.bar(simple_decrease.keys(), simple_decrease.values(), width=1.0, label="Underlying Data")

    # Plot the buckets with .errorbar so that we can those edge markers
    for bucket_x in mod_static_buckets:
        plt.errorbar(
            bucket_x,
            static_bucket_y,
            yerr=static_bucket_width * 0.25,
            color="red",
            linestyle="--",
            label="Static Width Buckets",
        )

    for bucket_x in mod_orbiteer_buckets:
        plt.errorbar(
            bucket_x,
            orbiteer_bucket_y,
            yerr=static_bucket_width * 0.25,
            color="green",
            linestyle=":",
            label="Orbiteer-generated Buckets",
        )

    # Unique labels
    # https://stackoverflow.com/a/13589144
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.title("Static-width vs Orbiteer-generated Bucket Comparison")

    # Tightens up the plot and ensures predictable ticks
    plt.xlim(0, 1000)
    plt.xlabel("X")
    plt.xticks([0, 200, 400, 600, 800, 1000])

    plt.ylim(0, 1200)
    plt.ylabel("Y")
    plt.yticks([0, 200, 400, 600, 800, 1000])

    plt.savefig("comparison.png")


if __name__ == "__main__":
    simple_decrease_graph_example()
