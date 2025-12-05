import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd

st.set_page_config(layout="wide", page_title="OOP Design Patterns Simulator")
st.title("OOP Design Patterns & API Principles Simulator 🧠")
st.markdown("This application demonstrates how four fundamental design patterns implement **Abstraction** and **Polymorphism** to achieve **Low Coupling**.")
st.markdown("---")

# =========================================================================
# 1. CREATIONAL — FACTORY PATTERN
# =========================================================================

## Factory Pattern Classes
class Document(ABC):
    """ABSTRACT INTERFACE (The Contract / API)"""
    @abstractmethod
    def render(self):
        pass

class PDFDocument(Document):
    """CONCRETE PRODUCT 1 (The Implementation)"""
    def render(self):
        return "PDF Document Created (Uses PDF Engine Logic)"

class WordDocument(Document):
    """CONCRETE PRODUCT 2 (The Implementation)"""
    def render(self):
        return "Word Document Created (Uses DOCX Engine Logic)"

class DocumentFactory:
    """CREATOR (The Factory)"""
    @staticmethod
    def create(doc_type):
        if doc_type == "PDF":
            return PDFDocument()
        elif doc_type == "WORD":
            return WordDocument()
        else:
            return None

st.header("1. Creational: Factory Pattern 🏭")
st.markdown("The Factory Pattern handles **object creation** for you. The client code asks for a generic 'Document' and the Factory decides which **concrete class** (`PDFDocument` or `WordDocument`) to return.")


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Simulate Creation")
    doc_type = st.selectbox("Choose a document type", ["PDF", "WORD"])
    
    if st.button("Create Document & Render"):
        doc = DocumentFactory.create(doc_type)
        st.success(f"Output: {doc.render()}")
        
        st.markdown("**Code Analysis:**")
        st.code(f"""
# Client Code only uses the Interface/Factory
doc = DocumentFactory.create("{doc_type}")
doc.render() # Polymorphism
""", language='python')

with col2:
    st.subheader("Key OOP Principle")
    st.markdown("* **Abstraction:** The client code (the button logic) only knows about the **`Document`** interface and the **`DocumentFactory`**. It never uses `PDFDocument()` directly.")
    st.markdown("* **Low Coupling:** If you add a new `ExcelDocument` class, the client code (the button logic) **does not need to change**, only the `DocumentFactory` needs a small update.")

st.markdown("---")


# =========================================================================
# 2. STRUCTURAL — DECORATOR PATTERN
# =========================================================================

## Decorator Pattern Classes
class Invoice:
    """COMPONENT (The Base Object)"""
    def print(self):
        return "Base Invoice"

class Decorator(Invoice):
    """DECORATOR BASE (Wraps the object)"""
    def __init__(self, invoice):
        self.invoice = invoice
        
    def print(self):
        # Delegate the call to the wrapped component
        return self.invoice.print() 

class WatermarkDecorator(Decorator):
    """CONCRETE DECORATOR 1 (Adds behavior before or after)"""
    def print(self):
        return self.invoice.print() + " + Watermark"

class LoggingDecorator(Decorator):
    """CONCRETE DECORATOR 2 (Adds behavior before or after)"""
    def print(self):
        return self.invoice.print() + " + Logging"

st.header("2. Structural: Decorator Pattern 🎁")
st.markdown("The Decorator Pattern lets you **attach new behaviors** to an object dynamically without modifying its core class. It's like wrapping a gift with new features.")


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Simulate Layering")
    invoice = Invoice()
    add_watermark = st.checkbox("Add Watermark", key="wm_chk")
    add_logging = st.checkbox("Add Logging", key="log_chk")

    if st.button("Generate Invoice"):
        final = invoice
        if add_watermark:
            final = WatermarkDecorator(final)
        if add_logging:
            final = LoggingDecorator(final)
        st.success(f"Invoice Output: {final.print()}")
        
        st.markdown("**Code Analysis:**")
        st.code(f"""
# Example layering:
final = WatermarkDecorator(Invoice()) 
# final now has the 'Watermark' feature, but still uses the same 'print' API.
""", language='python')

with col2:
    st.subheader("Key OOP Principle")
    st.markdown("* **Polymorphism:** The final object, regardless of how many decorators are wrapped around it (`final`), still responds to the **same API method** (`final.print()`).")
    st.markdown("* **Open/Closed Principle:** The original `Invoice` class never had to be changed (closed for modification), but we easily extended its functionality (open for extension).")
    
st.markdown("---")


# =========================================================================
# 3. BEHAVIORAL — STRATEGY PATTERN
# =========================================================================

## Strategy Pattern Classes
class PricingStrategy(ABC):
    """STRATEGY INTERFACE (The Contract / API for algorithms)"""
    @abstractmethod
    def calculate(self, price):
        pass

class DiscountStrategy(PricingStrategy):
    """CONCRETE STRATEGY 1 (The Implementation)"""
    def calculate(self, price):
        # Implementation 1: 20% off
        return price * 0.8

