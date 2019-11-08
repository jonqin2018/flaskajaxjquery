
$(function(){
	$('button').click(function(){
		$.ajax({
			url: '/signupuser',
			data:{"mydata": "world"},
			type: 'POST',
			success: function(response){
				console.log(response);
				alert("success");
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});


