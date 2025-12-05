import streamlit as st
import requests
import pandas as pd
import json
import urllib.parse
import uuid 

# --- CONFIGURATION ---
BASE_URL = "https://gorest.co.in/public/v2"

# NOTE: To test POST/PUT/DELETE, you MUST replace this with your valid token.
API_TOKEN = "YOUR_GOREST_API_TOKEN" 
HEADERS_AUTH = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}


# Set Streamlit Page Configuration
st.set_page_config(
    page_title="API Request Constructor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UTILITY FUNCTIONS: REQUEST VISUALIZATION & API CALLS ---

def display_request_components(method, endpoint, params=None, headers=None, body=None):
    """Displays the key components of the API request in a structured format."""
    full_url = f"{BASE_URL}/{endpoint}" if not endpoint.startswith("http") else endpoint
    
    st.subheader(f"Request Details ({method})")
    
    # Build URL including parameters for display purposes
    if params:
        query_string = urllib.parse.urlencode(params)
        url_display = f"{full_url}?{query_string}"
    else:
        url_display = full_url

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Method**")
        st.code(method)
        st.markdown("**Base URL**")
        st.code(BASE_URL)
        st.markdown("**Endpoint**")
        st.code(endpoint)
    
    with col2:
        st.markdown("**Full Request URL**")
        st.code(url_display, language='url')
        
        st.markdown("**Headers**")
        if headers:
            st.json(headers)
        else:
            st.markdown("`{}` (No special headers required)")
            
        st.markdown("**Body (Payload)**")
        if body:
            st.json(body)
        else:
            st.markdown("`{}` (No body required for GET/DELETE)")
    st.markdown("---")


@st.cache_data(ttl=600)
def fetch_data(endpoint, params=None):
    """Handles GET requests and error checking (specifically for educational pages)."""
    full_url = f"{BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(full_url, params=params, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        headers = {
            'Status Code': response.status_code,
            'Content-Type': response.headers.get('content-type'),
            'Total Pages': response.headers.get('x-pagination-pages', 'N/A'),
            'Current Page': response.headers.get('x-pagination-page', 'N/A'),
            'Total Items': response.headers.get('x-pagination-total', 'N/A')
        }
        
        return data, headers
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from the API: {e}")
        return None, {'Status Code': response.status_code if 'response' in locals() else 'N/A'}
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None, None


# --- PAGE FUNCTIONS ---

def intro_page():
    """Introduction and definition of REST APIs, including CRUD and OOP mapping."""
    st.header("Welcome to the API Education Simulator 🎓")
    st.markdown("""
    This interactive tool uses the **goRest API** to demonstrate fundamental concepts of how **R**epresentational **E**state **T**ransfer (**REST**) APIs work.
    
    Use the sidebar to explore different types of requests and concepts.
    """)
    
    st.subheader("The Four Core API Actions (CRUD)")
    st.markdown("""
    The behavior of almost all REST APIs is defined by four fundamental operations, collectively known as **CRUD** (Create, Read, Update, Delete). The GoRest API maps these actions to HTTP methods:
    """)

    st.table(pd.DataFrame({
        'HTTP Method': ['POST', 'GET', 'PUT | PATCH', 'DELETE'],
        'Endpoint Example': ['/public/v2/users', '/public/v2/users/7662336', '/public/v2/users/7662336', '/public/v2/users/7662336'],
        'Action': ['Create a new user', 'Get user details', 'Update user details', 'Delete user']
    }))
    
    st.subheader("💡 Connecting APIs to OOP Concepts (Constructors, Getters, Setters)")
    st.markdown("""
    You can relate these API actions to methods in **Object-Oriented Programming (OOP)**, where a resource (like a User object) is managed:
    
    * **POST (Create)** is like a **Constructor** or **Factory Method**.
    * **GET (Read)** is like a **Getter Method** (`getUserDetails()`).
    * **PUT/PATCH (Update)** is like a **Setter Method** (`setUserName()`).
    * **DELETE** is like a dedicated **Destructor** or **Delete Function**.
    """)
    st.markdown("---")

