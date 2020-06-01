;(function() {
  function Tablesort(el, options) {
    if (!(this instanceof Tablesort)) return new Tablesort(el, options);

    if (!el || el.tagName !== 'TABLE') {
      throw new Error('Element must be a table');
    }
    this.init(el, options || {});
  }

  var sortOptions = [];

  var createEvent = function(name) {
    var evt;

    if (!window.CustomEvent || typeof window.CustomEvent !== 'function') {
      evt = document.createEvent('CustomEvent');
      evt.initCustomEvent(name, false, false, undefined);
    } else {
      evt = new CustomEvent(name);
    }

    return evt;
  };

  var getInnerText = function(el) {
    return el.getAttribute('data-sort') || el.textContent || el.innerText || '';
  };

  // Default sort method if no better sort method is found
  var caseInsensitiveSort = function(a, b) {
    a = a.trim().toLowerCase();
    b = b.trim().toLowerCase();

    if (a === b) return 0;
    if (a < b) return 1;

    return -1;
  };

  // Stable sort function
  // If two elements are equal under the original sort function,
  // then there relative order is reversed
  var stabilize = function(sort, antiStabilize) {
    return function(a, b) {
      var unstableResult = sort(a.td, b.td);

      if (unstableResult === 0) {
        if (antiStabilize) return b.index - a.index;
        return a.index - b.index;
      }

      return unstableResult;
    };
  };

  Tablesort.extend = function(name, pattern, sort) {
    if (typeof pattern !== 'function' || typeof sort !== 'function') {
      throw new Error('Pattern and sort must be a function');
    }

    sortOptions.push({
      name: name,
      pattern: pattern,
      sort: sort
    });
  };

  Tablesort.prototype = {

    init: function(el, options) {
      var that = this,
          firstRow,
          defaultSort,
          i,
          cell;

      that.table = el;
      that.thead = false;
      that.options = options;

      if (el.rows && el.rows.length > 0) {
        if (el.tHead && el.tHead.rows.length > 0) {
          for (i = 0; i < el.tHead.rows.length; i++) {
            if (el.tHead.rows[i].getAttribute('data-sort-method') === 'thead') {
              firstRow = el.tHead.rows[i];
              break;
            }
          }
          if (!firstRow) {
            firstRow = el.tHead.rows[el.tHead.rows.length - 1];
          }
          that.thead = true;
        } else {
          firstRow = el.rows[0];
        }
      }

      if (!firstRow) return;

      var onClick = function() {
        if (that.current && that.current !== this) {
          that.current.removeAttribute('aria-sort');
        }

        that.current = this;
        that.sortTable(this);
      };

      // Assume first row is the header and attach a click handler to each.
      for (i = 0; i < firstRow.cells.length; i++) {
        cell = firstRow.cells[i];
        cell.setAttribute('role','columnheader');
        if (cell.getAttribute('data-sort-method') !== 'none') {
          cell.tabindex = 0;
          cell.addEventListener('click', onClick, false);

          if (cell.getAttribute('data-sort-default') !== null) {
            defaultSort = cell;
          }
        }
      }

      if (defaultSort) {
        that.current = defaultSort;
        that.sortTable(defaultSort);
      }
    },

    sortTable: function(header, update) {
      var that = this,
          column = header.cellIndex,
          sortFunction = caseInsensitiveSort,
          item = '',
          items = [],
          i = that.thead ? 0 : 1,
          sortMethod = header.getAttribute('data-sort-method'),
          sortOrder = header.getAttribute('aria-sort');

      that.table.dispatchEvent(createEvent('beforeSort'));

      // If updating an existing sort, direction should remain unchanged.
      if (!update) {
        if (sortOrder === 'ascending') {
          sortOrder = 'descending';
        } else if (sortOrder === 'descending') {
          sortOrder = 'ascending';
        } else {
          sortOrder = that.options.descending ? 'descending' : 'ascending';
        }

        header.setAttribute('aria-sort', sortOrder);
      }

      if (that.table.rows.length < 2) return;

      // If we force a sort method, it is not necessary to check rows
      if (!sortMethod) {
        while (items.length < 3 && i < that.table.tBodies[0].rows.length) {
          item = getInnerText(that.table.tBodies[0].rows[i].cells[column]);
          item = item.trim();

          if (item.length > 0) {
            items.push(item);
          }

          i++;
        }

        if (!items) return;
      }

      for (i = 0; i < sortOptions.length; i++) {
        item = sortOptions[i];

        if (sortMethod) {
          if (item.name === sortMethod) {
            sortFunction = item.sort;
            break;
          }
        } else if (items.every(item.pattern)) {
          sortFunction = item.sort;
          break;
        }
      }

      that.col = column;

      for (i = 0; i < that.table.tBodies.length; i++) {
        var newRows = [],
            noSorts = {},
            j,
            totalRows = 0,
            noSortsSoFar = 0;

        if (that.table.tBodies[i].rows.length < 2) continue;

        for (j = 0; j < that.table.tBodies[i].rows.length; j++) {
          item = that.table.tBodies[i].rows[j];
          if (item.getAttribute('data-sort-method') === 'none') {
            // keep no-sorts in separate list to be able to insert
            // them back at their original position later
            noSorts[totalRows] = item;
          } else {
            // Save the index for stable sorting
            newRows.push({
              tr: item,
              td: getInnerText(item.cells[that.col]),
              index: totalRows
            });
          }
          totalRows++;
        }
        // Before we append should we reverse the new array or not?
        // If we reverse, the sort needs to be `anti-stable` so that
        // the double negatives cancel out
        if (sortOrder === 'descending') {
          newRows.sort(stabilize(sortFunction, true));
        } else {
          newRows.sort(stabilize(sortFunction, false));
          newRows.reverse();
        }

        // append rows that already exist rather than creating new ones
        for (j = 0; j < totalRows; j++) {
          if (noSorts[j]) {
            // We have a no-sort row for this position, insert it here.
            item = noSorts[j];
            noSortsSoFar++;
          } else {
            item = newRows[j - noSortsSoFar].tr;
          }

          // appendChild(x) moves x if already present somewhere else in the DOM
          that.table.tBodies[i].appendChild(item);
        }
      }

      that.table.dispatchEvent(createEvent('afterSort'));
    },

    refresh: function() {
      if (this.current !== undefined) {
        this.sortTable(this.current, true);
      }
    }
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = Tablesort;
  } else {
    window.Tablesort = Tablesort;
  }
})();

