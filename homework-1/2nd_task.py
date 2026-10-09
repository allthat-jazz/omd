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

counts: dict[str, int] = {}
for q in queries:
    counts[q] = counts.get(q, 0) + 1

top = queries[0]
for q in counts:
    if counts[q] > counts[top]:
        top = q

print("всего запросов:", len(queries))
print("частота каждого запроса:", counts)
print("самый частый запрос:", top)
print("доля самого частого:", counts[top] / len(queries))
print("один раз:", [q for q in counts if counts[q] == 1])
