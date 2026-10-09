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

names = {r["product"].capitalize() for r in reviews}

worst = None
worst_avg = None
for name in names:
    marks = [r["stars"] for r in reviews if r["product"].capitalize() == name]
    avg = sum(marks) / len(marks)
    print(name, avg)

    if len(marks) >= 2 and (worst is None or avg < worst_avg):
        worst = name
        worst_avg = avg

print("худший (от 2 отзывов):", worst)

low = [r for r in reviews if r["stars"] <= 2]
print("отзывов на 1–2 звезды:", len(low))
print("доля:", len(low) / len(reviews))
