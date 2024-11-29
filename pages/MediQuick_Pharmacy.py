import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

class EcoMarket:
    def __init__(self):
        self.products = [
    {"id": 1, "name": "Reusable Water Bottle", "price": 15, "description": "Stainless steel, BPA-free bottle", "image": "C:\\Users\\shara\\OneDrive\\Pictures\\Screenshots\\Screenshot 2024-11-23 114137.png"},
    {"id": 2, "name": "Bamboo Toothbrush Set", "price": 10, "description": "Pack of 4 biodegradable toothbrushes", "image": "C:\\Users\\shara\\OneDrive\\Pictures\\Screenshots\\Screenshot 2024-11-07 191627.png"},
        ]

        # Initializing session state variables if not present
        if 'cart' not in st.session_state:
            st.session_state.cart = {}
        if 'wishlist' not in st.session_state:
            st.session_state.wishlist = set()
        if 'order_confirmed' not in st.session_state:
            st.session_state.order_confirmed = False

    def add_to_cart(self, product_id):
        if product_id in st.session_state.cart:
            st.session_state.cart[product_id] += 1
        else:
            st.session_state.cart[product_id] = 1
        st.success("Added to cart!")

    def remove_from_cart(self, product_id):
        if product_id in st.session_state.cart:
            if st.session_state.cart[product_id] > 1:
                st.session_state.cart[product_id] -= 1
            else:
                del st.session_state.cart[product_id]
        st.success("Removed from cart!")

    def toggle_wishlist(self, product_id):
        if product_id in st.session_state.wishlist:
            st.session_state.wishlist.remove(product_id)
            st.success("Removed from wishlist!")
        else:
            st.session_state.wishlist.add(product_id)
            st.success("Added to wishlist!")

    def display_products(self):
        st.title("🌿 Eco Market")
        st.write("Browse our selection of eco-friendly products to reduce your carbon footprint!")

        # Display products in a grid
        cols = st.columns(2)
        for idx, product in enumerate(self.products):
            with cols[idx % 2]:
                st.image(product['image'], use_column_width=True)
                st.subheader(product['name'])
                st.write(product['description'])
                st.write(f"Price: ${product['price']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🛒 Add to Cart", key=f"add_{product['id']}"):
                        self.add_to_cart(product['id'])
                with col2:
                    if st.button(f"{'❤' if product['id'] in st.session_state.wishlist else '🤍'} Wishlist", key=f"wish_{product['id']}"):
                        self.toggle_wishlist(product['id'])
                st.write("---")

    def display_cart(self):
        st.sidebar.title("🛒 Your Cart")
        total = 0
        for product_id, quantity in st.session_state.cart.items():
            product = next((p for p in self.products if p['id'] == product_id), None)
            if product:
                st.sidebar.write(f"{product['name']} (x{quantity}): ${product['price'] * quantity}")
                total += product['price'] * quantity
                if st.sidebar.button("Remove", key=f"remove_{product_id}"):
                    self.remove_from_cart(product_id)

        st.sidebar.write(f"Total: ${total}")

        # Proceed to checkout if the cart is not empty and order not confirmed
        if total > 0 and not st.session_state.order_confirmed:
            if st.sidebar.button("Proceed to Checkout"):
                st.session_state.proceed_to_checkout = True

        # Start checkout process if button is clicked
        if 'proceed_to_checkout' in st.session_state and st.session_state.proceed_to_checkout:
            self.checkout(total)

    def display_wishlist(self):
        st.sidebar.title("❤ Your Wishlist")
        for product_id in st.session_state.wishlist:
            product = next((p for p in self.products if p['id'] == product_id), None)
            if product:
                st.sidebar.write(f"{product['name']} - ${product['price']}")
                if st.sidebar.button("Add to Cart", key=f"wishlist_add_{product_id}"):
                    self.add_to_cart(product_id)
                    st.sidebar.success(f"Added {product['name']} to cart!")

    def checkout(self, total):
        st.title("Checkout")
        name = st.text_input("Full Name")
        address = st.text_area("Address")
        contact = st.text_input("Contact Number")
        payment_method = st.radio("Choose Payment Method:", ["QR Code Payment", "Cash on Delivery"])

        if st.button("Confirm Order"):
            if name and address and contact:
                if payment_method == "QR Code Payment":
                    self.generate_qr_code(total)
                else:
                    st.success("Order Confirmed! Cash on Delivery selected.")
                st.session_state.order_confirmed = True
                st.session_state.proceed_to_checkout = False  # Reset checkout
                self.show_final_confirmation()
            else:
                st.error("Please fill out all details.")

    def generate_qr_code(self, total):
        # Generate and display QR code for payment
        qr_data = f"EcoMarket Payment: ${total}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer)
        buffer.seek(0)
        qr_image = Image.open(buffer)
        st.image(qr_image, caption="Scan to Pay", use_column_width=True)

    def show_final_confirmation(self):
        st.success("Your order has been confirmed! Thank you for shopping with us.")
        st.write("🌍 Each small eco-friendly choice we make helps keep Bengaluru green and clean for generations to come!")
        st.session_state.cart = {}  # Clear cart after confirmation

    def display_market(self):
        self.display_products()
        self.display_cart()
        self.display_wishlist()

# Instantiate and run the app
eco_market = EcoMarket()
eco_market.display_market()
