import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io

# Sample data for medicines and eco-friendly products
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Ibuprofen', 'cost': 30, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Aspirin', 'cost': 15, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Cetirizine', 'cost': 25, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Amoxicillin', 'cost': 50, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Antacid', 'cost': 40, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
    ],
    'Eco-Friendly Products': [
        {'name': 'Bamboo Toothbrush', 'cost': 100, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Reusable Straw', 'cost': 50, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Cloth Bag', 'cost': 80, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Recycled Paper Notebook', 'cost': 120, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Compostable Cups', 'cost': 70, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
        {'name': 'Eco-friendly Water Bottle', 'cost': 150, 'image': "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."},
    ]
}

# Function to display products
def display_products(products):
    for category, items in products.items():
        st.header(category)
        for i in range(0, len(items), 2):
            cols = st.columns(2)  # Create 2 columns
            for j in range(2):
                if i + j < len(items):
                    item = items[i + j]
                    with cols[j]:
                        st.image(item['image'], width=150)
                        st.write(f"{item['name']}")
                        st.write(f"Price: ₹{item['cost']}")
                        if st.button('Add to Cart', key=item['name']):
                            st.session_state.cart.append(item)
                            st.success(f"{item['name']} added to cart!")

# Function to show cart
def show_cart():
    st.subheader("Your Cart")
    total_cost = 0
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₹{item['cost']}")
            total_cost += item['cost']
        st.write(f"Total: ₹{total_cost}")
    return total_cost

# Function to generate QR code for payment
def generate_qr(payment_link):
    qr = qrcode.make(payment_link)
    buf = io.BytesIO()
    qr.save(buf)
    buf.seek(0)
    return Image.open(buf)

# Initialize session state for cart, process flow, and user details
if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'proceed_to_buy' not in st.session_state:
    st.session_state.proceed_to_buy = False

if 'user_details' not in st.session_state:
    st.session_state.user_details = {
        'name': '',
        'contact_info': '',
        'address': '',
        'medical_report': None
    }

st.title("Medicines and Eco-Friendly Products Platform")

# Display products
display_products(products)

# Show cart and get total cost
total_cost = show_cart()

# User details and order confirmation
if st.session_state.proceed_to_buy:
    st.subheader("Fill Your Details")
    st.session_state.user_details['name'] = st.text_input("Name", value=st.session_state.user_details['name'])
    st.session_state.user_details['contact_info'] = st.text_input("Contact Info", value=st.session_state.user_details['contact_info'])
    st.session_state.user_details['address'] = st.text_area("Address", value=st.session_state.user_details['address'])
    st.session_state.user_details['medical_report'] = st.file_uploader("Upload Medical Report (if any)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Confirm Order"):
        if (
            st.session_state.user_details['name']
            and st.session_state.user_details['contact_info']
            and st.session_state.user_details['address']
            and total_cost > 0
        ):
            payment_link = f"http://example.com/pay?amount={total_cost}"
            qr_image = generate_qr(payment_link)
            st.image(qr_image)
            st.success("Order Confirmed! Your QR Code for payment is shown above.")
            st.session_state.cart.clear()
            st.session_state.proceed_to_buy = False
        else:
            st.warning("Please fill in all details and add items to your cart before confirming the order.")
else:
    if st.button("Proceed to Buy"):
        if total_cost > 0:
            st.session_state.proceed_to_buy = True
        else:
            st.warning("Your cart is empty. Please add items before proceeding.")
