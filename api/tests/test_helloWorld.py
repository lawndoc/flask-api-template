

def testHelloWorld(client):
    response = client.get("/api/hello-world",
                          headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert response.json["message"] == "Hello World!"