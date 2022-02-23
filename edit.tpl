%#template to generate a UI to edit a ticket with
<style>
body {
  background-color: lightblue;
} 
h1 {
  color: navy;
  margin-left: 20px;
}
.titletext {
  text-align: left; 
  color: darkblue;
  display: inline-block;
}
.btncontain {
    text-align: center;
}
.btn{
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
}
.backbtn{
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
}
.head{
    display: inline-block
}
</style>


<body>
<div class=head>
<h1 class = titletext>Ticket #{{ticketno}}</h1>
<h1 class = titletext>Phone: {{phone}}</h1>
<button class=backbtn onclick="window.location.href='/tickets';">
Back
</button>
</div>


<h1><center> Create Ticket </h1>
<form action="/editticket/{{ticketno}}" method="post"><center> <br> <br> <br>
DETAILS: <input name="details" type="text" required value='{{details}}' size=150/> <br> <br>
<input value="Submit Edit" type="submit" />
</form>
