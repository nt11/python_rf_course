import pandas as pd

if __name__ == "__main__":
   print("Results")
   print("-------")
   # Create DataFrame from dictionary
   data_dict = {
      'name': ['John', 'Anna', 'Peter'],
      'age': [25, 30, 35],
      'city': ['NY', 'LA', 'SF']
   }
   df1 = pd.DataFrame(data_dict)
   # Create from list of lists
   data_list = [
      ['John', 25, 'NY'],
      ['Anna', 30, 'LA'],
      ['Peter', 35, 'SF']
   ]
   df2 = pd.DataFrame(data_list, columns=['name', 'age', 'city'])
   # Save to CSV
   df1.to_csv('people.csv', index=False)
   # Read back from CSV
   df3 = pd.read_csv('people.csv')
   # Convert to different formats
   dict_format = df1.to_dict()
   dict_records_format = df1.to_dict('records')
   list_format = df1.values.tolist()

   print(df1)
   print("\nAs dictionary:",dict_format)
   print("\nAs list of lists:",list_format)
   print("\nAs list of dictionaries:",dict_records_format)