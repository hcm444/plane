import csv

# Open the input and output files
with open('GlobalAirportDatabase.txt', 'r') as input_file, open('GlobalAirportDatabase.csv', 'w', newline='') as output_file:
    # Create a CSV reader and writer
    reader = csv.reader(input_file, delimiter=':')
    writer = csv.writer(output_file)

    # Iterate through the rows in the input file
    for row in reader:
        # Check if the last two columns contain "0.000"
        if row[-2] != "0.000" and row[-1] != "0.000":
            # Slice the row list to select the desired columns
            selected_columns = [row[0], row[1], row[2], row[3], row[4], row[-2], row[-1]]
            writer.writerow(selected_columns)
