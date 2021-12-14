import matplotlib.pyplot as plt
import matplotlib.ticker as m_tick
from functools import cached_property
from typing import Optional, Iterator


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

    def p_failure(self, recurrences: int = 1) -> float:
        return 1 - self.effectiveness(recurrences)

    def p_failure_list(self, *, min_times: int = 0, max_times: int) -> Iterator:
        for n in range(min_times, max_times + 1):
            yield self.p_failure(n)


class MyPlot:
    _scenarios: list[Scenario]

    def __init__(self, scenarios: Iterator[Scenario]):
        self._scenarios = list(scenarios)

    def _setup_axes(self, ax: plt.Axes) -> None:
        ax.set_ylim(top=0.1)

        ax.grid(visible=True, which='major', linestyle='-')
        ax.grid(visible=True, which='minor', axis='x', linestyle=':')
        ax.minorticks_on()
        ax.yaxis.set_major_formatter(m_tick.PercentFormatter(xmax=1))

    def show(self, window: tuple[int, int] = (0, 50)) -> None:
        for idx, scenario in enumerate(self._scenarios):
            ax: plt.Axes = plt.subplot(len(self._scenarios), 1, idx+1)

            self._setup_axes(ax)
            ax.set_title(scenario.name)

            cumulative_p_list = list(scenario.p_failure_list(min_times=window[0], max_times=window[1]))
            ax.plot(cumulative_p_list, label=scenario.name)

            ax.legend()

        plt.suptitle("Probability of Pregnancy")
        plt.show()


def main():
    scenario1 = Scenario("Scenario 1")
    scenario1.add_method(Method(0.99))
    scenario1.add_method(Method(0.84))

    scenario2 = Scenario("Scenario 2")
    scenario2.add_method(Method(0.99))
    scenario2.add_method(Method(0.84))
    scenario2.add_method(Method(0.91))

    plot = MyPlot([scenario1, scenario2])
    plot.show()


if __name__ == '__main__':
    main()