let selected_config = new Array();
 $(document).ready(function(){
   
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

 fetchtest();

 })  //end of btn13 function

/////////////////// btn13
$("#btn14").click(function () {

  fetch_db_data();
 
  })  //end of btn14 function
 

}); // end of document ready
 
  

async function fetchtest() {

let response = await fetch('/fetch');

if (response.ok) { // if HTTP-status is 200-299
 // get the response body (the method explained below)
 let json = await response.text();
 console.log(typeof (json))  // string
 console.log("json out is here...");
 console.log(json);
 $("#fetch_result").html(json)  
} else {
 alert("HTTP-Error: " + response.status);
}

}

async function fetch_db_data() {

  let response = await fetch('/simpledb');
  
  if (response.ok) { // if HTTP-status is 200-299
   // get the response body (the method explained below)
   let res_string= await response.text();
   res_array  = JSON.parse(res_string)
   console.log(typeof res_array); // string
   console.log("json out is here...");
   console.log(res_array);
  //  $("#fetch_db_result").html(JSON.parse(res_array))  
   $("#fetch_db_result").append("<br> Return data is:  <br>" + JSON.stringify(res_array));
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
       table.setAttribute("class", "sort");
      //  table.setAttribute("class", "");
       table.setAttribute("id", "my_table");
    
  //  var thread = document.createElement("thread");
  //      table.appendChild(thread);
   var tr_1 = table.insertRow();
      //  thread.appendChild(tr_1);
    
       for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        // th.setAttribute("class", "w3-green");
        th.setAttribute("class", "sort-header");
        
        th.innerHTML = col[i];
        tr_1.appendChild(th);
    }
      //  table.append(thread);

   // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.


   // ADD JSON DATA TO THE TABLE AS ROWS.
   for (var i = 0; i < res_array.length; i++) {

       tr = table.insertRow();

       for (var j = 0; j < col.length; j++) {
           var tabCell = tr.insertCell(-1);
          //  tabCell.setAttribute("role", "cell");
           tabCell.innerHTML = res_array[i][col[j]];
       }
   }

   // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
   var divContainer = document.getElementById("db_table");
   divContainer.innerHTML = "";
   divContainer.appendChild(table);
   new Tablesort(document.getElementById('my_table'));

  } else {
   alert("HTTP-Error: " + response.status);
  }
  
  }