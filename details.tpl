%#template to generate a details table from the data collected in a ticket 
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
.info {
    font-size: 30px;
    text-align: center;
    word-wrap: normal;
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
.content {
    width: window.innerWidth;
}
</style>


<body>
<div class=content>
<div class=head>
<h1 class = titletext>Ticket #{{ticketno}}</h1>
<h1 class = titletext>Phone: {{phone}}</h1>
<button class=backbtn onclick="window.location.href='/tickets';">
Back
</button>
</div>

<div class=info>
<p> Customer Name: {{name}} <br>
    Date Created: {{date}}  <br>
    Device: {{device}}      <br>
    <br>
    Details: <br>
    {{details}}
</p>
</div>

<div class=btncontain>
<button class=btn onclick="window.location.href='https://gatech.co.nz/';">
Parts
</button>
<button class=btn onclick="window.location.href='/closeticket/{{ticketno}}';">
!CLOSE TICKET!
</button>
<button class=btn onclick="window.location.href='/editticket/{{ticketno}}';">
Edit Details
</button>
</div>
</div>