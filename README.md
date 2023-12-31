
## Hosting a Flask Application on EC2 with Gunicorn and Nginx

This guide will walk you through the process of setting up a Flask application on an EC2 instance, using Gunicorn as the WSGI server and Nginx as a reverse proxy.

Certainly! Let's delve into each step with a bit more detail:

### Step 1: Install Python Virtualenv

```bash
sudo apt-get update
sudo apt-get install python3-venv
```

This step ensures that your EC2 instance has the necessary tools to create and manage virtual environments for Python.

### Step 2: Set up the Virtual Environment

```bash
mkdir project
cd project
python3 -m venv venv
source venv/bin/activate
```

Here, you create a project directory and set up a virtual environment within it. Activating the virtual environment isolates your project's dependencies, preventing conflicts with other Python projects on the same machine.

### Step 3: Install Flask

```bash
pip install flask
```

This installs the Flask framework within your virtual environment, allowing you to develop web applications using Python.

### Step 4: Create a Simple Flask API (Clone Github repo)

```bash
git clone <link>
```

You clone your Flask application's code from a GitHub repository. This step assumes you have your Flask application hosted on a Git repository.

```bash
python run.py
```

Verifying that the application works ensures that your Flask API is set up correctly.

### Step 5: Install Gunicorn

```bash
pip install gunicorn
```

Gunicorn, or Green Unicorn, is a WSGI server for running Flask applications. Installing it is a crucial step in deploying a production-ready Flask app.

```bash
gunicorn -b 0.0.0.0:8000 app:app
```

You run Gunicorn, binding it to address 0.0.0.0:8000, and specifying the entry point to your Flask application (`app:app`).

### Step 6: Use systemd to Manage Gunicorn

You create a systemd unit file to manage the Gunicorn process as a service.

```bash
sudo nano /etc/systemd/system/project.service
```

The unit file specifies the user, working directory, and command to start Gunicorn as a service.

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

After creating the unit file, you enable and start the Gunicorn service.

```bash
sudo systemctl daemon-reload
sudo systemctl start project
sudo systemctl enable project
```

### Step 7: Run Nginx Webserver

```bash
sudo apt-get install nginx
```

Nginx is a web server that will act as a reverse proxy for your Flask application, forwarding requests to Gunicorn.

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

Starting and enabling Nginx ensures that it runs automatically after a system reboot.

```bash
sudo nano /etc/nginx/sites-available/default
```

You configure Nginx by editing its default configuration file, specifying the upstream server (Gunicorn) and the location for proxying requests.

```nginx
upstream flask_project {
    server 127.0.0.1:5000;
}

location / {
    proxy_pass http://flask_project;
}
```

After editing the configuration, you restart Nginx to apply the changes.

```bash
sudo systemctl restart nginx
```

Visiting your EC2 instance's public IP address in a browser confirms that your Flask application is now accessible through Nginx, completing the deployment process.
