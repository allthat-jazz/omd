orders: list[dict] = [
    {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
    {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
    {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
    {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
    {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
    {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
]


def main() -> None:
    returned = [o for o in orders if o["status"] == "returned"]
    delivered = [o for o in orders if o["status"] == "delivered"]

    print("сумма возвратов:", sum(o["amount"] for o in returned))
    print("вернули заказ:", {o["buyer"] for o in returned})
    print("доставлено заказов:", len(delivered))
    print("средний чек:",
          sum(o["amount"] for o in delivered) / len(delivered))


if __name__ == "__main__":
    main()
