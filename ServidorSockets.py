import socket
import struct

import cv2
import mediapipe as mp

PORT = 5000
SAVE_PATH = r"D:\ESP32\Programas\PC_Imagen\FotosDescargadas\captura.jpg"

def main():

    # Inicializar MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils

    # Crear socket
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Configurar dirección
    server_fd.bind(("", PORT))
    server_fd.listen(1)
    print(f"Servidor escuchando en puerto {PORT}...")

    while True:
        client_fd, client_addr = server_fd.accept()
        print("Cliente conectado:", client_addr)

        try:
            # Recibir tamaño de imagen (uint32_t)
            data = client_fd.recv(4)
            if not data:
                client_fd.close()
                continue

            img_size = struct.unpack("I", data)[0]  # uint32 en C
            print(f"Tamaño de imagen: {img_size} bytes")

            buffer = b""
            while len(buffer) < img_size:
                chunk = client_fd.recv(img_size - len(buffer))
                if not chunk:
                    break
                buffer += chunk

            # Guardar archivo
            with open(SAVE_PATH, "wb") as f:
                f.write(buffer)

            print("Imagen guardada")

            # Añadir aqui procesamiento de la imagen
            # Cargar imagen
            image = cv2.imread("D:\\ESP32\\Programas\\PC_Imagen\\FotosDescargadas\\captura.jpg")
            if image is None:
                print("❌ No se pudo cargar la imagen")
                exit()

            # Procesar imagen
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Dibujar resultados
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                print("Mano detectada")
                respuesta = posicionDedos(hand_landmarks, mp_hands)
                print(respuesta.decode().strip())
            else:
                print("No se detectó ninguna mano")
                respuesta = b"Nada detectado\n"

            # Mostrar imagen
            cv2.imshow("Detección de Mano", image)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()

            # Enviar respuesta
            #respuesta = b"A\n"
            client_fd.sendall(respuesta)

        finally:
            client_fd.close()

def posicionDedos(hand_landmarks, mp_hands):
    # Comprueba si los dedos están extendidos
    pulgar = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    indice = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    corazon = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    anular = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    menique = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    dedos = [pulgar, indice, corazon, anular, menique]

    if dedos == [False, False, False, False, False]: mano = "Puño\n"
    elif dedos == [True, False, False, False, False]: mano = "Pulgar arriba\n"
    elif dedos == [True, True, False, False, False]: mano = "Dos\n"
    elif dedos == [True, True, True, False, False]: mano = "Tres\n"
    elif dedos == [True, True, True, True, False]: mano = "Cuatro\n"
    elif dedos == [True, True, True, True, True]: mano = "Mano abierta\n"
    elif dedos == [True, True, False, False, True]: mano = "Rock and Roll\n"
    else: mano = "Posición no reconocida"
    
    return mano.encode()

if __name__ == "__main__":
    main()