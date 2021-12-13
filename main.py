def get_total_effectiveness(effectiveness_list: list[float]) -> float:
    total = 1
    for e in effectiveness_list:
        total *= (1 - e)
    return 1 - total


def get_cumulative_p_of_failure(effectiveness_list: list[float], recurrences: int) -> float:
    e_total = get_total_effectiveness(effectiveness_list)
    return 1 - e_total**recurrences


def main():
    effs = [float(p) for p in input("Effectiveness list> ").split()]

    while True:
        n = int(input("Number of occurrences> "))
        result = get_cumulative_p_of_failure(list(effs), n)
        print(f"{result:.2%}")


if __name__ == '__main__':
    main()
