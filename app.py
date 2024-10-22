import streamlit as st
import qrcode
from PIL import Image
import io
import speech_recognition as sr  # Will only work in a local environment with microphone access

# Function to generate QR code
def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # Convert the image to a format suitable for Streamlit
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()
    
    return img_byte_array

# Voice recognition function (only works locally)
def recognize_speech():
    recognizer = sr.Recognizer()
    
    try:
        mic = sr.Microphone()
        st.write("Listening for your order...")

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            order = recognizer.recognize_google(audio)
            st.write(f"You said: {order}")
            return order
        except sr.UnknownValueError:
            st.error("Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError:
            st.error("API unavailable")
            return None
    except Exception as e:
        st.error("Microphone not available. Please check your device.")
        return None

# App interface
st.title("Touchless Kiosk Ordering System")

# Generate a QR code for mobile interaction
url = "https://your-ordering-system.com"  # Replace with actual ordering site URL
st.write("Scan the QR code to use the ordering system on your phone:")

# Display the QR code
qr_image = generate_qr_code(url)
st.image(qr_image, caption="Scan to place your order", use_column_width=True)

st.write("Or use voice commands to place your order (works locally):")

# Button to start voice recognition (only works locally)
if st.button("Start Voice Command"):
    order = recognize_speech()
    if order:
        st.success(f"Order placed: {order}")

st.write("No need to touch the screen. Stay safe!")
