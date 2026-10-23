import csv

INPUT_FILE = "Corp_Summary.csv"
OUTPUT_FILE = "report.csv"


def read_file(filename):
    rows = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            if len(row) == 6:
                rows.append(row)
    return rows


def hierarchy(rows):
    result = {}
    for row in rows:
        dep = row[1]
        team = row[2]
        if dep not in result:
            result[dep] = []
        if team not in result[dep]:
            result[dep].append(team)
    return result


def summary(rows):
    salaries = {}
    for row in rows:
        dep = row[1]
        salary = float(row[5])
        if dep not in salaries:
            salaries[dep] = []
        salaries[dep].append(salary)

    result = []
    for dep in salaries:
        s = salaries[dep]
        result.append([dep, len(s), min(s), max(s), round(sum(s) / len(s), 2)])
    return result


def print_hierarchy(rows):
    data = hierarchy(rows)
    for dep in data:
        print(dep)
        for team in data[dep]:
            print("   -", team)


def print_summary(rows):
    data = summary(rows)
    print("Департамент  Численность  Мин  Макс  Средняя")
    for line in data:
        print(line[0], "  ", line[1], "  ", line[2], "  ",
              line[3], "  ", line[4])


def save_summary(rows, filename=OUTPUT_FILE):
    data = summary(rows)
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(
            ["Департамент", "Численность", "Мин", "Макс", "Средняя"]
        )
        for line in data:
            writer.writerow(line)
    print("Отчет сохранен в", filename)


def main(variant, filename=OUTPUT_FILE):
    rows = read_file(INPUT_FILE)
    if variant == 1:
        print_hierarchy(rows)
    elif variant == 2:
        print_summary(rows)
    elif variant == 3:
        save_summary(rows, filename)
    else:
        print("Нет такого варианта, выберите 1, 2 или 3")


if __name__ == "__main__":
    main(int(input("Выберите вариант 1, 2, 3: ")))
