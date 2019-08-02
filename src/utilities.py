import csv

def get_places(data_file):
    with open(data_file) as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for i in range(1, len(rows)):
        rows[i]['Tel'] = parse_tel_numbers(rows[i]['Tel'])
    return rows

def parse_tel_numbers(raw_tel_text):
    final_numbers = []
    separate_numbers = raw_tel_text.split(',') # "011222333, 011444444/5"
    for number_set in separate_numbers:
        numbers = number_set.split('/') # "011444444/5"
        if len(numbers) == 1:
            if len(numbers[0]) == 9:
                numbers[0] = '0' + str(numbers[0])
        for i in range(1, len(numbers)):
            numbers[i] = numbers[0][:-len(numbers[i])] + numbers[i]
        final_numbers.extend(numbers)
    return final_numbers
