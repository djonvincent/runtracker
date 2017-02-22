$(document).ready(function(){
   var runData;
   //Initialise empty chart
   var chart = new Chart($('#chart'));
   //Get the time frame to display data between
   var timeFrame = $('#timeFrameOption').val();
   //Get token so we can submit forms with protection from CSRF
   var csrftoken = $("[name=csrfmiddlewaretoken]").val();
   //Get the data from the server to populate chart
   updateTimeFrame(timeFrame);
   
   //Toggle between dropdown and custom time inputs
   $("#customRangeBox").change(function(){
      var checked = $(this).prop('checked');
      $('#upperDate, #lowerDate, #getRunsButton').prop('disabled', !checked);
      $('#timeFrameOption').prop('disabled', checked);
   });
   
   //Update time frame when user selects option, then update chart
   $('#timeFrameOption').change(function(){
      timeFrame = $(this).val();
      updateTimeFrame(timeFrame);
   });
   
   //Change chart data when user changes the variable to display
   $('#y-variable').change(function(){
      //Destroy old chart first
      chart.destroy();
      drawChart($(this).val());
   });
   
   //Validate and submit add run form when user clicks submit
   $('#addRunButton').click(function(){
      var distance = $('#distance').val();
      //Set values to 0 if no value is entered by user
      var hours = parseInt($('#hours').val());
      if (isNaN(hours)){
         hours = 0;
      }
      var minutes = parseInt($('#minutes').val());
      if (isNaN(minutes)){
         minutes = 0;
      }
      var seconds = parseInt($('#seconds').val());
      if (isNaN(seconds)){
         seconds = 0;
      }
      var datetime = $('#datetime').val();
      //Calculate time in minutes
      duration = 60*hours + minutes + seconds/60;
      //Alert error messages for missing values
      if (duration==0){
         alert("Enter a time");
         return;
      }else if (distance==0){
         alert("Enter a distance");
         return;
      }else if(datetime==''){
         alert("Enter a date and time");
         return;
      }
      
      //Submit form with AJAX post method, including the CSRF token
      $.post({
         url: 'addrun',
         data: {
            'distance': distance,
            'duration': duration,
            'datetime': datetime,
            'csrfmiddlewaretoken': csrftoken
            },
         //Update chart once new data is received
         success: function(result){
            updateTimeFrame(timeFrame);
         }
      });
   });
   
   //Function to get runs from server whose dates lie between the lower and upper dates
   $('#getRunsButton').click(function(){
      var lower = $('#lowerDate').val();
      var upper = $('#upperDate').val();
      
      //Submit form with AJAX post method, including the CSRF token
      $.post({
         url: 'getrunsbetween',
         data: {
            'lowerdate': lower,
            'upperdate': upper,
            'csrfmiddlewaretoken': csrftoken
            },
         //Update chart once new data is received
         success: function(result){
            updateChart(result);
         }
      });
   });
   
   //Delete selected runs and update data when user clicks delete button
   $('#deleteRunsButton').click(function(){
      //Array of primay keys of runs to be deleted
      var selected = [];
      //Select each checked checkbox
      $('#runList tr td input:checked').each(function(){
         selected.push($(this).val());
      });
      
       $.post({
         url: 'deleteruns',
         data: {
            'delete-run': selected,
            'csrfmiddlewaretoken': csrftoken
            },
         //Update chart with new data
         success: function(result){
            updateTimeFrame(timeFrame);
         }
      });
   });
   
   //Function to get data from specified time frame using AJAX
   function updateTimeFrame(timeFrame){
      $.post({
         url: 'getrunssince',
         data: {
            'timeFrame': timeFrame,
            'csrfmiddlewaretoken': csrftoken
            },
            //Server responds with JSON of run data
         dataType: 'json',
         //Update chart with new data
         success: function(result){
            updateChart(result);
         }
      });
   }
   
   //Function to update the runData and then the chart
   function updateChart(data){
      //Destroy the old chart first
      chart.destroy();
      //Update the run data
      runData = data;
      var yVariable = $('#y-variable').val();
      drawChart(yVariable);
      //Create a new table of runs
      updateRunList();
   }
   
   //Function to create HTML table of runs, with checboxes
   function updateRunList(){
      var htmlString;
      for (var i=0; i < runData.length; i++){
         var date = new Date(runData[i].fields.date);
         //Remove the seconds at end of time string
         var dateString = date.toLocaleString("en-GB").slice(0,-3);
         htmlString += '<tr><td>' + dateString + '</td>'
         + '<td><input name="delete-run" type="checkbox" value=' + runData[i].pk + '></input></td></tr>'
      }
      //Add HTML to the runlist
      $('#runList').html(htmlString);
   }
   
   //Function to draw the chart of the specified variable
   function drawChart(yVariable){
      //Initialise x- and y-data arrays
      var yData = [];
      var dateData = [];
      //Populate y-data with the chosen y-variable
      for (var i=0; i < runData.length; i++){
         //Get all fields and their values from the i-th run
         var fields = runData[i].fields;
         var distance = fields.distance;
         var duration = fields.duration;
         if (yVariable == "pace"){
            var label= "Pace (min/km)";
            //Calculate pace in min km^-1 to 2 d.p.
            var val = Math.round((100*duration)/distance)/100;
         } else if (yVariable == "speed"){
            var label = "Speed (km/h)";
            //Calculate speed in km h^-1 to 2 d.p.
            var val = Math.round((60*100*distance)/duration)/100;
         } else if (yVariable == 'distance'){
            var label = "Distance (km)";
            //Round distance to 2 d.p.
            var val = Math.round(100*fields.distance)/100;
         }else if (yVariable == 'time'){
            var label = "Time (min)";
            //Round time to 2 d.p.
            var val = Math.round(100*fields.duration)/100;
         }else if (yVariable == 'calories'){
            var label = "Calories Burnt (kcal)";
            //Round calories to 2 d.p.
            var val = Math.round(100*fields.calories)/100;
         }
         //Push x and y values
         yData.push(val);
         dateData.push(fields.date);
      };
      //Calculate total of yData
      var total = yData.reduce((a,b) => a + b, 0);
      //Update summary statistics underneath the chart
      $('#total').html("Total: " + Math.round(100*total)/100);
      $('#average').html("Average: " + Math.round(100*total/runData.length)/100);
      $('#max').html("Max: " + Math.max(...yData));
      $('#min').html("Min: " + Math.min(...yData));
      var ctx = $('#chart');
      //Create new line chart object with our coordinates
      chart = new Chart(ctx, {
         type: 'line',
         data: {
            labels: dateData,       //x-data
            datasets: [{
               label: label,    //Label at top of chart
               fill: true,          //Gives colour underneath line
               data: yData,         //y-data
               pointHitRadius: 10,  //Radius for mouse-over tooltip to activate
               borderColor: 'rgba(75,100,192,0.8)',
               backgroundColor: 'rgba(60,200,200,0.3)'
            }]
         },
         options: {
            responsive: false,
            scales: {
               xAxes :[{
                  type: 'time',
                  time: {
                     unit: 'month',    //Label x-axis at each month
                     min: dateData[0], //Start x-axis at our first date
                     tooltipFormat: 'DD/MM/YYYY    h:mm A'  //Format to display datetime in on the tooltip
                  }
               }]
            }
         }
      });
   };
});
