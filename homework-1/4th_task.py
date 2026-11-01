days: list[dict] = [
    {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
    {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
    {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
    {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
    {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
]


def main() -> None:
    print("выручка за неделю:", sum(d["revenue"] for d in days))
    print("лучший день:", max(days, key=lambda d: d["revenue"])["day"])

    for d in days:
        print(d["day"], d["revenue"] / d["orders"])

    print("возвратов > 20%:",
          [d["day"] for d in days if d["returns"] / d["orders"] > 0.2])


if __name__ == "__main__":
    main()
