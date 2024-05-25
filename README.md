# Integration with Cloud-Based ERP (QuickBooks Online)

## Task Description
Develop an application to interact with a cloud-based ERP system (such as QuickBooks Online) by implementing authentication with QBO. The application should authenticate with the ERP's API, extract vendor and account data from the sandbox environment, and demonstrate updating a vendor record. The appearance of the user interface is irrelevant; it can be a simple command-line interface or any functional interface that fulfills the requirements.

As a part of this assignment, you will need to create a developer account with QBO. Visit [QBO Developer Sandboxes](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes) for more details.

## Requirements

### Authentication with QBO
- Implement authentication with QuickBooks Online to securely authenticate with the ERP's API.
- Use appropriate authentication mechanisms provided by QBO's API.

### Data Extraction
- Retrieve sample vendor and account data from the sandbox environment of QuickBooks Online.
- Extract relevant data entities including vendor information (such as name, contact details) and account details.

### Data Update
- Implement functionality to update a vendor record in QuickBooks Online.
- Demonstrate updating at least one attribute of a vendor record (e.g., contact information).

### Error Handling
- Implement error handling mechanisms to handle API errors, authentication failures, or other unexpected issues.
- Provide informative error messages to aid in troubleshooting and debugging.

### Documentation
- Provide documentation with setup instructions, usage guidelines, and any additional notes.

## Additional Notes
- Integrate with a cloud-based ERP system.
- OAuth2 principles, API interaction, and error handling.

---
## Thought Process and Implementation

### Authentication with QuickBooks Online (QBO)

To authenticate with QBO, I needed to implement OAuth 2.0, a secure and industry-standard protocol for authorization. The steps included:
1. **Creating a Developer Account**: Registered for a developer account on Intuit Developer Portal and set up a new app.
2. **Setting Redirect URIs**: Configured the app to use `http://localhost:5000/redirect` as the redirect URI for handling OAuth responses.
3. **Generating Auth URL**: Created a function to generate the authorization URL, allowing users to authorize the app.
4. **Handling Redirects**: Implemented a route in Flask to handle redirects from QBO and exchange the authorization code for access and refresh tokens.

### Data Extraction

1. **Vendor and Account APIs**: Utilized the QBO APIs to fetch vendor and account details.
2. **API Endpoints**: Developed endpoints in Flask to get vendor and account data using the access tokens.
3. **Logging**: Added comprehensive logging to trace requests and responses for debugging and verification.

### Data Update

1. **Update Vendor Record**: Implemented a Flask endpoint to update vendor information.
2. **Update Account Record**: Implemented a Flask endpoint to update account information.
3. **Verification**: Ensured the updates were reflected by fetching the updated vendor/account data.

### Error Handling

1. **Exception Handling**: Wrapped API calls in try-except blocks to catch and log errors.
2. **Informative Messages**: Provided clear error messages to help diagnose issues.

### Documentation

1. **Setup Instructions**: Detailed steps to set up the project, including environment setup and dependencies.
2. **Usage Guidelines**: Instructions on how to run the application and interact with the APIs.
3. **Additional Notes**: Information about the OAuth flow, API endpoints, and testing.

---

## Project Setup

### Prerequisites

