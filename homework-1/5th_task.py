from collections import defaultdict

reviews: list[dict] = [
    {"id": 1, "product": "Чехол", "stars": 5},
    {"id": 1, "product": "Чехол", "stars": 3},
    {"id": 1, "product": "Чехол", "stars": 4},
    {"id": 2, "product": "Наушники", "stars": 2},
    {"id": 2, "product": "наушники", "stars": 2},
    {"id": 2, "product": "НАУШНИКИ", "stars": 5},
    {"id": 3, "product": "Планшет", "stars": 5},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 5, "product": "Кабель", "stars": 1},
]


def main() -> None:
    marks_by_name: defaultdict[str, list[int]] = defaultdict(list)
    for r in reviews:
        marks_by_name[r["product"].capitalize()].append(r["stars"])

    worst = None
    worst_avg = None
    for name, marks in marks_by_name.items():
        avg = sum(marks) / len(marks)
        print(name, avg)

        if len(marks) >= 2 and (worst_avg is None or avg < worst_avg):
            worst = name
            worst_avg = avg

    print("худший (от 2 отзывов):", worst)

    low = [r for r in reviews if r["stars"] <= 2]
    print("отзывов на 1–2 звезды:", len(low))
    print("доля:", len(low) / len(reviews))


if __name__ == "__main__":
    main()
