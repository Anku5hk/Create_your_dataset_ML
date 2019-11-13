import xml.etree.ElementTree as ET
import csv
import re
import textwrap
from typing import List, Any

# provide .xml file location
tree = ET.parse('/Downloads/sms-demo.xml')
root = tree.getroot()

sender_types = []
messages = []
dates_days = []
timestamp_data = []
contact_names = []
contact_address = []


# Extract useful aspects to work on
def extract_data():
    for child in root:
        dic = child.attrib
        sender_types.append(int(dic['type']))  # capture the sender type(me or some person)
        messages.append(dic['body'])  # actual message
        dates_days.append(dic['readable_date'])  # extract date
        timestamp_data.append(dic['date'])  # timestamp data
        contact_names.append(dic['contact_name'])  # name of sender
        contact_address.append(dic['address'])  # for unsaved contacts


from_data = []
to_data = []


# extract the sender and receiver with sender_types
def from_to_tab():
    for var in range(len(sender_types)):
        if sender_types[var] == 1:
            from_data.append(contact_names[var])
            to_data.append('ME')
        else:
            from_data.append('ME')
            to_data.append(contact_names[var])


new_names = []  # contains all saved and unsaved contacts names


# unsaved contacts use contact_address as name eg HP-AMAZON for texts from amazon sellers
def unknown_data_resolver():
    for var in range(len(from_data)):
        if from_data[var] == '(Unknown)':
            new_names.append(contact_address[var])
        else:
            new_names.append(from_data[var])


extract_data()
from_to_tab()
unknown_data_resolver()
person_name = set(new_names)  # unique namespace for all contacts
clusters = []
to_cluster = []

# mention any of the missing names if giving errors from cluster() method
missing_names = {'(Unknown)': 488}


# create a cluster to separate the conversations and get a extra feature.
def cluster(count=0):
    for name in new_names:
        if name in person_name:  # unique name
            count += 1  # assign cluster id
            if count not in missing_names.values():  # add to dictionary to be able to bring their name back if repeated
                missing_names[name] = count
                person_name.remove(name)
                clusters.append(count)
        else:
            prev_count = missing_names[name]  # repeated person so assigning dictionary's cluster_id
            clusters.append(prev_count)


cluster()
dates = []
months = []
days = []
years = []
times = []


# extract date, month, year and time separate from dates_day
def to_date():
    for date in range(len(dates_days)):
        split_string = re.split(r'[\s]', dates_days[date])
        months.append(split_string[0])
        days.append(split_string[1].replace(',', ''))
        years.append(split_string[2])
        times.append(split_string[3])


to_date()

formated_date = []


# create human readable dates in format preferred
def create_date():
    for num in range(len(dates_days)):
        formated_date.append(days[num] + '-' + months[num] + '-' + years[num])


# limit the size of characters per messages as it creates bloat in dataset(continues to a new column).
shorten_messages = []
for msg in messages:
    shorten_messages.append(textwrap.shorten(msg, width=250, placeholder="..."))  # to 250 on the safe side max length
    # is 255.

create_date()

# rows = ['From||', ' To||', 'Conversation_Id||', 'Date||', 'Message||', 'Time'] # name the columns of datasets

with open('/home/anku5h/Downloads/sms-demo-data.csv', 'w') as csvFile:  # new csv file location
    writer = csv.writer(csvFile)
    # writer.writerow(rows)
    for row in range(len(messages)):
        writer.writerow([str(new_names[row]) + '&&' + str(to_data[row]) + '&&' + str(clusters[row]) + '&&' +
                         str(formated_date[row]) + '&&' + str(timestamp_data[row])+ '&&' + str(shorten_messages[row])
                         + '&&' + str(times[row])])
        # used custom delimiter '&&' to differentiate columns
    if writer:
        print('Success')  # simple done message
csvFile.close()
