from model.dao.FaceDAO import FaceDAO
from model.Face import Face
import os
import face_recognition
import pickle
import cv2
import logging
import datetime
import uuid
from cryptography.fernet import Fernet
import sqlite3


class FaceController:
    def __init__(self):
        self.face_dao = FaceDAO()
        self._initialize_encryption()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # E:\Users\ploan\python_EAUT\BTL
        log_file = os.path.join(BASE_DIR, "view", "utils", "face_id.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Create directory if it doesn't exist
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def register_face(self, user_id):
        frame = self.capture_face_register()
        encodings = face_recognition.face_encodings(frame)
        if not encodings:
            return False, "No face detected!"
        encoding = encodings[0]
        encrypted_encoding = self.fernet.encrypt(pickle.dumps(encoding))

        try:
            face = Face(id=str(uuid.uuid4()), user_id=user_id, face_encoding=encrypted_encoding, created_at=datetime.datetime.now())
            self.face_dao.tao(face)
            return True, "Đăng kí gương mặt thành công!"
        except sqlite3.IntegrityError:
            return False, "User ID already exists!"

    def verify_face(self):
        frame = self.capture_face_verify()
        encodings = face_recognition.face_encodings(frame)

        if not encodings:
            return False, "No face detected!"

        # Get the first face encoding (assuming only one face in the frame)
        new_encoding = encodings[0]

        # Retrieve all stored face data
        all_face_data = self.face_dao.lay_tat_ca()

        if not all_face_data:
            return False, "No registered faces found!"

        # Compare with each stored face encoding
        for face_data in all_face_data:
            user_id, encrypted_encoding = face_data[1], face_data[2]  # Adjust indices based on your DB schema

            try:
                stored_encoding = pickle.loads(self.fernet.decrypt(encrypted_encoding))
                # Compare the face encodings
                matches = face_recognition.compare_faces([stored_encoding], new_encoding, tolerance=0.5)

                if matches[0]:
                    # Face matched
                    return user_id, f"Face verified successfully for user {user_id}!"
            except Exception as e:
                logging.error(f"Error decrypting face data: {e}")
                continue

        return None, "Face verification failed - no matching face found!"

    def _initialize_encryption(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Gets E:\Users\ploan\python_EAUT\BTL
        key_path = os.path.join(BASE_DIR, "view", "utils", "face_encryption.key")  # Full path to session.json
        # key_path = "face_encryption.key"
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                self.fernet = Fernet(f.read())
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as f:
                f.write(key)
            self.fernet = Fernet(key)

    def capture_face_register(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Press SPACE to capture', frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                break
        cap.release()
        cv2.destroyAllWindows()
        return frame

    def capture_face_verify(self):
        cap = cv2.VideoCapture(0)
        face_detected = False
        frame = None

        while not face_detected:
            ret, frame = cap.read()
            if not ret:
                continue

            # Chuyển đổi ảnh sang định dạng RGB để xử lý
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            # Nếu phát hiện ít nhất một khuôn mặt, chụp và thoát vòng lặp
            if face_locations:
                face_detected = True
                print("✅ Face detected! Capturing...")

            # Hiển thị hình ảnh lên màn hình
            cv2.imshow('Detecting face...', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Cho phép thoát bằng phím 'q'
                break

        cap.release()
        cv2.destroyAllWindows()
        return frame