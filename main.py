import matplotlib.pyplot as plt
import matplotlib.ticker as m_tick


def get_total_effectiveness(effectiveness_list: list[float]) -> float:
    total = 1
    for e in effectiveness_list:
        total *= (1 - e)
    return 1 - total


def get_cumulative_p_of_failure(e_total: float, recurrences: int) -> float:
    return 1 - e_total**recurrences


def main():
    effs = [0.99, 0.84]
    e_total = get_total_effectiveness(effs)

    cumulative_p_list = [get_cumulative_p_of_failure(e_total, n) for n in range(50+1)]

    ax: plt.Axes = plt.axes()

    ax.plot(cumulative_p_list)

    ax.set_title("Probability of Pregnancy")
    ax.grid(visible=True, which='major', linestyle='-')
    ax.grid(visible=True, which='minor', axis='x', linestyle=':')
    ax.minorticks_on()
    ax.yaxis.set_major_formatter(m_tick.PercentFormatter(xmax=1))

    plt.show()


if __name__ == '__main__':
    main()
