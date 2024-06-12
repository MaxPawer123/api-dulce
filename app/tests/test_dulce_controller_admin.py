
def test_get_dulces(test_client, admin_auth_headers):
    response = test_client.get("/api/dulces", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json == []


def test_create_dulce(test_client, admin_auth_headers):
    data = {"marca": "coyote", "peso": 5.5, "sabor": "dulce","origen":"americana"}
    response = test_client.post("/api/dulces", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    assert response.json["marca"] == "coyote"
    assert response.json["peso"] == 5.5
    assert response.json["sabor"] == "dulce"
    assert response.json["origen"] == "americana"


def test_get_dulce(test_client, admin_auth_headers):
    # Primero crea un dulce
    data = {"marca": "toyota", "peso": 6.5, "sabor": "amargo","origen":"europeo"}
    response = test_client.post("/api/dulces", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    dulce_id = response.json["id"]

    # Ahora obtén el dulce
    response = test_client.get(f"/api/dulces/{dulce_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json["marca"] == "toyota"
    assert response.json["peso"] == 6.5
    assert response.json["sabor"] == "amargo"
    assert response.json["origen"] == "europeo"

def test_get_nonexistent_dulce(test_client, admin_auth_headers):
    response = test_client.get("/api/dulces/999", headers=admin_auth_headers)
    print(response.json)
    assert response.status_code == 404
    assert response.json["error"] == "Dulce no encontrado"


def test_create_dulce_invalid_data(test_client, admin_auth_headers):
    data = {"marca": "Pepin"}  # Falta species y age
    response = test_client.post("/api/dulces", json=data, headers=admin_auth_headers)
    assert response.status_code == 400
    assert response.json["error"] == "Faltan datos requeridos"

def test_update_dulce(test_client, admin_auth_headers):
    # Primero crea un libro
    data = {"marca": "Peopin", "peso": 10.5, "sabor": "amargo","origen":"europeo"}
    response = test_client.post("/api/dulces", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    dulce_id = response.json["id"]

    # Ahora actualiza el libro
    update_data = {"marca": "Peopin", "peso": 10.5, "sabor": "picante","origen":"americano"}
    response = test_client.put(
        f"/api/dulces/{dulce_id}", json=update_data, headers=admin_auth_headers
    )
    assert response.status_code == 200
    assert response.json["sabor"] == "picante"
    assert response.json["origen"] == "americano"


def test_update_nonexistent_dulce(test_client, admin_auth_headers):
    update_data = {"marca": "toyota", "peso": 10.5, "sabor": "picante","origen":"americano"}
    response = test_client.put(
        "/api/dulces/999", json=update_data, headers=admin_auth_headers
    )
    print(response.json)
    assert response.status_code == 404
    assert response.json["error"] == "Dulce no encontrado"
    
def test_delete_dulce(test_client, admin_auth_headers):
    # Primero crea un libro
    data = {"marca": "fermat", "peso": 11.3, "sabor": "picante","origen":"europeo"}
    response = test_client.post("/api/dulces", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    dulce_id = response.json["id"]
    response = test_client.delete(
        f"/api/dulces/{dulce_id}", headers=admin_auth_headers
    )
    assert response.status_code == 204
    response = test_client.get(f"/api/dulces/{dulce_id}", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Dulce no encontrado"


def test_delete_nonexistent_dulce(test_client, admin_auth_headers):
    response = test_client.delete("/api/dulces/999", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Dulce no encontrado"

