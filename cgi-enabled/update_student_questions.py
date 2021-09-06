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
print "Content-type: text/html\n\n"
def cgiFieldStorageToDict(fieldStorage):
   params = {}
   for key in fieldStorage.keys( ):
      params[key] = fieldStorage[key].value
   return params


dict = cgiFieldStorageToDict(cgi.FieldStorage())


if dict.has_key('mode'): #see's if form variables have been sent
   #mode can either be new_question, delete_question or page_refresh
   if dict['mode'] == "new_question":
      sql = "INSERT INTO `Questions`(`id_Users`, `id_Teachers`, `Question`) VALUES (%s,%s,%s)"
      values = (dict['user_id'], 1, dict['new_question_text'])
      cursor.execute(sql, values)
      mydb.commit()
		
   if dict['mode'] == "delete":
      sql = "DELETE FROM `Questions` WHERE `key_Questions` = %s"
      cursor.execute(sql, (dict['question_id'],))
      mydb.commit()
		
   #driver that tests is the refresh is working correctly
   if dict['mode'] == "driver":
     print("<h1>Driver Test Successful</h1>")
   sql= "SELECT * FROM `Questions` WHERE `id_Users` = %s ORDER BY `DateOfQuestion` DESC"
   cursor.execute(sql, (dict['user_id'],))
   records = cursor.fetchall()
  
	print"""
		<h1>Your questions</h1>
				<table>
					<tbody>
   """	
   for record in records:
      print"<tr>"
      print"<td class='student_question'>" + record['Question'] + "</td>"
      print"<td rowspan='2' class='delete_column'> <button class='delete' value='" + str(record['key_Questions']) + "'>Delete</button></td>"
      print"<tr>"
      print"<td class='teacher_response'>" + str(record['Response']) + "</td>"
      print"""
				</tr>
				<tr>
					<td colspan='2'>&nbsp;</td>
				</tr>
      """
   print """
					</tbody>
				</table>
	<script>
	  $("button.delete").click(function(e) {
		e.preventDefault();
		$.ajax({
		  type: "GET",
		  url: "/SDDProject/cgi-enabled/update_student_questions.py",
		  data: {
			question_id: $(this).val(),
   """
   print "user_id: " + str(dict['user_id']) +  ",\n"
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
      </script>
   """

