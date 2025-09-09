
---

# 🧠 App Overview

### `accounts`
- Manages doctors, patients, and authentication
- Role-based access (doctor is the payer)

### `case`
- Defines dental cases and their treatment items
- Connects to services and materials

### `treatment`
- Catalog of services, materials, and scopes
- Used for pricing and case planning

### `pricing`
- PriceListModel: defines active price lists
- ServicePriceModel: prices per service/material/scope
- SurchargeModel: extra costs (e.g. urgency, complexity)
- QuoteRequestModel: optional quote system

### `orders`
- CartModel: temporary basket before payment
- OrderModel: finalized order with total price
- PaymentModel: PayPal-based payment tracking
- All orders are linked to the doctor

### `public`
- CaseFileModel: uploaded scans (Pre-op, Waxup, etc.)
- Supports multilingual tagging and flexible linking

---


## 🔐 Business Logic Highlights
- Only doctors can submit orders and make payments
- CaseItems are priced via ServicePriceModel
- Surcharges are applied per case or globally
- Payments are tracked via PayPal transaction ID
- Uploaded files are linked to cases or item


## 📄 License & Credits
This project is developed by Hamed Khodami, backend developer focused on clean architecture, modular Django apps, and scalable systems.

