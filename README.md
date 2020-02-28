### ml-practice 

#### First things to do
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e . // install sejongpatch module
```

##### Tests 
* Run all tests: ``` pytest .```
* Run only unit tests: ```pytest -v -m "not functional"```