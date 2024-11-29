import streamlit as st
import os
import io
import qrcode
from PIL import Image

# Sample data for medicines and eco-friendly products
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': "C:/Users/shara/OneDrive/Desktop/WhatsApp Image 2024-11-29 at 22.09.50_edb34354.jpg"},
        {'name': 'Ibuprofen', 'cost': 30, 'image': "C:/Users/shara/OneDrive/Desktop/WhatsApp Image 2024-11-29 at 22.09.50_edb34354.jpg"},
    ],
    'Eco-Friendly Products': [
        {'name': 'Bamboo Toothbrush', 'cost': 10, 'image': "C:/Users/shara/OneDrive/Desktop/WhatsApp Image 2024-11-29 at 22.09.50_edb34354.jpg"},
        {'name': 'Reusable Straw', 'cost': 5, 'image': "C:/Users/shara/OneDrive/Desktop/WhatsApp Image 2024-11-29 at 22.09.50_edb34354.jpg"},
    ]
}

# Function to display products
def display_products(products):
    for category, items in products.items():
        st.header(category)
        for item in items:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if os.path.exists(item['image']):
                    st.image(item['image'], width=150)
                else:
                    st.warning(f"Image not found for {item['name']}")
            with col2:
                st.write(item['name'])
                st.write(f"Price: ₹{item['cost']}")
            with col3:
                if st.button(f"Add to Cart ({item['name']})"):
                    st.session_state.cart.append(item)
                    st.success(f"{item['name']} added to cart!")

# Function to show the cart
def show_cart():
    st.subheader("Your Cart")
    total_cost = 0  # Initialize total_cost
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

# Initialize session state for the cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.title("Medicines and Eco-Friendly Products Platform")

# Display products
display_products(products)

# Show cart and calculate total cost
total_cost = show_cart()

# User details and order confirmation
if st.button("Proceed to Buy"):
    st.subheader("Fill Your Details")
    name = st.text_input("Name", placeholder="Enter your name")
    contact_info = st.text_input("Contact Info", placeholder="Enter your contact details")
    address = st.text_area("Address", placeholder="Enter your delivery address")
    medical_report = st.file_uploader("Upload Medical Report (if any)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Confirm Order"):
        if name and contact_info and address and total_cost > 0:
            payment_link = f"http://example.com/pay?amount={total_cost}"
            qr_image = generate_qr(payment_link)
            st.image(qr_image, caption="Scan to Pay")
            st.success("Order Confirmed! Your QR Code for payment is shown above.")
            st.info(f"Total Payment: ₹{total_cost}")
            st.session_state.cart.clear()  # Clear cart after order confirmation
        else:
            st.warning("Please fill in all details and add items to your cart before confirming the order.")
