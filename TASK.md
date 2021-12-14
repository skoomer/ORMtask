Create own ORM based on psycopg2

1. Establish connection to DB in the most convenient way. Close connection;

2. Create class which represents varchar, integer, boolean, datetime, onetoone, onetomany fields in DB

	2.1. Varchar fields length should be configurable

	2.2. Max and min values of the integer field should be configurable
 
	2.3. Datetime field should work with date and datetime string formats


3. Create a class which represents a single table in DB. Columns of a table should be represented as attributes of the class


4. Implement the next functionality:
   
   4.0. Create tables of DB. Based on the used models


   4.1. Each table should include a primary key field.

   4.2. Get a single row of a table and work with it as an instance of the class;

   4.3. Get all rows from a table and work with them as list of namedtuple objects;

   4.4. Add possibility to filter all select queries;

   4.5. Update single row;

   4.6. Update filtered list of rows;

   4.7. Remove single row;

   4.8. Remove filtered list of rows;

   4.9. Get string representation of the class instance;

   4.10. Configurable Table name;

   4.11. Add possibility to join related tables and models; 

   4.12. Implemented such named lazy queries


 5. Add tests

 6. Add docker-compose file with the DB and instruction to populate DB if needed

 7. Add file with dependencies

 8. Add instruction to start project and base examples of usage;
