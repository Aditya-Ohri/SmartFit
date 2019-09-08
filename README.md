# SmartFit

## Set up and run locally!
Create the virtual environment, install dependencies, and run the web server
```python
def generate_virtualenv_activation_cmd():
  if OS == 'Windows':
    yield '.\venv\Scripts\activate.bat'
  else:
    yield 'source venv/bin/activate'

# set up virtualenv
generate_virtualenv_activation_cmd()

# install deps & run
subprocess.check_call("""pip install -r requirements.txt && python main.py""")
```

Open up a browser, go to ```http://localhost:5000```, and begin **living healthier** :tada:
