%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<style>
body {
  background-color: lightblue;
} 
h1 {
  color: navy;
  margin-left: 20px;
}
.titletext {
  text-align: center; 
  color: darkblue;
}
table {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border-bottom: 1px solid #ddd;
}
th {
  background-color: #04AA6D;
  color: white;
}
tr:hover {background-color: yellow;}
.backbtn{
    position: absolute;
    left: 10px;
}
</style>
<p><center>The open items are as follows:</p>
<table border="1">
<tr>
  <th> ID </th>
  <th> NAME </th>
  <th> PHONE NO. </th>
  <th> DATE CREATED </th>
  <th> DEVICE </th>
  <th> DETAILS </th>
</tr>
%for iteration, row in enumerate(rows):
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  %iteration += 1
  <td><button onclick="window.location.href='/ticket/{{ !iteration }}';">DETAILS</button></td>
  </tr>
%end
</table>
<button class=backbtn onclick="window.location.href='/home';">
Back
</button>