def page_get_all():
    """Demonstrates a simple GET request for a list of resources."""
    st.header("1. Core Concept: The GET Request (Read / Getter)")
    st.markdown("""
    The **GET** method is used to **retrieve** data. This is the API equivalent of calling a **Getter Method** on a collection.
    
    * **Action**: Read (safe/idempotent).
    * **Request Components**: Only the URL and Method are minimally required.
    """)
    
    if st.button('Execute Simple GET Request', key='get_all_btn', type="primary"):
        st.info("Constructing Request...")
        display_request_components(method='GET', endpoint='users')
        
        with st.spinner("Executing GET request..."):
            data, headers = fetch_data("users")
            
            if data:
                st.subheader("API Response Data")
                df = pd.DataFrame(data)
                st.dataframe(df[['id', 'name', 'email', 'gender', 'status']], use_container_width=True)
                
                st.subheader("HTTP Response Details")
                st.json(headers)
                
                with st.expander("View Raw JSON Payload"):
                    st.json(data)
                
                st.session_state['data_get_all'] = data 
                st.session_state['headers_get_all'] = headers

def page_resource_id():
    """Demonstrates retrieving a single resource by ID."""
    st.header("2. Core Concept: Resource Identification (GET by ID)")
    st.markdown("""
    To get a **specific item**, the unique identifier is embedded in the **URL path**. This is a **Path Parameter**.
    * **Endpoint Format:** `/users/{id}`
    * **Request Components**: The specific ID changes the URL path.
    """)
    
    selected_id = 6858200
    st.markdown(f"**We will test fetching User ID:** `{selected_id}`")

    if st.button(f'Execute GET Request for ID {selected_id}', key='get_id_btn', type="primary"):
        st.info("Constructing Request...")
        display_request_components(method='GET', endpoint=f"users/{selected_id}")
        
        with st.spinner(f"Executing GET request for ID {selected_id}..."):
            data, headers = fetch_data(f"users/{selected_id}")
            
            if data:
                st.subheader("API Response Data (Single Object)")
                st.json(data)
                
                st.subheader("HTTP Response Details")
                st.json(headers)

def page_pagination():
    """Demonstrates using Query Parameters for filtering and pagination."""
    st.header("3. Core Concept: Query Parameters (Pagination)")
    st.markdown("""
    **Query Parameters** are used to filter, sort, or limit data. They are key-value pairs appended to the URL after a `?`.
    
    * **Endpoint with Query:** `/users?page=X&per_page=Y`
    * **Request Components**: Parameters are passed via the `params` argument in Python.
    """)
    
    st.subheader("Interactive Pagination Test")
    col1, col2 = st.columns(2)
    
    with col1:
        page_num = st.number_input('Page Number:', min_value=1, value=1, step=1)
    with col2:
        per_page_count = st.selectbox('Users Per Page:', [5, 10, 20])

    if st.button('Execute Paginating GET Request', key='get_pagination_btn', type="primary"):
        params = {"page": page_num, "per_page": per_page_count}
        
        st.info("Constructing Request...")
        display_request_components(method='GET', endpoint='users', params=params)
        
        with st.spinner("Executing GET request with parameters..."):
            data, headers = fetch_data("users", params=params)
            
            if data:
                st.subheader("API Response Data")
                df = pd.DataFrame(data)
                st.dataframe(df[['id', 'name', 'email', 'gender', 'status']], use_container_width=True)
                
                st.subheader("HTTP Response Details (Note Pagination Headers!)")
                st.json(headers)

# --- NEW PAGE: DETAILED HEADERS & BODY DISSECTION ---

