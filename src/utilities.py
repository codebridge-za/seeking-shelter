def parse_tel_numbers(raw_tel_text):
    final_numbers = []
    separate_numbers = raw_tel_text.split(',') # "011222333, 011444444/5"
    for number_set in separate_numbers:
        numbers = number_set.split('/') # "011444444/5"
        for i in range(1, len(numbers)):
            numbers[i] = numbers[0][:-len(numbers[i])] + numbers[i]
        final_numbers.extend(numbers)
    return final_numbers
