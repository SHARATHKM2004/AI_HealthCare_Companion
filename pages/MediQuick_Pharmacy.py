import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io

# Sample data for medicines and eco-friend
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': "https://www.google.com/imgres?q=paracetamol&imgurl=https%3A%2F%2F5.imimg.com%2Fdata5%2FSELLER%2FDefault%2F2022%2F9%2FQR%2FAF%2FMV%2F69966959%2Fparacip-paracetamol-650-tablet.jpg&imgrefurl=https%3A%2F%2Fwww.indiamart.com%2Fproddetail%2Fparacetamol-tablets-500-mg-26560013348.html&docid=yfHNNJS9mMsJsM&tbnid=RshYnZ-whyQHwM&vet=12ahUKEwjv0pC4u4KKAxWaXmwGHYfDAUkQM3oECBUQAA..i&w=2000&h=2000&hcb=2&ved=2ahUKEwjv0pC4u4KKAxWaXmwGHYfDAUkQM3oECBUQAA"},
        {'name': 'Ibuprofen', 'cost': 30, 'image': "https://www.google.com/imgres?q=ibuprofen&imgurl=https%3A%2F%2F5.imimg.com%2Fdata5%2FSELLER%2FDefault%2F2023%2F7%2F325863554%2FWI%2FJM%2FSY%2F135658020%2Fibuprofen-tablets-ip-200-mg-.jpg&imgrefurl=https%3A%2F%2Fwww.indiamart.com%2Fproddetail%2Fibuprofen-tablets-ip-200-mg-24994070188.html&docid=EV15jtRkSjP3hM&tbnid=_4j75MnXgJBMKM&vet=12ahUKEwit--fMu4KKAxXXTGcHHVR7I70QM3oECBgQAA..i&w=1987&h=1987&hcb=2&ved=2ahUKEwit--fMu4KKAxXXTGcHHVR7I70QM3oECBgQAA"},
    ],
    'Eco-Friendly Products': [
        {'name': 'Bamboo Toothbrush', 'cost': 10, 'image': "https://www.google.com/imgres?q=bamboo%20tooth%20brush&imgurl=https%3A%2F%2Ftoystorey.in%2Fwp-content%2Fuploads%2F2023%2F02%2FBamboo-Toothbrush-C-Shaped-5-scaled-1.jpg&imgrefurl=https%3A%2F%2Ftoystorey.in%2Fproduct%2Forganic-bamboo-toothbrush-soft-bristles-for-babies-pack-of-1%2F&docid=yS8Jb4bHpQ3iiM&tbnid=HKBEd0sb-UbriM&vet=12ahUKEwiGxOrcu4KKAxXWUGwGHVdtHGMQM3oECFIQAA..i&w=2560&h=2560&hcb=2&ved=2ahUKEwiGxOrcu4KKAxXWUGwGHVdtHGMQM3oECFIQAA"},
        {'name': 'Reusable Straw', 'cost': 5, 'image': "https://www.google.com/imgres?q=reusable%20straw&imgurl=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F71MDgPCH%2B6L.jpg&imgrefurl=https%3A%2F%2Fwww.amazon.in%2FReusable-Silicone-Straws-100-Straw-Openable-Compatible%2Fdp%2FB0888DML1J&docid=s-1_KrCH8umPqM&tbnid=DY8iu6iIvmE43M&vet=12ahUKEwjQjsbxu4KKAxVpTWwGHTwENKIQM3oECBcQAA..i&w=1500&h=1480&hcb=2&ved=2ahUKEwjQjsbxu4KKAxVpTWwGHTwENKIQM3oECBcQAA"},
    ]
}

# Function to display products
def display_products(products):
    for category, items in products.items():
        st.header(category)
        for item in items:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.image(item['image'], width=150)
            with col2:
                st.write(item['name'])
                st.write(f"Price: ₹{item['cost']}")
            with col3:
                if st.button('Add to Cart', key=item['name']):
                    st.session_state.cart.append(item)
                    st.success(f"{item['name']} added to cart!")

# Function to show cart
def show_cart():
    st.subheader("Your Cart")
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        total_cost = 0
        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₹{item['cost']}")
            total_cost += item['cost']
        st.write(f"Total: ₹{total_cost}")
    return total_cost  # Return the total cost for use later

# Function to generate QR code for payment
def generate_qr(payment_link):
    qr = qrcode.make(payment_link)
    buf = io.BytesIO()
    qr.save(buf)
    buf.seek(0)
    return Image.open(buf)

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.title("Medicines and Eco-Friendly Products Platform")

# Display products
display_products(products)

# Show cart and get total cost
total_cost = show_cart()

# User details and order confirmation
if st.button("Proceed to Buy"):
    st.subheader("Fill Your Details")
    name = st.text_input("Name")
    contact_info = st.text_input("Contact Info")
    address = st.text_area("Address")
    medical_report = st.file_uploader("Upload Medical Report (if any)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Confirm Order"):
        # Validate that all required fields are filled
        if name and contact_info and address and total_cost > 0:
            # Generate payment link and QR code
            payment_link = f"http://example.com/pay?amount={total_cost}"
            qr_image = generate_qr(payment_link)
            st.image(qr_image)
            st.success("Order Confirmed! Your QR Code for payment is shown above.")
            # Optionally, you can add code to save the order details to a database or CSV
            # Clear cart after order confirmation
            st.session_state.cart.clear()
        else:
            st.warning("Please fill in all details and add items to your cart before confirming the order.")
