#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip if not already installed
sudo apt-get install -y python3 python3-pip python3-venv

# Install nginx
sudo apt-get install -y nginx

# Create a directory for the app
sudo mkdir -p /var/www/interview-prep-assistant
sudo chown -R $USER:$USER /var/www/interview-prep-assistant

# Copy application files
cp -r ./* /var/www/interview-prep-assistant/

# Create and activate virtual environment
cd /var/www/interview-prep-assistant
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/interview-prep-assistant.service << EOF
[Unit]
Description=Interview Prep Assistant Streamlit App
After=network.target

[Service]
User=$USER
WorkingDirectory=/var/www/interview-prep-assistant
Environment="PATH=/var/www/interview-prep-assistant/venv/bin"
ExecStart=/var/www/interview-prep-assistant/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/interview-prep-assistant << EOF
server {
    listen 80;
    server_name _;  # Replace with your domain name when ready

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/interview-prep-assistant /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start and enable services
sudo systemctl start interview-prep-assistant
sudo systemctl enable interview-prep-assistant
sudo systemctl restart nginx

echo "Deployment completed! The app should be running at http://your-server-ip"
echo "To check the status, run: sudo systemctl status interview-prep-assistant" 