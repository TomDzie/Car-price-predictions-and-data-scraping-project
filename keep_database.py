import csv

daily_data_list = []
daily_id = []

with open('C:\\Users\\tom19\\VScode_Projects\\OTOmoto_project\\data\\data.csv', 'r', newline='') as daily:
    with open('C:\\Users\\tom19\\VScode_Projects\\OTOmoto_project\\data\\database.csv', 'r+', newline='') as database:

        daily_reader = csv.reader(daily)
        database_reader = csv.reader(database)
        writer = csv.writer(database)
        row_index = None

        for row in daily_reader:
            daily_data_list.append(row)
            daily_id.append(row[-1])
        
        for row in database_reader:
            if row[-1] in daily_id:
                row_index = daily_id.index(row[-1])
                daily_id.remove(row[-1])
                daily_data_list.remove(daily_data_list[row_index])
        for row in daily_data_list:
            writer.writerow(row)