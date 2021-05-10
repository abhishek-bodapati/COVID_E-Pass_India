## Prerequisites
- Python version 3 and above

## Install Packages
```
pip install Flask
pip install qrcode
pip install dload
pip install Flask-PyMongo
pip install requests
pip install pdfkit
pip install python-dotenv
pip install pathlib
```
<!--
## Setup Environment Variables for API Key
### Mac

Update the development environment with your [SENDGRID_API_KEY](https://app.sendgrid.com/settings/api_keys) (more info [here](https://sendgrid.com/docs/User_Guide/Settings/api_keys.html)), for example:

```bash
echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
```
SendGrid also supports local environment file `.env`. Copy or rename `.env_sample` into `.env` and update [SENDGRID_API_KEY](https://app.sendgrid.com/settings/api_keys) with your key.

### Windows
Temporarily set the environment variable(accessible only during the current cli session):
```bash
set SENDGRID_API_KEY=YOUR_API_KEY
```
Permanently set the environment variable(accessible in all subsequent cli sessions):
```bash
setx SENDGRID_API_KEY "YOUR_API_KEY"
```
-->