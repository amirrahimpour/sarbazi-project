import csv
import json


def save_csv(index_reader, attribute_names):
    make_row = lambda record, key: record[key] if key in record.keys() else ''
    with open('LogDB.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=attribute_names)
        writer.writeheader()
        i = 0
        for record in index_reader:
            new_row = {key: make_row(record['_source'], key) for key in attribute_names}
            writer.writerow(new_row)
            i += 1
    print("The number of records: %d" % i)


def save_json(index_reader):
    with open('../static/LogDB.json', 'w', encoding='utf-8') as jsonfile:
        flag = False
        jsonfile.write("[")
        i = 0
        for record in index_reader:
            if flag:
                jsonfile.write(",\n")
            json.dump(record['_source'], jsonfile, ensure_ascii=False, indent=4)
            flag = True
            i += 1
        jsonfile.write("]")
    print("The number of records: %d" % i)
