moscow = {201, 202, 203, 204}
kazan = {203, 204, 205, 206}

print("в любом из городов:", moscow & kazan)
print("только в Москве:", moscow - kazan)
print("только в Казани:", kazan - moscow)
print("всего разных товаров:", len(moscow | kazan))
