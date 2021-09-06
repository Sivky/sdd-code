#!/usr/bin/env python

import cgi, cgitb
import mysql.connector
cgitb.enable()
# Create MySQL Connection
mydb = mysql.connector.connect(
	host = "10.0.0.34",
	user = "SDDProject",
	passwd = "lpyjfre",
	database = "SDDMajorProject"
)


cursor = mydb.cursor(dictionary=True)


#create a variable named dict which stores the posted form data
def cgiFieldStorageToDict(fieldStorage):
   """ Get a plain dictionary rather than the '.value' system used by the 
   cgi module's native fieldStorage class. """
   params = {}
   for key in fieldStorage.keys(  ):
      params[key] = fieldStorage[key].value
   return params
dict = cgiFieldStorageToDict(cgi.FieldStorage())


# Tell the broswer that the output of this script is html
print "Content-type: text/html\n\n"


# Test to see if data has been posted to this script. If the page is access directly rather that through the login form, the form variable will be empty
if dict.has_key('username'):
	# If the variables include one named username then the login form has been submitted so search the MySql database to see if there is a user identified by the username and password form variables
	sql = "SELECT * FROM `Users` WHERE `UserName` LIKE %s AND `UserPass` LIKE %s"
	values = (dict['username'], dict['password'])
	cursor.execute(sql, values)
	records = cursor.fetchall()

	# Store a variable named userexists so we can record whether a user has been found with the username and password
	userexists = False
	for record in records:
		# A user exists so test to see if they are a student or teacher in the mysql record
		userexists = True
		if record['AuthLevel'] == 'Stud':
			# Create the student page including the user id in the scripts to distinguish this user  according to the log in details
			print """
			<!doctype html>
			<html>
			<head>
				<meta charset="UTF-8">
				<title>StudentPage</title>
				<link href="../student.css" rel="stylesheet" type="text/css">
				<script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
				<script src="../library/jquery-3.6.0.min.js"></script> 
			</head>

			<body>
				<div id="Menubar">
					<p id="page_identity">Student Page</p>
					<button id="logout" ><a href="../">Log Out</a></button>
				</div>
				<div id="body_page">
                                  <button id="driver_test">Driver</button>
					<div id="left_container">
						<form id="new_question" action="" method="get">
							<h1>Ask a question</h1>
							<input type="text" id="textbox_newQuestion" name="new_question" placeholder="Enter Question">
			"""
			print "<input type='hidden' name='student_id' value='" + str(record['key_Users']) +"'>"
			print """
							<button id="submit_new_q">Submit</button>
						</form>	
						<div id="past_questions">
							<h1>Loading...</h1>
						</div>
					</div>
					<div id="raise_hand">
						<p></p>
					</div>
				</div>
				<script>



				  var id = setInterval(function() {
				  $.ajax({ method: "get",url: "/SDDProject/cgi-enabled/update_student_questions.py",
			"""
			print 'data: "mode=all&user_id=' + str(record['key_Users']) + '",' 
			print """
				  success: function(html){$("#past_questions").html(html); 
				  }});
				}, 1000);

				</script>
				<script>


	$("#driver_test").click(function(e) {
		e.preventDefault();
		$.ajax({
		  type: "GET",
		  url: "/SDDProject/cgi-enabled/update_student_questions.py",
		  data: {
			new_question_text: $("#textbox_newQuestion").val(),
			user_id: 1,
			mode: "driver"
		  },
		  success: function(html) {
			$("#past_questions").html(html); 
		  },
		  error: function(result) {
			alert('There was an error running the driver.');
		  }
              });
	});


				  $("button.delete").click(function(e) {
					e.preventDefault();
				        $.ajax({
					  type: "GET",
					  url: "/SDDProject/cgi-enabled/update_student_questions.py",
					  data: {
						question_id: $(this).val(),
			"""
			print "user_id:" + str(record['key_Users']) + ", \n"
			print """
						mode: "delete"
					  },
					  success: function(html) {
						$("#past_questions").html(html); 
					  },
					  error: function(result) {
     					alert('There was an error deleting the question.');
					  }
				   });
				  });



				$("#submit_new_q").click(function(e) {
					e.preventDefault();
					$.ajax({
					  type: "GET",
					  url: "/SDDProject/cgi-enabled/update_student_questions.py",
					  data: {
						new_question_text: $("#textbox_newQuestion").val(),
			"""
			print "user_id:" + str(record['key_Users']) + ", \n"
			print """
						mode: "new_question"
					  },
					  success: function(html) {
						$("#past_questions").html(html); 
					  },
					  error: function(result) {
						alert('There was an error deleting the question.');
					  }
					});
					$('#new_question').trigger("reset");
				  });
				</script>
			</body>
			</html>
			"""
		elif record['AuthLevel'] == 'Teach':
			print("Serve up teacher")
	if userexists == False:
		print("Account not found")
cursor.close()
mydb.close()



