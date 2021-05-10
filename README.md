# COVID E-Pass India
* Checks the COVID affected counts in the destination district and decides to provide an e-Pass.
* Generates the e-Pass, sends the attachment to the citizen's e-mail address and also provides an option to download.
* e-Pass details stored in DB.
* Also verifies the authenticity of the e-Pass with a QR code generated text.
* COVID data collected from [COVID-19 India API](http://api.covid19india.org/v4/data.json)

## Prerequisites
- Python version 3 and above
- [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) 
- MongoDB (DB name - **E-Pass**, Collections name - **Tokens**)
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

## Setup Environment Variables for API Key
### Mac

Update the development environment with your [SENDGRID_API_KEY](https://app.sendgrid.com/settings/api_keys) (more info [here](https://sendgrid.com/docs/User_Guide/Settings/api_keys.html)), for example:

```bash
echo -e "export SENDGRID_API_KEY='YOUR_API_KEY'\nexport MAIL_DEFAULT_SENDER='YOUR_MAIL_ID'" > sendgrid.env > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
```
SendGrid also supports local environment file `.env`. Copy or rename `.env_sample` into `.env` and update [SENDGRID_API_KEY](https://app.sendgrid.com/settings/api_keys) with your key.

### Windows
Temporarily set the environment variable(accessible only during the current cli session):
```bash
set SENDGRID_API_KEY=YOUR_API_KEY
set MAIL_DEFAULT_SENDER=YOUR_MAIL_ID
```
Permanently set the environment variable(accessible in all subsequent cli sessions):
```bash
setx SENDGRID_API_KEY "YOUR_API_KEY"
setx MAIL_DEFAULT_SENDER "YOUR_MAIL_ID"
```
## How to run?
```
python main.py
```
* Open [localhost:5000](http://127.0.0.1:3000/) in browser.