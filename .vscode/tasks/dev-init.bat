mkdir venv
py -m venv venv
venv/Scripts/activate
py -m pip install -r requirements.txt
venv/Scripts/deactivate
echo Requirements have been installed in the venv
echo Please ensure to set the Python interpriter to the venv interpriter for testing