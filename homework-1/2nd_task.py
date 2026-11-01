queries = [
    "чехол",
    "iphone",
    "чехол",
    "наушники",
    "iphone",
    "iphone",
    "кабель",
    "чехол",
    "iphone",
]


def main() -> None:
    counts: dict[str, int] = {}
    for q in queries:
        counts[q] = counts.get(q, 0) + 1

    top = max(counts, key=counts.__getitem__)

    print("всего запросов:", len(queries))
    print("частота каждого запроса:", counts)
    print("самый частый запрос:", top)
    print("доля самого частого:", counts[top] / len(queries))
    print("один раз:", [q for q in counts if counts[q] == 1])


if __name__ == "__main__":
    main()
