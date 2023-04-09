import json

rows = {}
file = 'C:/Users/Kanan/Desktop/EUScrapper/EUScraper/results.json'
write_file = 'C:/Users/Kanan/Desktop/EUScrapper/EUScraper/write_results.json'

with open(file, 'r', encoding='utf-8') as json_file:
    with open(write_file, 'w', encoding='utf-8') as json_write_file:
        for line in json_file:
            try:
                data = json.loads(line)
                if not data['url'] in rows.keys():
                    rows[data['url']] = data
                    json_write_file.write(line)
            except Exception as exc:
                print(exc)

print(rows)