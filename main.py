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
    _methods: list[Method]
    _effectiveness: Optional[float]

    def __init__(self):
        self._methods = list()
        self._effectiveness = None

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
    _ax: plt.Axes

    def __init__(self):
        self._ax = plt.axes()

        self._ax.set_title("Probability of Pregnancy")
        self._ax.grid(visible=True, which='major', linestyle='-')
        self._ax.grid(visible=True, which='minor', axis='x', linestyle=':')
        self._ax.minorticks_on()
        self._ax.yaxis.set_major_formatter(m_tick.PercentFormatter(xmax=1))

    def add_scenario(self, scenario: Scenario, window: tuple[int, int] = (0, 50)) -> None:
        cumulative_p_list = list(scenario.p_failure_list(min_times=window[0], max_times=window[1]))
        self._ax.plot(cumulative_p_list)

    def show(self) -> None:
        plt.show()


def main():
    plot = MyPlot()

    scenario = Scenario()

    scenario.add_method(Method(0.99))
    scenario.add_method(Method(0.84))

    plot.add_scenario(scenario)
    plot.show()


if __name__ == '__main__':
    main()
