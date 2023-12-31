
## Hosting a Flask Application on EC2 with Gunicorn and Nginx

This guide will walk you through the process of setting up a Flask application on an EC2 instance, using Gunicorn as the WSGI server and Nginx as a reverse proxy.

### Step 1: Install Python Virtualenv

```bash
sudo apt-get update
sudo apt-get install python3-venv
```

### Step 2: Set up the Virtual Environment

```bash
mkdir project
cd project
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Flask

```bash
pip install flask
```

### Step 4: Create a Simple Flask API (Clone Github repo)

```bash
git clone <link>
```

Verify if it works:

```bash
python run.py
```

### Step 5: Install Gunicorn

```bash
pip install gunicorn
```

Run Gunicorn:

```bash
gunicorn -b 0.0.0.0:8000 app:app
```

### Step 6: Use systemd to Manage Gunicorn

Create a systemd unit file:

```bash
sudo nano /etc/systemd/system/project.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn instance for a de-project
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/project
ExecStart=/home/ubuntu/project/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start project
sudo systemctl enable project
```

Check if the app is running:

```bash
curl localhost:8000
```

### Step 7: Run Nginx Webserver

Install Nginx:

```bash
sudo apt-get install nginx
```

Start Nginx:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

Edit the Nginx default configuration:

```bash
sudo nano /etc/nginx/sites-available/default
```

Add the following lines:

```nginx
upstream flask_project {
    server 127.0.0.1:8000;
}

location / {
    proxy_pass http://flask_project;
}
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

Visit your EC2 instance's public IP address in the browser, and your Flask application should be up and running!
