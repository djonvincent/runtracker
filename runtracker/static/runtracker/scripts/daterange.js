$(document).ready(function(){
   var csrftoken = $("[name=csrfmiddlewaretoken]").val();
   
   $("#customRangeBox").change(function(){
      var checked = $(this).prop('checked');
      $('#upperDate, #lowerDate, #getRunsButton').prop('disabled', !checked);
      $('#timeFrameOption').prop('disabled', checked);
   });
   
   $('#timeFrameOption').change(function(){
      var timeFrame = $(this).val();
      $.post({
         url: 'getrunssince',
         data: {
            'timeFrame': timeFrame,
            'csrfmiddlewaretoken': csrftoken
            },
         dataType: 'json',
         success: function(result){
            runData = result;
            var yVariable = $('#y-variable').val()
            drawChart(yVariable);
         }
      }); 
   });
});