class DynamicStrategy(PricingStrategy):
    """CONCRETE STRATEGY 2 (The Implementation)"""
    def calculate(self, price):
        # Implementation 2: 10% premium
        return price * 1.1

class PricingContext:
    """CONTEXT (Uses the Strategy interface)"""
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_price(self, base):
        # Delegates the specific calculation to the strategy object
        return self.strategy.calculate(base)

st.header("3. Behavioral: Strategy Pattern ♟️")
st.markdown("The Strategy Pattern defines a **family of interchangeable algorithms** and makes them accessible via a common interface. It allows the **Context** (`PricingContext`) to switch behaviors at runtime.")


col1, col2 = st.columns([1, 2])
BASE_PRICE = 100

with col1:
    st.subheader("Simulate Behavior Change")
    base_price = st.number_input("Base Price", value=BASE_PRICE)
    strategy_select = st.selectbox("Pricing Strategy", ["Discount (80% Final)", "Dynamic (110% Final)"])

    if st.button("Calculate Price"):
        if strategy_select == "Discount (80% Final)":
            context = PricingContext(DiscountStrategy())
        else:
            context = PricingContext(DynamicStrategy())
        
        final_price = context.get_price(base_price)
        st.success(f"Final Price: ${final_price:,.2f}")
        
        st.markdown("**Code Analysis:**")
        st.code(f"""
# Client (Context) code:
context = PricingContext(SelectedStrategy())
context.get_price({BASE_PRICE}) 
# The context doesn't know *how* the price is calculated, 
# only that it must call the 'calculate' API.
""", language='python')

with col2:
    st.subheader("Key OOP Principle")
    st.markdown("* **Polymorphism:** The `PricingContext` always calls the same method (`strategy.calculate(base)`), but the actual code executed is different depending on whether the `DiscountStrategy` object or the `DynamicStrategy` object is plugged in.")
    st.markdown("* **Low Coupling:** The core `PricingContext` never has to be modified if you add a new `HolidayPricingStrategy`—you just plug the new strategy into the context.")

st.markdown("---")


# =========================================================================
# 4. STRUCTURAL — ADAPTER PATTERN
# =========================================================================

## Adapter Pattern Classes
class WeatherAPI(ABC):
    """TARGET INTERFACE (The unified API your client expects)"""
    @abstractmethod
    def get_data(self):
        # Client expects {'temperature': X, 'humidity': Y}
        pass

class OpenWeatherAPI:
    """ADAPTEE 1 (The incompatible API/Legacy Code)"""
    def fetch(self):
        # Incompatible structure: {"temp_c": 21, "humidity": 60}
        return {"temp_c": 21, "humidity": 60}

class AccuWeatherAPI:
    """ADAPTEE 2 (Another incompatible API)"""
    def retrieve(self):
        # Incompatible structure: {"temperature": 22, "hum": 58}
        return {"temperature": 22, "hum": 58}

class OpenWeatherAdapter(WeatherAPI):
    """ADAPTER 1 (Translates the incompatible method to the target interface)"""
    def __init__(self, api):
        self.api = api # Holds the adaptee object

    def get_data(self):
        # Translation logic: fetch() -> get_data() and rename/reformat keys
        raw = self.api.fetch() 
        return {"temperature": raw["temp_c"], "humidity": raw["humidity"]}

class AccuWeatherAdapter(WeatherAPI):
    """ADAPTER 2 (Translates another incompatible method)"""
    def __init__(self, api):
        self.api = api

    def get_data(self):
        # Translation logic: retrieve() -> get_data() and rename/reformat keys
        raw = self.api.retrieve()
        return {"temperature": raw["temperature"], "humidity": raw["hum"]}

st.header("4. Structural: Adapter Pattern 🔌")
st.markdown("The Adapter Pattern converts the **interface** of a class into another interface the client expects. It lets incompatible systems work together.")


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Simulate API Unification")
    weather_select = st.selectbox("Weather Source", ["OpenWeather (Incompatible Keys)", "AccuWeather (Incompatible Method)"])

    if st.button("Get Weather Data"):
        if "OpenWeather" in weather_select:
            adapter = OpenWeatherAdapter(OpenWeatherAPI())
        else:
            adapter = AccuWeatherAdapter(AccuWeatherAPI())
        
        data = adapter.get_data()
        st.success(f"Unified Output: {data}")
        
        st.markdown("**Code Analysis:**")
        st.code(f"""
# Client code always expects the unified API:
data = adapter.get_data() 
# The adapter hides whether 'fetch' or 'retrieve' was called internally.
# The keys are always 'temperature' and 'humidity'.
""", language='python')

with col2:
    st.subheader("Key OOP Principle")
    st.markdown("* **Target Interface:** The client (the button logic) only interacts with the **`WeatherAPI`** interface's method, **`get_data()`**.")
    st.markdown("* **Abstraction/Coupling:** The client is completely decoupled from the specific, ugly implementation details (like calling `fetch()` vs. `retrieve()` or renaming `temp_c` to `temperature`). The Adapter does the dirty work.")

st.markdown("---")