def page_dissection_full():
    """Explains the origin of the headers and body components using the user's specific text."""
    st.header("4. API Dissection: Where Headers & Body Come From 🔍")
    st.markdown("""
    The **Headers** and **Body** in an API request aren't just arbitrary JSON; they are essential pieces of information dictated by the client's needs and the server's requirements.
    """)
    st.markdown("---")
    
    # --- Headers Section ---
    st.subheader("1. ⚙️ Where the Headers Came From")
    st.markdown("Headers are metadata about the request itself. In our POST example, we needed two primary headers, which were determined by the **goRest API Documentation** and the **HTTP Protocol standards**:")

    st.markdown("### A. Authorization Header")
    st.markdown("* **Header:** `Authorization: Bearer YOUR_GOREST_API_TOKEN`")
    st.markdown("* **Purpose:** This header tells the server **who you are** and that you have permission to perform an action that changes data (like creating a user). Since `GET` requests usually read public data, they often don't need this, but `POST`, `PUT`, and `DELETE` almost always do.")
    st.markdown("* **Source:** We got the structure (`Bearer [Token]`) directly from the **goRest API Documentation**. We implemented this in the script with the dictionary:")
    st.code("HEADERS_AUTH = {'Authorization': f'Bearer {API_TOKEN}', ...}", language='python')

    st.markdown("### B. Content-Type Header")
    st.markdown("* **Header:** `Content-Type: application/json`")
    st.markdown("* **Purpose:** This header tells the server **what format the data in the Body is in**. Since we are sending a JSON object in the request Body, we must declare the content type as `application/json`.")
    st.markdown("* **Source:** This is an **HTTP standard** required whenever you send structured data to a server.")

    st.markdown("---")

    # --- Body Section ---
    st.subheader("2. 🧱 Where the Body Came From")
    st.markdown("The Body (or Payload) contains the actual data you want the server to process.")

    st.markdown("### A. The Data Schema (Fields)")
    st.markdown("* **Purpose:** To define the new resource you want to create (e.g., a new user with `name`, `gender`, `email`, and `status`).")
    st.markdown("* **Source:** We got the required fields and their expected data types directly from the **goRest API Documentation for the POST /users endpoint**.")
    st.code("""
    # Example Required Fields (from goRest Documentation)
    {
        "name": "...",
        "gender": "...",
        "email": "...",
        "status": "..."
    }
    """, language='json')
    st.markdown("> **Note:** If you leave out a required field, the API will definitely throw an error (often a 422 Unprocessable Entity).")

    st.markdown("### B. The Structure (JSON Format)")
    st.markdown("* **Structure:** We use Python dictionaries converted to the JSON string format.")
    st.markdown("* **Source:** The JSON format (`key: value` pairs enclosed in braces `{}`) is the **standard format** for sending data in most modern REST APIs.")
    
    st.markdown("---")
    st.markdown("In short, when making an API call, you must always look at the **external API's documentation** to learn exactly which **Headers** (metadata) and **Body fields** (data) are required.")


# --- END OF NEW PAGE ---

