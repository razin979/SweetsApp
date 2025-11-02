import streamlit as st
import requests
import jwt

BASE_URL = "http://127.0.0.1:8000"

# --- Session management ---
if "token" not in st.session_state:
    st.session_state.token = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# --- Helpers ---
def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def handle_response(resp):
    if resp.status_code in (200, 201):
        st.success("Action successful")
        if resp.status_code == 201:
            st.rerun()
    else:
        try:
            error_detail = resp.json().get("detail", "Error")
            st.error(f"Error: {error_detail}")
        except Exception as e:
            st.error(f"Something went wrong: Status {resp.status_code}")

# --- Authentication ---
def register_ui():
    st.subheader("Register New User")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", max_chars=200)
    is_admin = st.checkbox("Register as Admin")
    if st.button("Register"):
        try:
            resp = requests.post(f"{BASE_URL}/api/auth/register", json={
                "email": email, "password": password, "is_admin": is_admin
            }, timeout=5)
            handle_response(resp)
        except requests.exceptions.ConnectionError:
            st.error("Backend server is not running")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def login_ui():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", max_chars=200)
    if st.button("Login"):
        try:
            resp = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": email, "password": password
            }, timeout=5)
            if resp.status_code == 200:
                token_data = resp.json()
                st.session_state.token = token_data["access_token"]
                payload = jwt.decode(token_data["access_token"], options={"verify_signature": False})
                st.session_state.is_admin = payload.get("is_admin", False)
                st.success("Logged in successfully")
                st.rerun()
            else:
                handle_response(resp)
        except requests.exceptions.ConnectionError:
            st.error("Backend server is not running")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def logout_ui():
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.is_admin = False
        st.success("Logged out")
        st.rerun()

# --- Main Dashboard ---
def dashboard():
    st.title("🍬 Sweets Shop")
    logout_ui()

    st.subheader("Available Sweets")
    query = st.text_input("Search by name or category")
    min_price = st.number_input("Min Price", min_value=0.0, step=1.0)
    max_price = st.number_input("Max Price", min_value=0.0, step=1.0)

    if st.button("Search"):
        params = {}
        if query:
            params["name"] = query
            params["category"] = query
        if min_price:
            params["min_price"] = min_price
        if max_price:
            params["max_price"] = max_price
        resp = requests.get(f"{BASE_URL}/api/sweets/search", headers=get_headers(), params=params)
    else:
        resp = requests.get(f"{BASE_URL}/api/sweets", headers=get_headers())

    if resp.status_code == 200:
        sweets = resp.json()
        for sweet in sweets:
            with st.container(border=True):
                st.markdown(f"### {sweet['name']}")
                st.write(f"**Category:** {sweet['category']}")
                st.write(f"**Price:** ₹{sweet['price']}")
                st.write(f"**Quantity:** {sweet['quantity']}")
                if sweet['quantity'] <= 0:
                    st.button("Out of Stock", disabled=True, key=sweet['id'])
                else:
                    if st.button("Purchase", key=f"p-{sweet['id']}"):
                        p = requests.post(f"{BASE_URL}/api/sweets/{sweet['id']}/purchase", headers=get_headers())
                        handle_response(p)
                        st.rerun()

    else:
        st.error("Unable to fetch sweets")

    # --- Admin Section ---
    if st.session_state.is_admin:
        st.markdown("---")
        st.subheader("🛠️ Admin Panel")

        tabs = st.tabs(["Add Sweet", "Update Sweet", "Delete Sweet", "Restock Sweet"])

        # Add Sweet
        with tabs[0]:
            name = st.text_input("Name", key="add_name")
            category = st.text_input("Category", key="add_cat")
            price = st.number_input("Price", min_value=0.0, key="add_price")
            qty = st.number_input("Quantity", min_value=0, key="add_qty")
            if st.button("Add Sweet"):
                data = {"name": name, "category": category, "price": price, "quantity": qty}
                resp = requests.post(f"{BASE_URL}/api/sweets", headers=get_headers(), json=data)
                handle_response(resp)
                st.rerun()

        # Update Sweet
        with tabs[1]:
            sweet_id = st.text_input("Sweet ID to Update")
            name = st.text_input("New Name")
            category = st.text_input("New Category")
            price = st.number_input("New Price", min_value=0.0)
            qty = st.number_input("New Quantity", min_value=0)
            if st.button("Update Sweet"):
                data = {"name": name, "category": category, "price": price, "quantity": qty}
                resp = requests.put(f"{BASE_URL}/api/sweets/{sweet_id}", headers=get_headers(), json=data)
                handle_response(resp)
                st.rerun()

        # Delete Sweet
        with tabs[2]:
            sweet_id = st.text_input("Sweet ID to Delete")
            if st.button("Delete Sweet"):
                resp = requests.delete(f"{BASE_URL}/api/sweets/{sweet_id}", headers=get_headers())
                handle_response(resp)
                st.rerun()

        # Restock Sweet
        with tabs[3]:
            sweet_id = st.text_input("Sweet ID to Restock")
            qty = st.number_input("Restock Quantity", min_value=1)
            if st.button("Restock"):
                resp = requests.post(f"{BASE_URL}/api/sweets/{sweet_id}/restock", headers=get_headers(), params={"quantity": qty})
                handle_response(resp)
                st.rerun()

# --- Routing ---
st.sidebar.title("🍭 Sweets App")
if not st.session_state.token:
    page = st.sidebar.radio("Menu", ["Login", "Register"])
    if page == "Login":
        login_ui()
    else:
        register_ui()
else:
    dashboard()
