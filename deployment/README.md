# Linux deployment

After cloning this repository on the target Linux machine:

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the service file into systemd:
   ```bash
   sudo cp deployment/ha-mikroservice.service /etc/systemd/system/ha-mikroservice.service
   ```
4. Reload systemd and enable the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ha-mikroservice.service
   ```
5. Start it:
   ```bash
   sudo systemctl start ha-mikroservice.service
   ```
6. Check status:
   ```bash
   sudo systemctl status ha-mikroservice.service
   ```

The service assumes the app is started from the repository root and uses the virtual environment in that same directory.