- Python 3.9+
- Flask
- Requests
- Intuit Developer Account

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vsinghal3737/Integration-with-Cloud-Based-ERP
   cd Integration-with-Cloud-Based-ERP
   ```
2. **Manual Setup (Optional)**:
   * **Create a Virtual Environment**:
      ```bash
      python -m venv venv
      source venv/bin/activate   # On Windows: `venv\Scripts\activate`
      ```
   * **Install Dependencies**:
      ```bash
      pip install -r requirements.txt
      ```
   * For more detailed information on virtual environments and package installation, refer to the [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).
3. **PyCharm Setup (Skip #2)**:
   If you are using PyCharm, you can skip step 2. Instead, follow these steps:
   * Open PyCharm and navigate to `File` > `Open` and select the cloned repository directory.
   * PyCharm will detect the `requirements.txt` file and prompt you to install the dependencies.
   * Confirm and let PyCharm handle the setup.
4. **Set Up Environment Variables(Important)**:
   ```
   CLIENT_ID = "<your_client_id>"
   CLIENT_SECRET = "<your_client_secret>"
   REDIRECT_URI = "<your_redirect_URI>" (Default: "http://localhost:5000/redirect")
   ```

---
## How to Run
**Start the Flask Application**:
* **Run via Command Line**:
  ```bash
  python main.py
  ```
* **Run via PyCharm**:
  - Open `main.py` in PyCharm.
  - Ensure the following code block is present at the bottom of `main.py`:
    ```python
    if __name__ == "__main__":
        main()
    ```
  - Right-click on `main.py` and select `Run 'main'`.


---
## API Documentation
### 1. Initiate Authorization
To begin the authorization process, open your browser and navigate to the following URL:
```
http://localhost:5000/authorize
```
This endpoint generates an authorization URL and redirects the user to the QuickBooks Online (QBO) login page where they can authorize the application.

### 2. Authorize Application
After completing the authorization process on QBO's login page, the user will be redirected back to the following URL with the authorization code and realm ID:
```
http://localhost:5000/redirect
```
This endpoint handles the redirect from QBO, exchanges the authorization code for access and refresh tokens, and displays the tokens.

### 3. Fetch Vendor and Account Data
#### Get All Vendors
**Request:**
```http
GET http://localhost:5000/vendors
```
**Response:**
```json
[
  {
    "id": "56",
    "name": "Bob's Burger Joint",
    "balance": 0,
    "currency": "USD"
  },
  ...
]
```

#### Get Vendor by ID
**Request:**
```http
GET http://localhost:5000/vendors/56
```
**Response:**
```json
{
  "id": "56",
  "name": "Bob's Burger Joint",
  "balance": 0,
  "currency": "USD",
  "active": true,
  "meta_data": {
    "create_time": "2024-05-10T14:28:52-07:00",
    "last_updated_time": "2024-05-10T14:28:52-07:00"
  }
}
```

#### Get All Accounts
**Request:**
```http
GET http://localhost:5000/accounts
```
**Response:**
```json
[
  {
    "id": "123",
    "name": "Cash",
    "type": "Bank",
    "balance": 1000
  },
  ...
]
```

#### Get Account by ID
**Request:**
```http
GET http://localhost:5000/accounts/123
```
**Response:**
```json
{
  "id": "123",
  "name": "Cash",
  "type": "Bank",
  "balance": 1000,
  "meta_data": {
    "create_time": "2024-05-10T14:28:52-07:00",
    "last_updated_time": "2024-05-10T14:28:52-07:00"
  }
}
```

### 4. Update Vendor and Account Data
#### Update Vendor by ID
**Request:**
```http
POST http://localhost:5000/vendors/56
Content-Type: application/json

{
  "update_fields": {
    "DisplayName": "New Vendor Name",
    "Balance": 100
  }
}
```
**Response:**
```json
{
  "id": "56",
  "name": "New Vendor Name",
  "balance": 100,
  "currency": "USD",
  "active": true,
  "meta_data": {
    "create_time": "2024-05-10T14:28:52-07:00",
    "last_updated_time": "2024-05-24T15:05:00.672-07:00"
  }
}
```
#### Update Account by ID
**Request:**
```http
POST http://localhost:5000/accounts/123
Content-Type: application/json

{
  "update_fields": {
    "name": "Updated Account Name",
    "balance": 2000
  }
}
```

**Response:**
```json
{
  "id": "123",
  "name": "Updated Account Name",
  "type": "Bank",
  "balance": 2000,
  "meta_data": {
    "create_time": "2024-05-10T14:28:52-07:00",
    "last_updated_time": "2024-05-24T15:05:00.672-07:00"
  }
}
```
---
