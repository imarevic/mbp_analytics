## mbp-analytics
A web-app that visualizes historic data from the German tennis results
site [**mybigpoint**](https://mybigpoint.tennis.de/).

In order to use the application a valid account is required at https://mybigpoint.tennis.de/.

> **Note**: The setup to make this analytics dashboard work on your local machine involves a few steps (see below). This application is for demonstration purposes only and will not be hosted in a production environment.

---
**Dependencies**
- Python: `https://www.python.org/downloads/`
- Grafana: `https://grafana.com/grafana/download`

---
**Architecture**
@@ add architecture overview

---
**Setup (Linux only)**

- install all Python dependencies:

  `pip install requirements.txt`

- install grafana json plugin:

 `sudo grafana-cli plugins install simpod-json-datasource`

- change to following configurations in `/etc/grafana/grafana.ini`:
```bash
allow_embedding: true
cookie_samesite: none
```
- start Grafana server and check status:
```bash
sudo service grafana-server start
sudo service grafana-server status
```
- navigate to `http://localhost:3000/` in your browser.
- login with following credentials:
```bash
user: admin
password: admin
```
- navigate to `+ --> Import --> Upload json File` and select the file `gf_dashboard.json` from the `dashboard` directory of this repo.

- open the dashboard in grafana and navigate to `Share dashboard`. Then navigate to the tab `Snapshot` and create a `Local Snapshot`. Copy this link into the `src` attribute of the `iframe` tag in `/app/templates/dashboard.html`.


---
**Usage**

- start the webserver via `bash start.sh` in root of this repo.

- in your browser go to `http://127.0.0.1:5000/`.

- login with your mybigpoint credentials and wait for data to be loaded.


---
**License**

Apache Software License 2.0