def page_example_request():
    """Demonstrates a fully formed POST request with pre-filled fields."""
    st.header("5. API Example: POST Request (Create / Constructor)")
    st.markdown("""
    This example demonstrates a **POST** request. Notice that this requires both **Headers** (for authorization and content type) and a **Body** (the data to be created).
    """)
    
    # --- Pre-filled Fields ---
    method = "POST"
    endpoint = "users"
    
    unique_name = f"TestUser_{uuid.uuid4().hex[:6]}"
    example_email = f"test_{uuid.uuid4().hex[:10]}@example.com"
    
    example_headers = json.dumps(HEADERS_AUTH, indent=4)
    example_body = json.dumps({
        "name": unique_name,
        "gender": "male",
        "email": example_email,
        "status": "active"
    }, indent=4)

    st.subheader("Request Setup (Pre-filled)")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.text_input("HTTP Method:", method, disabled=True)
    with col2:
        st.text_input("Endpoint:", endpoint, disabled=True)
        
    st.code(f"Headers:\n{example_headers}", language='json')
    st.code(f"Body (Payload):\n{example_body}", language='json')

    # --- Execution Button ---
    if st.button(f"Execute {method} Request (Requires Valid API Key)", type="primary"):
        full_url = f"{BASE_URL}/{endpoint}"
        
        if API_TOKEN == "YOUR_GOREST_API_TOKEN":
            st.error("Cannot execute POST request. Please replace 'YOUR_GOREST_API_TOKEN' in the script with a valid token.")
            return

        st.info("Constructing Request...")
        display_request_components(method=method, endpoint=endpoint, 
                                   headers=HEADERS_AUTH, body=json.loads(example_body))

        with st.spinner(f"Executing POST request to {endpoint}..."):
            try:
                response = requests.post(full_url, headers=HEADERS_AUTH, json=json.loads(example_body), timeout=10)
                
                st.subheader("API Response")
                st.metric("HTTP Status Code", response.status_code)
                
                try:
                    res_data = response.json()
                    st.json(res_data)
                except json.JSONDecodeError:
                    st.warning("Response was not valid JSON.")
                    st.code(response.text)

                with st.expander("View Full Response Headers"):
                    st.json(dict(response.headers))

            except requests.exceptions.RequestException as e:
                st.error(f"Error during request execution: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


def page_playground():
    """Interactive page for testing custom API requests."""
    st.header("6. API Practice Playground 🧪")
    st.markdown("""
    Use this area to construct and execute your own custom API requests.
    
    **Important**: To successfully run **POST**, **PUT**, or **DELETE** requests, you must generate a **Personal Access Token** from the [goRest website](https://gorest.co.in/) and replace the `API_TOKEN` variable in the script.
    """)
    st.markdown("---")
    
    # --- Request Construction UI ---
    col1, col2 = st.columns([1, 3])
    with col1:
        method = st.selectbox("HTTP Method:", ["GET", "POST", "PUT", "DELETE"])
    with col2:
        endpoint = st.text_input("Endpoint (e.g., users or users/ID):", "users")
    
    # Headers Input (for authorization/content type)
    headers_json = st.text_area("Headers (JSON format):", 
                                '{}', 
                                help="For POST/PUT, you usually need 'Content-Type: application/json' and 'Authorization' header.")
    
    # Body Input (for POST/PUT)
    body_json = st.text_area("Body (JSON format):", 
                             '{}', 
                             help="Required for POST (Create) and PUT/PATCH (Update).")

    # --- Execution Button ---
    if st.button(f"Execute {method} Request", type="primary"):
        full_url = f"{BASE_URL}/{endpoint}"
        
        # 1. Parse Inputs
        try:
            req_headers = json.loads(headers_json)
            req_body = json.loads(body_json) if body_json.strip() and method in ["POST", "PUT", "PATCH"] else None
        except json.JSONDecodeError:
            st.error("Invalid JSON format in Headers or Body. Please fix the syntax.")
            return

        # Inject Authorization Header if necessary for goRest
        if method != "GET" and "Authorization" not in req_headers and API_TOKEN != "YOUR_GOREST_API_TOKEN":
             req_headers.update(HEADERS_AUTH)

        # 2. Display the Request Components
        st.info("Constructing Request...")
        display_request_components(method=method, endpoint=endpoint, headers=req_headers, body=req_body)

        # 3. Execute Request
        with st.spinner(f"Executing {method} request to {endpoint}..."):
            try:
                if method == "GET":
                    response = requests.get(full_url, headers=req_headers, timeout=10)
                elif method == "POST":
                    response = requests.post(full_url, headers=req_headers, json=req_body, timeout=10)
                elif method == "PUT":
                    response = requests.put(full_url, headers=req_headers, json=req_body, timeout=10)
                elif method == "DELETE":
                    response = requests.delete(full_url, headers=req_headers, timeout=10)
                else:
                    st.error("Invalid HTTP method selected.")
                    return

                # 4. Display Results
                st.subheader("API Response")
                st.metric("HTTP Status Code", response.status_code)
                
                try:
                    res_data = response.json()
                    st.json(res_data)
                except json.JSONDecodeError:
                    st.warning("Response was not valid JSON (e.g., DELETE often returns an empty body or simple text).")
                    st.code(response.text)

                # Show response headers
                with st.expander("View Full Response Headers"):
                    st.json(dict(response.headers))

            except requests.exceptions.RequestException as e:
                st.error(f"Error during request execution: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


# --- MAIN APP LOGIC ---

st.sidebar.title("API Concepts")
page_selection = st.sidebar.selectbox(
    "Select a Core Concept to Explore:",
    {
        "Intro": "Introduction to REST & CRUD",
        "GET List": "1. GET Request (Read / Getter)",
        "GET ID": "2. Path Parameters (Single Item)",
        "GET Query": "3. Query Parameters (Pagination)",
        "Dissection": "4. API Dissection: Headers & Body 🔍",
        "Example POST": "5. API Example: POST Request ✏️",
        "Playground": "6. API Practice Playground 🧪"
    }
)

# Render the selected page
if page_selection == "Intro":
    intro_page()
elif page_selection == "GET List":
    page_get_all()
elif page_selection == "GET ID":
    page_resource_id()
elif page_selection == "GET Query":
    page_pagination()
elif page_selection == "Dissection":
    page_dissection_full() # Calling the new detailed function
elif page_selection == "Example POST":
    page_example_request()
elif page_selection == "Playground":
    page_playground()

st.sidebar.divider()
st.sidebar.caption("Powered by Streamlit and GoREST API.")