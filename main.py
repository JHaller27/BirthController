def get_total_effectiveness(effectiveness_list: list[float]) -> float:
    total = 1
    for e in effectiveness_list:
        total *= (1 - e)
    return 1 - total


def get_cumulative_p_of_failure(e_total: float, recurrences: int) -> float:
    return 1 - e_total**recurrences


def main():
    effs = [float(p) for p in input("Effectiveness list> ").split()]
    e_total = get_total_effectiveness(effs)

    while True:
        n = int(input("Number of occurrences> "))
        result = get_cumulative_p_of_failure(e_total, n)
        print(f"{result:.2%}")


if __name__ == '__main__':
    main()
