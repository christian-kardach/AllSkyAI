# AllSkyAI

This is a simple classification REST server for classifying AllSky live images, the result will be returned as a JSON string:

`{"AllSkyAISky": "light_clouds", "AllSkyAIConfidence": 94.00085210800171, "UTC": 1668109745.83148}`

## Requirement
* Python 3.9

## Installation
* Clone the repository, for example to `D:\Repositories\AllSkyAI`
* Create a Virtual Environment `C:\> C:\Python39\python -m venv D:\Repositories\AllSkyAI\venv`
* Activate virtual environment 
  * Activate from CMD - `D:\Repositories\AllSkyAI> .\venv\Scripts\activate.bat`
  * or
  * Activate from PS - `PS D:\Repositories\AllSkyAI> .\venv\Scripts\Activate.ps1`
* Install requirements - `pip install -r requirements.txt`*
* Deactivate venv
  * CMD - `D:\Repositories\AllSkyAI> .\venv\Scripts\deactivate.bat`
  * PS - `deactivate`
* Update the URL in the `.env` file
* Start the server
  * `D:\Repositories\AllSkyAI\venv\Scripts\python.exe .\app.py`
    
Start a browser and check the response:
`http://127.0.0.1:5000/classifylive?type=bw` or `http://127.0.0.1:5000/classifylive?type=color`