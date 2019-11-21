<script>

$('#loader').addClass("hide-loader");
       
$("#btn11").click(function(){
                
var data_1 = {{ data | safe }};

obj = JSON.stringify(data_1);

swal({
title: "Are you sure?",
text: "Sending config commands to {{string_var}}, not reversible please double check and confirm!",
icon: "warning",
buttons: true,
dangerMode: true,
})
.then((willDelete) => {
  if (willDelete) {

  ////
  $.ajax({url:"/result", data: {"data": obj }, success: function(res){
    console.log(res);
  // return res is an array 
  var res_array = JSON.parse(res);
  console.log(res_array)
  $("#secret_field").append("<br> Return data is:  <br>" +  JSON.stringify(res_array));
  // res_array.push(res_dict);
  // console.log(res_dict);
//  
  var col = [];
  for (var i = 0; i < res_array.length; i++) {
    for (var key in res_array[i]) {
        if (col.indexOf(key) === -1) {
            col.push(key);
        }
    }
}
 
// 
// CREATE DYNAMIC TABLE.
var table = document.createElement("table");
    table.setAttribute("class", "w3-table-all");
    
    

// CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

var tr = table.insertRow(-1);                   // TABLE ROW.

for (var i = 0; i < col.length; i++) {
    var th = document.createElement("th");      // TABLE HEADER.
    th.setAttribute("class", "w3-green")
    th.innerHTML = col[i];
    tr.appendChild(th);
}

// ADD JSON DATA TO THE TABLE AS ROWS.
for (var i = 0; i < res_array.length; i++) {

    tr = table.insertRow(-1);

    for (var j = 0; j < col.length; j++) {
        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = res_array[i][col[j]];
    }
}

// FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
var divContainer = document.getElementById("createtable");
divContainer.innerHTML = "";
divContainer.appendChild(table);

// reveal secret field

var info_str = "<br> USERNAME: {{ session["cli_username"] }} <br>PASSWORD: {{ session["cli_password"] }} ";
    info_str = info_str + "<br>String variable:  {{ string_var }}";

$("#secret_field").append(info_str);

  }}); //end of ajax call
  ///   

    swal("Done configration!", {
      icon: "success",
    });
  } else {
    swal("No configure is pushed!");
  }
});

});  // end of button function


/////////////////// check select
$(".checkboxClass").click(function(){
let selectedCountry = new Array();
var n = $(".checkboxClass:checked").length;
if (n > 0){
    $(".checkboxClass:checked").each(function(){
        selectedCountry.push($(this).val());
    });
}
selected_config = selectedCountry
console.log(selectedCountry);
});
/////////////////// btn12 

$("#btn12").click(function(){
              
                console.log(selected_config)
                var data_1 = selected_config;
                
                obj = JSON.stringify(data_1);
                
                swal({
                title: "Are you sure?",
                text: "Sending config commands to {{string_var}}, not reversible please double check and confirm!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
                })
                .then((willDelete) => {
                  if (willDelete) {
                    // $('#loader').addClass("show-loader");
                    // $('#loader').removeClass("hide-loader");
                    $('#overlay').addClass("show-overlay");
                    $('#overlay').removeClass("hide-overlay");
                ////
                var data = {
                "ipaddress": JSON.stringify(["1.1.1.1"]),
                 "package": JSON.stringify(selected_config),
               };

                obj = JSON.stringify(data);

                function your_func() {
                  $.ajax({url:"/TechType_fix_config", data: {"data": obj }, success: function(res_str){
                  console.log(res_str);
                
                // delay 5 secs to show the loader effect


                  // return res is an array 
                  var res_array = JSON.parse(res_str);
                  console.log(res_array);
                  $("#secret_field").empty();
                  $("#secret_field").append("<br> Return data is:  <br>" +  JSON.stringify(res_array));
                  // res_array.push(res_dict);
                  // console.log(res_dict);
                //  
                  
                // reveal secret field
        
                var info_str = "<br> USERNAME: {{ session["cli_username"] }} <br>PASSWORD: {{ session["cli_password"] }} ";
                    info_str = info_str + "<br>String variable:  {{ string_var }}";
         
                $("#secret_field").append(info_str);

                $('#overlay').addClass("hide-overlay");
                $('#overlay').removeClass("show-overlay");

                  }}); //end of ajax call
                  console.log("noop");
                }
                setTimeout(function() { your_func(); }, 2000);
                
                  ///   
        
                    swal("Done configration!", {
                      icon: "success",
                    });
           

                  } else {
                    swal("No configure is pushed!");
                    }
               });  //end of then

}); // end of button 12 function

/////////////////// btn13
$("#btn13").click(function () {
try {
  let response = fetch('/', {
    method: "GET",

  })
  let data = await response;
  console.log(data);
  if (!data.r) {
    $('#fetch_result').html(data.rs);

  } else {
    $('#fetch_result').html(data.error);
  }

} catch (e) {
  console.log("something wrong", e);
}
}); //end of button 13 function

</script>