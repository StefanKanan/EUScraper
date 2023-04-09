import json

rows = {}
file = 'C:/Users/Kanan/Desktop/EUScrapper/EUScraper/results_all_divide.json'
write_file = 'C:/Users/Kanan/Desktop/EUScrapper/EUScraper/'

export_to_files = {'http://www.nalas.eu/Press-Centre/press-releases': 'press_releases.json',
                   'http://www.nalas.eu/Publications/Books': 'books.json',
                   'http://www.nalas.eu/Publications/Newsletter': 'newsletter.json',
                   'http://www.nalas.eu/News': 'news.json',
                   'http://nalas.eu/knowledge-center/Policy-positions': 'policy_papers.json',
                   'http://nalas.eu/services/quick-responces': 'quick_responses.json'}
jsons = {}

with open(file, 'r', encoding='utf-8') as json_file:
    for line in json_file:
        try:
            data = json.loads(line)
            for key, val in export_to_files.items():
                if key.lower() in data['parent_url'].lower():
                    if key.lower() not in jsons.keys():
                        jsons[key.lower()] = []
                    jsons[key.lower()].append(line)
        except Exception as exc:
            print(exc)

for key, val in export_to_files.items():
    new_write_to_file = f'{write_file}{val}'
    lines = jsons[key.lower()]
    with open(new_write_to_file, 'w', encoding='utf-8') as json_write_file:
        json_write_file.writelines(lines)

print(jsons)