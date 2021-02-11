import json


def read_data():
    with open('test.json') as file_json:
        data = json.load(file_json)
    return data

def main():
    input_data = read_data()
    print(input_data)

if __name__ == "__main__":
    main()