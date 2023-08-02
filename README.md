# Export users data from SQL database (phpmyadmin) as a csv file

This code will export the data as csv file from your SQL database


Suppose you want to get users' data from different table and export it as csv file.

There is an array with name "to_find_list". In this array, write the information of the main table (i.e users) as an object. 


Similarly, write the details of other tables 
Make sure that the first table is the main table


Once done, set the "db_config" object to connect to your phpmyadmin database


When you run this code, it will get all the data from the fields you have written and save it as a csv file
Each row of the csv file will have data of each user from the tables and fields you have mentioned in the "to_find_list"


Happy exporting!
