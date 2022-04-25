#Setup.sh

#install dependancies
pip install flask
pip install yara-python

# Clone yara rules
# By defalt all rule will be cloned under CDW/rules
git clone https://github.com/Yara-Rules/rules.git

#update index.yar with absolute full path and remove "MALW_AZORULT.yar" entry as it is causing error for yara-python
python3 indexWriter.py
