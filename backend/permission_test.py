import requests

BASE_URL = "http://127.0.0.1:8000/api"

CREDENTIALS = {
    "admin": {
        "username": "Pravin",
        "password": "Pravin@2204"
    },
    "manager": {
        "username": "Manager2",
        "password": "Test@1234"
    },
    "employee": {
        "username": "Employee1",
        "password": "Test@1234"
    }
}

IDS = {
    "task_own": 1,
    "task_other": 2,
    "project_own": 1,
    "project_other": 2,
    "employee_other": 3,
}


def get_token(role):
    url = f"{BASE_URL}/accounts/auth/login/"
    response = requests.post(url, json=CREDENTIALS[role])

    if response.status_code != 200:
        print(f"❌ Login failed for {role}")
        print(response.text)
        return None

    return response.json()["access"]


TOKENS = {
    role: get_token(role) for role in CREDENTIALS
}


def make_request(role, method, endpoint, data=None):
    url = f"{BASE_URL}/work{endpoint}"
    headers = {
        "Authorization": f"Bearer {TOKENS[role]}",
        "Content-Type": "application/json"
    }

    response = requests.request(method, url, json=data, headers=headers)

    print(f"\n[{role.upper()}] {method} {endpoint}")
    print(f"Status: {response.status_code}")
    try:
        print("Response:", response.json())
    except:
        print("Response:", response.text)

    return response


# =========================
# EMPLOYEE TESTS
# =========================

def test_employee():
    print("\n===== EMPLOYEE TESTS =====")

    make_request("employee", "GET",
        f"/projects/{IDS['project_other']}/tasks/"
    )

    make_request("employee", "PATCH",
        f"/projects/{IDS['project_other']}/tasks/{IDS['task_other']}/",
        {"title": "HACKED"}
    )


# =========================
# MANAGER TESTS
# =========================

def test_manager():
    print("\n===== MANAGER TESTS =====")

    make_request("manager", "GET",
        f"/projects/{IDS['project_other']}/"
    )

    make_request("manager", "PATCH",
        f"/projects/{IDS['project_other']}/tasks/{IDS['task_other']}/",
        {"assignee": IDS["employee_other"]}
    )

    make_request("manager", "GET", "/assignments/")


# =========================
# ADMIN TESTS
# =========================

def test_admin():
    print("\n===== ADMIN TESTS =====")

    make_request("admin", "GET",
        f"/projects/{IDS['project_other']}/tasks/"
    )

    make_request("admin", "PATCH",
        f"/projects/{IDS['project_other']}/tasks/{IDS['task_other']}/",
        {"title": "ADMIN_UPDATE"}
    )

    make_request("admin", "GET", "/projects/")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    test_employee()
    test_manager()
    test_admin()