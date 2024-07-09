from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

class Encryption:
    def __init__(self, filename):
        self.filename = filename

    def encryption(self):
        try:
            original_information = open(self.filename, 'rb')
        except (IOError, FileNotFoundError):
            return "File with name {} is not found.".format(self.filename)

        try:
            encrypted_file_name = 'cipher_' + os.path.basename(self.filename)
            encrypted_file_object = open(encrypted_file_name, 'wb')

            content = original_information.read()
            content = bytearray(content)

            key = 192
            for i, val in enumerate(content):
                content[i] = val ^ key

            encrypted_file_object.write(content)
        except Exception as e:
            return f"Something went wrong: {e}"
        finally:
            encrypted_file_object.close()
            original_information.close()

        return encrypted_file_name

class Decryption:
    def __init__(self, filename):
        self.filename = filename

    def decryption(self):
        try:
            encrypted_file_object = open(self.filename, 'rb')
        except (FileNotFoundError, IOError):
            return "File with name {} is not found.".format(self.filename)

        try:
            decrypted_file_name = 'decipher_' + os.path.basename(self.filename)
            decrypted_file_object = open(decrypted_file_name, 'wb')

            cipher_text = encrypted_file_object.read()
            key = 192
            cipher_text = bytearray(cipher_text)

            for i, val in enumerate(cipher_text):
                cipher_text[i] = val ^ key

            decrypted_file_object.write(cipher_text)
        except Exception as e:
            return f"Some problem with Ciphertext: {e}"
        finally:
            encrypted_file_object.close()
            decrypted_file_object.close()

        return decrypted_file_name

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(os.getcwd(), file.filename)
    file.save(file_path)
    e = Encryption(file_path)
    result = e.encryption()
    os.remove(file_path)  # Clean up the uploaded file after processing
    return jsonify({'message': result})

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(os.getcwd(), file.filename)
    file.save(file_path)
    d = Decryption(file_path)
    result = d.decryption()
    os.remove(file_path)  # Clean up the uploaded file after processing
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)
