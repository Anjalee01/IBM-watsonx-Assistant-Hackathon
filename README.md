# IBM-watsonx-Assistant-Hackathon


## Servonix

Servonix is an AI-powered assistant designed to streamline order management for e-commerce platforms. This project showcases a mockup of the system, featuring a frontend built with HTML, CSS, and TailwindCSS, a backend written in Python, and integration with IBM watsonx Assistant.

---

## **Project Overview**

### **Frontend**
- **Technology:** HTML, CSS, TailwindCSS and JavaScript.
- **Purpose:** Provides a modern and responsive landing page where the IBM watsonx Assistant is embedded to handle customer queries.
- **Deployment:** Hosted on **Vercel** for fast and scalable access.

### **Backend**
- **Technology:** Python.
- **Purpose:** Serves as the backend API for IBM watsonx Assistant, providing mock responses to simulate order management functionalities like tracking, modifications, and returns.
- **Hosting:** Temporarily hosted on **Replit** for easy prototyping and collaboration.

### **AI Assistant**
- **Platform:** IBM watsonx Assistant.
- **Integration:** Consumes backend APIs to retrieve and provide order-related data, delivering a seamless conversational experience.

---

## **Project Features**
- **Frontend:**
  - Responsive design with TailwindCSS.
  - Embeds the IBM watsonx Assistant widget.
  - Clear structure for easy navigation and interaction.
  
- **Backend:**
  - Python-based mockup simulating essential e-commerce operations.
  - Integration-ready endpoints for IBM watsonx Assistant.
  
- **AI Assistant:**
  - Handles natural language queries related to order tracking, modifications, and returns.
  - Connects with the backend to retrieve and provide accurate data.

---

## **Setup and Deployment**

### **Frontend**
1. Clone the repository:
   ```bash
   git clone git@github.com:Anjalee01/IBM-watsonx-Assistant-Hackathon.git
    ```
2. Navigate to the frontend folder:

    ```bash
    cd servonix/frontend
    ```
3. Deploy on Vercel:
    - Login to Vercel.
    - Link the project and deploy.

---

### **Backend**

🚀 Servonix Backend Setup Guide

Welcome to the Servonix Backend! This guide will walk you through setting up and running the backend services for the Servonix Virtual Assistant for hassle-free order management. Follow these detailed steps to get started.


---

🛠️ Requirements

Before proceeding, ensure you have the following installed on your system:

1. Python 3.9 or later
Download Python from the official website: Python Downloads.


2. pip (Python package manager)
Comes bundled with Python. Verify installation:

pip --version


3. Flask
A lightweight Python web framework.
Installation is covered in the setup steps below.


4. Git
For cloning the project repository.
Install Git: Git Downloads.


5. Postman (Optional)
For testing API endpoints easily.
Download here: Postman Downloads.




---

📂 Project Structure

Here’s an overview of the backend file structure:

servonix-backend/
├── app.py                   # Main entry point of the backend
├── requirements.txt         # List of dependencies
├── models/                  # Data models (e.g., User, Order)
│   ├── user.py
│   └── order.py
├── controllers/             # API logic controllers
│   ├── user_controller.py
│   └── order_controller.py
└── services/                # Business logic services
    ├── user_service.py
    └── order_service.py


---

⚙️ Setup Instructions

1️⃣ Clone the Repository

First, clone the Servonix repository from GitHub to your local machine:

git clone https://github.com/your-username/servonix-backend.git
cd servonix-backend

2️⃣ Install Dependencies

Install the required Python packages using pip:

pip install -r requirements.txt

3️⃣ Run the Server

Start the Flask server by running the following command:

python app.py

This will launch the backend server at http://127.0.0.1:5000.


---

🧩 Configuration

🔑 Watson Assistant Integration

To use IBM Watson Assistant, register for a free IBM Cloud account and set up a Watson Assistant instance:
🔗 IBM Cloud Watson Assistant

Once set up, note down the following values:

Integration ID

Service Instance ID

Region



Add this information to the frontend index.html in the Watson Assistant script:

window.watsonAssistantChatOptions = {
    integrationID: "<YOUR_INTEGRATION_ID>",
    region: "<YOUR_REGION>",
    serviceInstanceID: "<YOUR_INSTANCE_ID>",
    onLoad: async (instance) => { await instance.render(); }
};

🛢️ Database

Currently, this project uses a mock database for demonstration purposes. If you want to integrate a real database:

1. SQLite: Easy to set up for local use.
Installation guide: SQLite Downloads


2. PostgreSQL: Recommended for production.
Get started: PostgreSQL Downloads



Update the services and models to connect with your chosen database.


---

📬 Testing the API

Using Postman

1. Import your API endpoints into Postman for easy testing: Postman Docs.


2. Test example endpoints:

GET /users: Retrieve all users.

POST /orders: Create a new order.




Example request for creating an order:

POST /orders
{
    "item": "Smartphone",
    "user_id": 101
}

Using Curl (Optional)

Test endpoints directly from the terminal:

curl -X GET http://127.0.0.1:5000/orders


---

🌐 Deployment

To deploy the backend to production, use one of the following services:

🖥️ Heroku

A free hosting platform for small projects.
Sign up and follow the deployment steps: Heroku Sign Up.

☁️ AWS

Amazon Web Services for scalable production deployments.
Get started: AWS Free Tier.

🧑‍💻 Docker

Containerize the app for consistent deployment across environments.
Learn more: Docker Documentation.


---

📘 API Documentation

For detailed documentation of all endpoints, refer to the README.md in the docs/ folder or use tools like Swagger to generate documentation.


---

1. Fork the repository.


2. Create a feature branch:

git checkout -b feature-name


3. Submit a pull request.




---

🔗 Resources

IBM Watson Assistant Documentation

Flask Framework Documentation

Postman API Tool

Python Official Website


---

### **IBM watsonx Assistant**

1. Configure your Assistant:
    - Log in to the IBM watsonx Assistant Console.
    - Create a new assistant and configure it to connect to the backend endpoints.
2. Embed the assistant widget:

    - Copy the generated embed code from the watsonx Assistant console.
    - Paste it into the frontend HTML.

---

## **Usage**

- Visit the deployed frontend on Vercel.

- Interact with the IBM watsonx Assistant to:
  - Track orders.
  - Modify shipping details.
  - Request returns or refunds.

- The assistant communicates with the Python backend to provide mock responses.

---

## **Future Plans**

- Expand backend to support real-world APIs and databases.

- Add authentication for secure operations.

- Enhance the frontend with advanced features like analytics dashboards.

---

## **Contributors**

- [Anjalee Ramwani] - Team Lead, Frontend Developer
- [Mouafo kamgno keryan gift] - Backend Integration
- [guxal] - AI Assistant Configuration

---

---

🎉 Thank You for Using Servonix!

For any issues or questions, feel free to open an issue in the repository or contact us directly. Let’s simplify order management together! 😊


