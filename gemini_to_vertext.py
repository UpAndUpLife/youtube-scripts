import csv
import json

# Define the input and output file paths
csv_file_path = './out/legacy/_video_transcripts_UCcYzLCs3zrQIBVHYA1sK2sw.csv'
json_file_path = 'output.json'

# Initialize an empty list to store the JSON data
json_data = []

# Read the CSV file and process each row
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        # Create the JSON structure for each row
        json_row = {
            "messages": [
                {"role": "user", "content": row['Title']},
                {"role": "model", "content": row['Transcript']}
            ]
        }
        # Append the JSON structure to the list
        json_data.append(json_row)

# Write the JSON data to a file
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=2)

print(f"Converted CSV to JSON and saved to {json_file_path}")
