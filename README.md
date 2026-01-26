# Docker Python Assignment App

## Docker (Students Task)
Students must understand this Repo and dockerize the app:
- bind mounts
- named volumes
- .env file

# Instructions for Dockerizing the Python App

## Steps to Run the App Locally

1. **Clone the Repository**:
   ```bash
   git clone <repo-link>
   cd <repo-folder>
   ```

2. **Create a `.env` File**:
   - Use the provided `.env.example` file as a reference.
   - Copy the `.env.example` file to `.env` in the root directory:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with the required values.

3. **Install Dependencies**:
   - Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
     ```
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the App Locally**:
   - Start the app:
     ```bash
     python app.py
     ```
   - Open your browser and navigate to `http://127.0.0.1:5001` to test the app.

5. **Verify Everything Works**:
   - Ensure all pages load correctly.
   - Check that logs are being written to the `logs/app.log` file.

---

## Steps to Dockerize the App

1. **Create a `Dockerfile` in the Root Directory**
   - Add Named volume for app.logs 
   - Add Bind volume for app updation
   - copy .env file

   
2. **Build the Docker Image**:
   - Run the following command to build the Docker image:
     ```bash
     docker build -t python-app .
     ```

3. **Run the Docker Container**:
   

4. **Test the Dockerized App**:
   - Open your browser and navigate to `http://127.0.0.1:5001` to test the app.
   - Verify that the app works as expected and logs are being written to the `app_logs` volume.
   - When restart the container or start new container previous logs are displayed.

---

By following these steps, you will successfully dockerize the Python app and ensure it works both locally and in a Docker container. Good luck!# Docker-Python-Assignment-App
