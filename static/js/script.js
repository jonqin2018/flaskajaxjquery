
// $(function(){
// 	$('button').click(function(){
// 		$.ajax({
// 			url: '/signupuser',
// 			data:{"mydata": "world"},
// 			type: 'POST',
// 			success: function(response){
// 				console.log(response);
// 				alert("success");
// 			},
// 			error: function(error){
// 				console.log(error);
// 			}
// 		});
// 	});
// });

function CreateTable(rowCount,cellCount)
{
  $("#createtable").empty();
   var table=$("<table border='1' cellspacing='0'> </table>");
   table.appendTo($("#createtable"));

   var trh=$("<tr></tr>");
   trh.appendTo(table);

   for(var h=0; h<cellCount; h++)
   {
	  var th = $("<th>" +h+"</th>");
	  th.appendTo(trh);
   }

   for(var i=0;i<rowCount;i++)
   {
	  var tr=$("<tr></tr>");
	  tr.appendTo(table);
	  for(var j=0;j<cellCount;j++)
	  {
		 var td=$("<td>"+i*j+"</td>");
		 td.appendTo(tr);
	  }
   }

}

