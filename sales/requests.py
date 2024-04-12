import requests


def inventory_update_quantity(id_produto: int, quantity: int):
    url = "http://127.0.0.1:8001/inventorys/update-quantities"

    payload = [
        {
            "id": id_produto,
            "quantity": -quantity
        }
    ]
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "insomnia/8.6.1"
    }

    response = requests.request("PUT", url, json=payload, headers=headers)

    return response
