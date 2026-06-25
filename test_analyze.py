import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJlbWFpbCI6ImFraGlsQHRlc3QuY29tIiwiZXhwIjoxNzgxODg2Njk4fQ.gtfqtm2FLLBY5dqyUK2VxJE9jQ_1tw0JIIPME-9psNU"

response = requests.post(
    "http://localhost:8000/v1/reviews/analyze",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "review_text": "This product broke after one day, terrible quality",
        "rating": 5
    }
)

print(response.status_code)
print(response.json())