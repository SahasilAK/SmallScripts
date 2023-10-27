import os
import sys
import csv
import re

def find_word_combinations(root_dir, list_of_table_cols, default_value):
    results = []
    valid_sql_extensions = {'.sql'}  # Set of valid SQL file extensions
    word1 = 'from'
    word3 = default_value

    # Create sets for faster membership tests
    list_of_table_cols = {(col1.lower(), col2.lower()) for col1, col2 in list_of_table_cols}
  

    # Compile regex patterns outside the loop
    pattern_set=[]
    for word2, word4 in list_of_table_cols:
        pattern_string_1 = r'\b{}\b.*?\b{}\b'.format(word1,word2)
        pattern_string_2 = r'\b{}\b.*?\b{}\b'.format(word3,word4)
        pattern1 = re.compile(pattern_string_1, re.DOTALL)
        pattern2 = re.compile(pattern_string_2, re.DOTALL)
        pset=(pattern1,pattern2,word2,word4)
        pattern_set.append(pset)
 


    sql_file_count = 0  # Initialize a counter for SQL files

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            _, file_extension = os.path.splitext(filename)
            if file_extension.lower() in valid_sql_extensions:
                sql_file_count += 1  # Increment the counter for each SQL file found

                file_path = os.path.join(dirpath, filename)

                with open(file_path, "r") as file:
                    sql_content = file.read().lower()
                    
                    for pattern1,pattern2,word2,word4 in set(pattern_set):
                        match1 = pattern1.search(sql_content)
                        match2 = pattern2.search(sql_content)

                        if match1 and match2:
                            result = (word2, word4, file_path)
                            results.append(result)

    return sql_file_count, results  # Return the SQL file count along with the word combinations

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print( "Usage: python script.py <csv_path> [<default_value>]")
        sys.exit(1)

    root_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        default_value = sys.argv[2]
    else:
        default_value = "where"  # Set your default value here

    with open(csv_path, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        list_of_table_cols = [ls[1:3] for ls in list(csvreader)][1:]

    sql_file_count, word_combinations = find_word_combinations(root_path, list_of_table_cols, default_value)

    print( "Total SQL files found: {}".format(sql_file_count))

    output_file_path = "sql_file_paths.txt"

    with open(output_file_path, "w") as output_file:
        output_file.write("Total SQL files found: {}\n".format(sql_file_count))
        output_file.write("-" * 50)

        if word_combinations:
            for combination in word_combinations:
                output_file.write("\ntable_name: {}\ncolumn_name: {}\nFile Path: {}\n\n".format(combination[0], combination[1], combination[2]))
                output_file.write("-" * 50)
            print( "Output saved to {}".format(output_file_path))
        else:
            print( "No word combinations found.")
