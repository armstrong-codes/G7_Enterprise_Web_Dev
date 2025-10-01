import xmltodict
import json

# Read the XML file
with open('yourfile.xml', 'r') as xml_file:
    xml_content = xml_file.read()

# Convert XML to dict
data_dict = xmltodict.parse(xml_content)

# Convert dict to JSON
json_data = json.dumps(data_dict, indent=4)

# Save to a JSON file
with open('modified_sms_v2.json', 'sms_momo.json') as json_file:
    json_file.write(json_data)