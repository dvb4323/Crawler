import json

def format_json_file(input_file, output_file):
    # Read the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    # Write back the data with proper character formatting and sorting
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)

if __name__ == "__main__":
    input_file = 'scraped_data.json'
    output_file = 'formatted_data.json'
    format_json_file(input_file, output_file)
    print(f"Formatted JSON data has been saved to '{output_file}'")
