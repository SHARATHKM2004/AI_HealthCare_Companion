import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io

# Sample data for medicines and eco-friend
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': "data:image/jpeg;base64,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"},
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
