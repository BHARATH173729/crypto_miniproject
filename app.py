# # # from flask import Flask, request, jsonify
# # # from flask_cors import CORS

# # # app = Flask(__name__)
# # # CORS(app)  # Enable CORS for all origins

# # # class Encryption:
# # #     def __init__(self, filename):
# # #         self.filename = filename

# # #     def encryption(self):
# # #         try:
# # #             original_information = open(self.filename, 'rb')
# # #         except (IOError, FileNotFoundError):
# # #             return "File with name {} is not found.".format(self.filename)

# # #         try:
# # #             print("ashish bkl")
# # #             encrypted_file_name = 'cipher_' + self.filename
# # #             encrypted_file_object = open(encrypted_file_name, 'wb')

# # #             content = original_information.read()
# # #             content = bytearray(content)

# # #             key = 192
# # #             for i, val in enumerate(content):
# # #                 content[i] = val ^ key

# # #             encrypted_file_object.write(content)
# # #         except Exception as e:
# # #             return f"Something went wrong: {e}"
# # #         finally:
# # #             encrypted_file_object.close()
# # #             original_information.close()

# # #         return encrypted_file_name

# # # class Decryption:
# # #     def __init__(self, filename):
# # #         self.filename = filename

# # #     def decryption(self):
# # #         try:
# # #             encrypted_file_object = open(self.filename, 'rb')
# # #         except (FileNotFoundError, IOError):
# # #             return "File with name {} is not found.".format(self.filename)

# # #         try:
# # #             decrypted_file_name = 'decipher_' + self.filename
# # #             decrypted_file_object = open(decrypted_file_name, 'wb')

# # #             cipher_text = encrypted_file_object.read()
# # #             key = 192
# # #             cipher_text = bytearray(cipher_text)

# # #             for i, val in enumerate(cipher_text):
# # #                 cipher_text[i] = val ^ key

# # #             decrypted_file_object.write(cipher_text)
# # #         except Exception as e:
# # #             return f"Some problem with Ciphertext: {e}"
# # #         finally:
# # #             encrypted_file_object.close()
# # #             decrypted_file_object.close()

# # #         return decrypted_file_name

# # # @app.route('/encrypt', methods=['POST'])
# # # def encrypt_file():
# # #     data = request.get_json()
# # #     filename = data.get('filename')
# # #     e = Encryption(filename)
# # #     result = e.encryption()
# # #     return jsonify({'message': result})

# # # @app.route('/decrypt', methods=['POST'])
# # # def decrypt_file():
# # #     data = request.get_json()
# # #     filename = data.get('filename')
# # #     d = Decryption(filename)
# # #     result = d.decryption()
# # #     return jsonify({'message': result})

# # # if __name__ == '__main__':
# # #     app.run(debug=True)



# import streamlit as st
# import requests

# st.title("File Encryption and Decryption Tool")

# # URL of the Flask API
# API_URL = "http://localhost:5000"

# # Function to handle file encryption
# def encrypt_file(filename):
#     response = requests.post(f"{API_URL}/encrypt", json={"filename": filename})
#     return response.json()

# # Function to handle file decryption
# def decrypt_file(filename):
#     response = requests.post(f"{API_URL}/decrypt", json={"filename": filename})
#     return response.json()

# # File upload widget
# uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "jpg", "jpeg", "png", "docx"])

# if uploaded_file is not None:
#     st.write("Filename:", uploaded_file.name)

#     # Save the uploaded file locally
#     with open(uploaded



import os
from tqdm import tqdm
import streamlit as st

class Encryption:
    def __init__(self, filename):
        self.filename = filename

    def encryption(self):
        try:
            with open(self.filename, 'rb') as original_information:
                content = original_information.read()
        except (IOError, FileNotFoundError):
            st.error(f'File with name {self.filename} is not found.')
            return None

        try:
            encrypted_file_name = 'cipher_' + self.filename
            content = bytearray(content)
            key = 192
            st.info('Encryption Process is in progress...!')
            for i, val in tqdm(enumerate(content)):
                content[i] = val ^ key

            with open(encrypted_file_name, 'wb') as encrypted_file_object:
                encrypted_file_object.write(content)
            
            st.success('Encryption completed successfully!')
            return encrypted_file_name
        except Exception as e:
            st.error(f'Something went wrong with {self.filename}: {e}')
            return None

class Decryption:
    def __init__(self, filename):
        self.filename = filename

    def decryption(self, output_filename):
        try:
            with open(self.filename, 'rb') as encrypted_file_object:
                cipher_text = encrypted_file_object.read()
        except (FileNotFoundError, IOError):
            st.error(f'File with name {self.filename} is not found.')
            return None

        try:
            key = 192
            cipher_text = bytearray(cipher_text)
            st.info('Decryption Process is in progress...!')
            for i, val in tqdm(enumerate(cipher_text)):
                cipher_text[i] = val ^ key

            with open(output_filename, 'wb') as decrypted_file_object:
                decrypted_file_object.write(cipher_text)
            
            st.success('Decryption completed successfully!')
            return output_filename
        except Exception as e:
            st.error(f'Some problem with Ciphertext unable to handle: {e}')
            return None

# Streamlit application
st.title('File Encryption and Decryption Tool')

# File upload section
st.header('Upload a File')
uploaded_file = st.file_uploader('Choose a file')

if uploaded_file:
    # Save the uploaded file to the server
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    st.success(f'File {uploaded_file.name} uploaded successfully!')

    # Encryption and Decryption options
    option = st.selectbox('What would you like to do?', ('Encrypt', 'Decrypt'))

    if st.button('Process'):
        if option == 'Encrypt':
            encryptor = Encryption(uploaded_file.name)
            encrypted_file_name = encryptor.encryption()
            if encrypted_file_name:
                with open(encrypted_file_name, 'rb') as f:
                    st.download_button('Download Encrypted File', data=f, file_name=encrypted_file_name)
        elif option == 'Decrypt':
            output_filename = 'decipher_' + uploaded_file.name  # Simplify filename creation
            decryptor = Decryption(uploaded_file.name)
            decrypted_file_name = decryptor.decryption(output_filename)
            if decrypted_file_name:
                with open(decrypted_file_name, 'rb') as f:
                    st.download_button('Download Decrypted File', data=f, file_name=decrypted_file_name)

# Run the Streamlit app
if __name__ == '__main__':
    st.set_option('deprecation.showfileUploaderEncoding', False)
