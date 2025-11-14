# Smart Parking System

A complete Parking Management System supporting:  
- Vehicle entry and exit logging  
- Parking slot management  
- Automatic fee calculation  
- Payment recording  
- Car detection using OCR cameras  
- Dashboard for admin and user monitoring  

---

## 1️⃣ Users App

### App Description:
- Manage users (Admin / User)  
- Manage cars linked to users  

### API Endpoints:

| Method | URL | Description |
|--------|-----|------------|
| GET | `/api/users/users/` | List all users |
| POST | `/api/users/users/` | Create a new user |
| GET | `/api/users/cars/` | List all cars |
| POST | `/api/users/cars/` | Add a new car |
| GET | `/api/users/cars/<id>/` | Retrieve car details |
| PUT/PATCH | `/api/users/cars/<id>/` | Update car details |
| DELETE | `/api/users/cars/<id>/` | Delete a car |

---

## 2️⃣ Parking App

### App Description:
- Manage parking slots  
- Register vehicle entry and exit (Transactions)  
- Calculate parking duration and fees automatically  

### API Endpoints:

| Method | URL | Description |
|--------|-----|------------|
| GET | `/api/parking/slots/` | List all parking slots |
| POST | `/api/parking/slots/` | Create a new parking slot |
| GET | `/api/parking/transactions/` | List all transactions |
| POST | `/api/parking/transactions/enter/` | Register car entry |
| POST | `/api/parking/transactions/exit/` | Register car exit and calculate fees |

---

## 3️⃣ Payments App

### App Description:
- Manage payments for each transaction  
- Support multiple payment methods (Cash / Card / Online)  

### API Endpoints:

| Method | URL | Description |
|--------|-----|------------|
| GET | `/api/payments/payments/` | List all payments |
| POST | `/api/payments/pay_transaction/` | Record a payment for a completed transaction |
| GET | `/api/payments/payments/<id>/` | Retrieve payment details |
| PUT/PATCH | `/api/payments/payments/<id>/` | Update payment method or amount |
| DELETE | `/api/payments/payments/<id>/` | Delete a payment |

---

## 4️⃣ Camera_OCR App

### App Description:
- Manage cameras in the parking lot  
- Assign slots monitored by each camera  
- Record OCR logs for license plates  
- Automatically update slot status  

### API Endpoints:

| Method | URL | Description |
|--------|-----|------------|
| GET | `/api/camera_ocr/cameras/` | List all cameras |
| POST | `/api/camera_ocr/cameras/` | Create a new camera |
| GET | `/api/camera_ocr/ocr_logs/` | List all OCR logs |
| POST | `/api/camera_ocr/ocr_logs/detect_car/` | Record car detection and update slot status |

---

## 5️⃣ Dashboard App

### App Description:
- Aggregate data from all other apps  
- Display slots, cars, payments, recent OCR logs  
- Provide ready-to-use statistics  

### API Endpoints:

| Method | URL | Description |
|--------|-----|------------|
| GET | `/api/dashboard/` | Retrieve all dashboard data: slots, cars, payments, recent OCR logs, and statistics |

---

## 6️⃣ Models Diagram (ERD)

<img width="3127" height="4191" alt="deepseek_mermaid_20251114_633cc6" src="https://github.com/user-attachments/assets/d32f0323-63af-4ecd-976f-5e276616ce1c" />

**Explanation:**

- **User-Car:** Each user can own multiple cars  
- **Car-ParkingTransaction-ParkingSlot:** Each car enters a slot, each slot can have multiple transactions over time  
- **ParkingTransaction-Payment:** Each transaction can have one or more payments  
- **Camera-OCRLog-ParkingSlot:** Each camera can monitor multiple slots, each OCR log is linked to a camera and slot  
- Dashboard aggregates all data without adding new tables  

---

**Notes:**
- All apps use Django REST Framework for APIs  
- System can be expanded to support more payment methods, additional cameras, or detailed reports  
- Dashboard frontend can be built using React, Vue, or Django Templates



