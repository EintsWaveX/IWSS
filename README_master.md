# IWSS (Intelligent Waste Sorter System)

## Grand Assignment Prototype (IoT x AI x Embedded System)

---

### Related Project's Branches

1. kivy-desktop
2. android_studio-mobile

---

### Information about The Application

1. **Topic Title: *Intelligent Waste Sorting System***
2. **Sensors: ESP32-CAM and Weight Sensor (HX711)**
3. **Actuators: 3 SG90 Servos**

We are developing an automated waste sorting system that integrates artificial intelligence, Internet of Things technology, and embedded electronics to address the challenge of proper waste segregation. This compact device will physically separate recyclable materials—plastic, paper, and metal—using computer vision for identification and servo-controlled mechanisms for physical routing.

The system employs an ESP32-CAM microcontroller as its central processing unit, combining camera capabilities with WiFi connectivity in a single low-cost module. Three micro servos operate individual trap doors that direct items into corresponding collection bins below. The mechanical structure will be constructed from accessible materials like acrylic sheets or reinforced cardboard, featuring precisely angled guide chutes that ensure items land in their designated containers.

For the AI implementation, we will train a convolutional neural network using TensorFlow Lite, initially collecting hundreds of labeled images of common waste items to create our dataset. The model will run directly on the ESP32-CAM using TensorFlow Lite Micro, performing real-time classification without cloud dependency. The IoT component connects the device to a cloud dashboard via MQTT protocol, enabling remote monitoring of sorting statistics, accuracy metrics, and system performance through a web interface.

The embedded system programming involves precise timing control for servo movements, camera capture optimization for the ESP32's limited RAM, and power management to ensure reliable operation. By combining these technologies, we create a demonstrative platform that showcases how edge AI can enable intelligent automation in everyday applications, while providing valuable data insights through IoT connectivity. The entire system operates on standard 5V USB power and maintains a compact footprint suitable for educational demonstrations or small-scale implementation.

### Application Requirements

TBA

### IWSS Contributors

1. Immanuel Eben Haezer Joseph Aletheia (101022300172)
2. Naufal Rafi Rahmadian (101022300334)
3. Zuela Tinto Valdy Abdillah (101022330098)

---
