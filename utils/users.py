from utils.contracts import validate_document


def user_endpoint(user_id):
    if type(user_id) is not int or user_id <= 0:
        raise ValueError("user_id must be a positive integer")
    return f"/users/{user_id}"


class UsersApi:
    def __init__(self, client):
        self.client = client

    def create(self, payload):
        validate_document(payload, "user_request")
        return self.client.request("POST", "/users", payload=payload)

    def read(self, user_id):
        return self.client.request("GET", user_endpoint(user_id))

    def update(self, user_id, payload):
        endpoint = user_endpoint(user_id)
        validate_document(payload, "user_request")
        return self.client.request("PUT", endpoint, payload=payload)

    def delete(self, user_id):
        return self.client.request("DELETE", user_endpoint(user_id))
