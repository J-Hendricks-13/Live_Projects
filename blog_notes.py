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
def page_oop_notes():
    """Consolidated notes on OOP principles (Abstraction, Encapsulation, Inheritance)
       and their relation to APIs and the Vehicle example."""
    
    st.header("OOP Principles: Notes & API Connection 🧠")
    st.markdown("These notes summarize the core Object-Oriented Programming (OOP) concepts and how they relate to designing robust APIs and code structures.")

    st.markdown("---")

    ## 1. Abstraction and the API Interface
    st.subheader("1. Abstraction and the Interface (The 'What')")
    
    st.markdown("""
    **Abstraction** is the principle of showing only **essential information** to the user and hiding the complex background details.
    
    * **The Interface/API:** In programming, the **Interface** is the public contract that defines **what** an object can do (the methods and attributes it exposes).
    * **The Dot Operator (`.`):** When you type `my_object.` in your IDE, the dropdown list that appears **is the interface** (or API) for that object. It shows you the public functions you are allowed to call (e.g., `.start_engine()`, `.get_info()`). 
    * **API Connection:** A **REST API** (like goRest) is the ultimate form of abstraction, exposing endpoints (`/users`) that define what actions you can perform (`GET`, `POST`) without showing you the server's database code.
    """)
    
    st.markdown("---")

    ## 2. Encapsulation
    st.subheader("2. Encapsulation (Hiding the 'How')")

    st.markdown("""
    **Encapsulation** is the binding of data (attributes) and the methods (functions) that operate on that data into a single unit (the class), and **hiding the internal state**.
    
    * **Goal:** Protect the data from being accidentally changed by external code and ensure it is only modified through controlled public methods.
    * **Vehicle Example:** In our `Car` class, the `self._is_running` attribute is an internal detail.
        * It is marked with a single underscore (`_is_running`) in Python to indicate it's **private/protected** (though Python doesn't strictly enforce it).
        * The only way to change its value is through the public API method: `my_car.start_engine()`. This prevents outside code from putting the car in an invalid state.
    """)
    st.code("""
class Car(Vehicle):
    def __init__(self, make, model):
        # Hidden internal detail (Encapsulated)
        self._is_running = False 
        ...
    
    # Public method (API) that controls the internal state
    def start_engine(self):
        self._is_running = True
        ...
""", language='python')
    
    st.markdown("---")

    ## 3. Inheritance and Coupling
    st.subheader("3. Inheritance and Coupling (The 'Depends On' Rule)")

    st.markdown("""
    **Inheritance** allows a new class (subclass) to take on the properties and methods of an existing class (parent class). This is vital for code reuse and defining hierarchies.
    
    * **Vehicle Example:** The concrete **`Car`** and **`Truck`** classes **inherit** from the abstract **`Vehicle`** interface.
    * **Low Coupling is Key:** To build maintainable systems, we follow the **Dependency Inversion Principle**, which is: **Program to an interface, not an implementation.** 
        * **Good Practice (Low Coupling):** Inherit from the **Abstract Interface** (`Vehicle`). Your code relies only on the public contract (`start_engine` exists), not on any concrete implementation details.
        * **Bad Practice (High Coupling):** Inherit from a **Concrete Class** (`Car`). Any internal change to `Car` (even a renaming of a private variable) can break your new inherited class, creating a fragile system.
    """)
    
    st.markdown("---")
    st.caption("These principles ensure our API-driven applications are flexible, scalable, and easy to maintain over time.")

# --- MAIN APP LOGIC ---

st.sidebar.title("Concepts to Explore")
page_selection = st.sidebar.selectbox(
    "Select a Core Concept to Explore:",
    {
        "OOP Notes": "0. OOP Principles Notes 📝",
        "API Concepts": "Introduction to REST & CRUD",        
        "API Dissection": "4. API Dissection: Headers & Body 🔍"
    }
)

# Render the selected page
if page_selection == "API Concepts":
    intro_page()
elif page_selection == "OOP Notes": # <-- ADDED NEW CONDITION
    page_oop_notes()
elif page_selection == "API Dissection":
    page_dissection_full() # Calling the new detailed function

st.sidebar.divider()

st.sidebar.caption("Powered by Streamlit and GoREST API.")
