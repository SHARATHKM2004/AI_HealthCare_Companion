import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

class EcoMarket:
    def __init__(self):
        self.products = [
    {"id": 1, "name": "Reusable Water Bottle", "price": 15, "description": "Stainless steel, BPA-free bottle", "image": "data:image/jpeg;base64,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"},
    {"id": 2, "name": "Bamboo Toothbrush Set", "price": 10, "description": "Pack of 4 biodegradable toothbrushes", "image": "https://www.google.com/imgres?q=IMAGES&imgurl=https%3A%2F%2Fwww.shutterstock.com%2Fimage-photo%2Fcalm-weather-on-sea-ocean-600nw-2212935531.jpg&imgrefurl=https%3A%2F%2Fwww.shutterstock.com%2Fsearch%2Fbackground&docid=ICn889JPjZ6CCM&tbnid=O60LdRXewHbkcM&vet=12ahUKEwjvnL-RsYKKAxWIT2wGHV1CBCIQM3oECBcQAA..i&w=600&h=400&hcb=2&itg=1&ved=2ahUKEwjvnL-RsYKKAxWIT2wGHV1CBCIQM3oECBcQAA"},
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
