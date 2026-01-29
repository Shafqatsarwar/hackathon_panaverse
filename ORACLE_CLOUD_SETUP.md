# ☁️ How to Run on Oracle Cloud (24/7 Watchers)

This guide explains how to deploy your Panaversity Assistant Watchers (WhatsApp & Gmail) to Oracle Cloud Free Tier using Docker, ensuring they run 24/7.

## ✅ Prerequisites

1.  **Oracle Cloud Account** (Free Tier is fine).
2.  **VM Instance**: Ubuntu 22.04 or 24.04 (AMD64 recommended for Playwright, but ARM64 Ampere works with emulation or specific base images).
3.  **Docker & Docker Compose** installed on the VM.

## 🚀 Step 1: Upload Your Code

On your local machine, zip your project (excluding large folders like `.venv`, `node_modules`):
```powershell
# In your project root
tar -czvf project.tar.gz . --exclude=.venv --exclude=node_modules --exclude=.git
```
Upload to your VM (replace IP with your Oracle VM IP):
```bash
scp project.tar.gz ubuntu@YOUR_VM_IP:~/
```

## 🛠️ Step 2: Setup on VM

SSH into your VM:
```bash
ssh ubuntu@YOUR_VM_IP
```

Extract and setup:
```bash
mkdir app
tar -xzvf project.tar.gz -C app
cd app

# create logs directory if missing
mkdir -p logs data/vault whatsapp_session linkedin_session
```

## 🐳 Step 3: Build Docker Container

Build the watcher container:
```bash
docker-compose build
```

## 📱 Step 4: WhatsApp Login (The Tricky Part)

Since the cloud has no screen, we must log in using a "Remote QR Code" method.

1.  **Start the container interactively:**
    ```bash
    docker-compose run --rm watcher /bin/bash
    ```

2.  **Run the Cloud Login Helper:**
    ```bash
    # Inside the container
    python scripts/cloud_login.py
    ```
    *It will take a screenshot of the QR code and save it as `qr_code.png`.*

3.  **Download the QR Code (Open a NEW terminal on your LOCAL machine):**
    ```bash
    # Replace ID with container ID (docker ps) or just copy from volume if mounted
    # Simpler way if you used docker-compose run:
    # The file checks are saving to the mounted volume!
    # So check the 'app' folder on your VM host.
    ```
    
    *On your local machine, copy the image from the VM:*
    ```bash
    scp ubuntu@YOUR_VM_IP:~/app/qr_code.png ./
    ```

4.  **Scan the QR Code** with your phone immediately.
5.  **Verify:** The script will print `✅ SUCCESS: Logged in!`

6.  **Exit container:** `exit`

## ⏱️ Step 5: Start 24/7 Watchers

Now that you are logged in (session saved to `whatsapp_session/` folder), start the watchers in background mode:

```bash
docker-compose up -d
```

**Your Watchers are now running 24/7!**

## 🔍 Monitoring

Check logs:
```bash
docker-compose logs -f
```

Stop watchers:
```bash
docker-compose down
```

## ⚠️ Important Notes

- **Session Expiry:** WhatsApp sessions can expire every 14 days or if detecting unrelated IPs. You may need to repeat Step 4 occasionally.
- **Resources:** Oracle Free Tier has limited RAM. The Dockerfile uses a lightweight base, but keep an eye on memory usage (`htop`).
