%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The open items are as follows:</p>
<table border="1">
%for iteration, row in enumerate(rows):
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  %iteration += 1
  <td><button onclick="window.location.href='/ticket/{{ !iteration }}';">view</button></td>
  </tr>
%end
</table>