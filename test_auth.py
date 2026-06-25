import requests

# create account first
signup_response = requests.post(
    "http://localhost:8000/v1/signup",
    json={"email": "akhil@test.com", "password": "test1234"}
)
print("Signup status:", signup_response.status_code)
print("Signup response:", signup_response.json())

# now login
login_response = requests.post(
    "http://localhost:8000/v1/login",
    json={"email": "akhil@test.com", "password": "test1234"}
)
print("\nLogin status:", login_response.status_code)
print("Login response:", login_response.json())

token = login_response.json().get("access_token")

if token:
    response = requests.post(
        "http://localhost:8000/v1/reviews/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json={"review_text": "Great product, very happy", "rating": 5}
    )
    print("\nAnalyze status:", response.status_code)
    print("Analyze response:", response.json())
else:
    print("\nNo token received — login failed.")