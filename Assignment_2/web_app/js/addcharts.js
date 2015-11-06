var updateChart = function(data){
	console.log("update chart");
	console.log(data);
	$('.foodPieChart').remove(); // this is my <canvas> element
  	$('#pie-chart-holder').append("<canvas id= 'foodPieChart' width='300' height='300' style='text-align:center;'></canvas>");
	var ctx = document.getElementById("foodPieChart").getContext("2d");
	var myPieChart = new Chart(ctx).Pie(data);
}
var addChart = function(data){
	console.log("new chart");
	var ctx = document.getElementById("foodPieChart").getContext("2d");
	var myPieChart = new Chart(ctx).Pie(data);
}

var updateSubheading = function(){
	document.getElementById("data-placeholder").innerHTML = "<br><br><h2>Here's what she ate:</h2>\
                    <div class='pie-chart-holder'>\
                        <canvas id= 'foodPieChart' width='300' height='300' style='text-align:center;'></canvas>\
                    </div>";
}

var test_data = [
    {
        value: 300,
        color:"#F7464A",
        highlight: "#FF5A5E",
        label: "Red"
    },
    {
        value: 50,
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Green"
    },
    {
        value: 100,
        color: "#FDB45C",
        highlight: "#FFC870",
        label: "Yellow"
    }
];

var dataURL = "/get_data";

var InfiniteAjaxRequest = function (uri) {
    $.ajax({
        url: uri,
        success: function(data) {
            // do something with "data"
            updateChart(data);
            InfiniteAjaxRequest (uri);
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert(thrownError);
        }
    });
};

document.getElementById('data-form').addEventListener('submit', function (e) {
	e.preventDefault();
    updateSubheading();
    //addChart(test_data);
    updateChart(test_data);
    InfiniteAjaxRequest (dataURL);
}, false);