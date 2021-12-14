import matplotlib.pyplot as plt
import matplotlib.ticker as m_tick
import math
from functools import cached_property
from typing import Optional, Iterator, Iterable


class Method:
    _effectiveness: float

    def __init__(self, effectiveness: float):
        assert 0.0 <= effectiveness <= 1.0
        self._effectiveness = effectiveness

    @property
    def effectiveness(self) -> float:
        return self._effectiveness

    @cached_property
    def p_failure(self) -> float:
        return 1 - self._effectiveness


class Scenario:
    _name: str
    _methods: list[Method]
    _effectiveness: Optional[float]

    def __init__(self, name: str):
        self._name = name
        self._methods = list()
        self._effectiveness = None

    @property
    def name(self) -> str:
        return self._name

    def add_method(self, method: Method) -> None:
        self._methods.append(method)

    def effectiveness(self, n: int = 1) -> float:
        if self._effectiveness is None:
            total = 1
            for m in self._methods:
                total *= m.p_failure
            self._effectiveness = 1 - total

        return self._effectiveness ** n

    def n_for_threshold(self, threshold: float) -> float:
        return math.log(1 - threshold, self.effectiveness())

    def n_list(self, thresholds: Iterable[float]) -> Iterator[float]:
        for t in thresholds:
            yield self.n_for_threshold(t)


class MyPlot:
    _scenarios: list[Scenario]

    def __init__(self, scenarios: Iterator[Scenario]):
        self._scenarios = list(scenarios)

    @cached_property
    def _steps(self, *, min_threshold: float = 0.0, max_threshold: float = 1.0, step_size: float = 0.01) -> list[float]:
        steps = [min_threshold + step_size * mult for mult in range(math.ceil((max_threshold - min_threshold) / step_size))]
        return steps

    def _setup_axes(self, ax: plt.Axes) -> None:
        ax.set_xscale('log')
        ax.set_yscale('log')

        ax.grid(visible=True, which='major', linestyle='-')
        ax.grid(visible=True, which='minor', axis='x', linestyle=':')
        ax.grid(visible=True, which='minor', axis='y', linestyle=':')
        ax.minorticks_on()
        ax.yaxis.set_major_formatter(m_tick.PercentFormatter(xmax=1))
        ax.xaxis.set_major_formatter(m_tick.FuncFormatter("{:,.0f}".format))

        ax.set_xlabel("Times having sex")
        ax.set_ylabel("Chance of pregnancy")

    def show(self) -> None:
        max_n = 100_000

        fig, axes = plt.subplots(nrows=len(self._scenarios))
        fig: plt.Figure
        fig.tight_layout(pad=3.0)

        for ax, scenario in zip(axes, self._scenarios):
            self._setup_axes(ax)
            ax.set_xlim(right=max_n)
            ax.set_title(scenario.name)

            n_list = list(scenario.n_list(self._steps))
            ax.plot(n_list, self._steps, label=scenario.name)

        plt.suptitle("Probability of Pregnancy")
        plt.show()


def main():
    scenario1 = Scenario("Scenario 1")
    scenario1.add_method(Method(0.91))
    scenario1.add_method(Method(0.85))
    scenario1.add_method(Method(0.76))

    scenario2 = Scenario("Scenario 2")
    scenario2.add_method(Method(0.99))
    scenario2.add_method(Method(0.91))
    scenario2.add_method(Method(0.85))
    scenario2.add_method(Method(0.76))

    plot = MyPlot([scenario1, scenario2])
    plot.show()


if __name__ == '__main__':
    main()
