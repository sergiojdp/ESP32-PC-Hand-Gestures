#include "esp_camera.h"
#include <WiFi.h>

#define WIFI_SSID "MIWIFI_08A6"
#define WIFI_PASS "T8MDUMC4RQ"

#define SERVER_IP "192.168.1.94"   // IP de tu PC
#define SERVER_PORT 5000

#define BOTON 0   // BOOT -> GPIO0

// Pines AI Thinker ESP32-CAM
#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      21
#define SIOD_GPIO_NUM      26
#define SIOC_GPIO_NUM      27

#define Y9_GPIO_NUM        35
#define Y8_GPIO_NUM        34
#define Y7_GPIO_NUM        39
#define Y6_GPIO_NUM        36
#define Y5_GPIO_NUM        19
#define Y4_GPIO_NUM        18
#define Y3_GPIO_NUM         5
#define Y2_GPIO_NUM         4
#define VSYNC_GPIO_NUM     25
#define HREF_GPIO_NUM      23
#define PCLK_GPIO_NUM      22

volatile bool flag = false;

void IRAM_ATTR botonISR() {
  flag = true; // Marcamos que se pulsó
}

void setup() {
  Serial.begin(115200);

  pinMode(BOTON, INPUT_PULLUP); 
  attachInterrupt(digitalPinToInterrupt(BOTON), botonISR, FALLING);

  // Config cámara
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG; 

  config.frame_size = FRAMESIZE_VGA;   // 640x480 (rápido y suficiente)
  config.jpeg_quality = 10;
  config.fb_count = 1;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("¡Error al inicializar la cámara!");
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  if (s) {
    s->set_vflip(s, 1);    // 1 = voltear verticalmente
  }

  // Conectar a WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
}

void loop() {

  if (flag){
    flag = false;

    WiFiClient client;
    if (!client.connect(SERVER_IP, SERVER_PORT)) {
      Serial.println("No se pudo conectar al servidor");
      return;
    }

    // Capturar foto
    camera_fb_t *fb = esp_camera_fb_get();
    esp_camera_fb_return(fb);  // descarta el primero
    fb = esp_camera_fb_get();  // usa el segundo, más reciente

    if (!fb) {
      Serial.println("Error capturando imagen");
      return;
    }

    // Enviar tamaño y bytes de imagen
    uint32_t img_size = fb->len;
    client.write((uint8_t*)&img_size, sizeof(img_size));
    client.write(fb->buf, img_size);

    esp_camera_fb_return(fb);

    Serial.println("Esperando respuesta del servidor");

    // Leer respuesta del servidor
    while (client.connected()) {
      if (client.available()) {
        String respuesta = client.readStringUntil('\n');
        Serial.println("Respuesta servidor: " + respuesta);
        break;
      }
    }
    Serial.println("");
    client.stop();
    delay(1000);
  }
}
