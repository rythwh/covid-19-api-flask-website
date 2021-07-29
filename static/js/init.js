$(document).ready(function () {
  console.log("Ryan White 0967628")

  $("#login-button").click(function () {
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/login",
      data: JSON.stringify({username: $("#username-input-field").val(), password: $("#password-input-field").val()}),
      dataType: "json"
    });
  });

  $("#logout-button").click(function () {
    $.ajax({
      type: "POST",
      contentType: "application/html; charset=utf-8",
      url: "/logout"
    });
  });

  $("#update-data-button").click(function () {
    $.ajax({
      type: "GET",
      contentType: "application/json; charset=utf-8",
      url: "/data/" + $("#region-dropdown option:selected").val() + "," + $("#region-dropdown option:selected").text(),
      success: function(response) {
        location.reload();
      }
    });
  });
});

function selectRegion(region) {
  $("div.region-selection select").val(region).change();
}

var caseChart = null;

function updateChart(labels, changeCases, totalCases) {

  if (caseChart != null) {
    caseChart.destroy();
  }

  var labels = JSON.parse(labels);

  var data = {
    labels: labels,
    datasets: [
      {
        label: "New Cases",
        data: JSON.parse(changeCases),
        backgroundColor: "#EEE",
        borderColor: "#D6D6D6",
        borderWidth: 2,
        pointRadius: 0.1,
        pointHoverRadius: 1
      },{
        label: "Total Cases",
        data: JSON.parse(totalCases),
        backgroundColor: "#EEE",
        borderColor: "#D6D6D6",
        borderWidth: 2,
        pointRadius: 0.1,
        pointHoverRadius: 1,
        hidden: true
      },
    ]
  };

  var options = {
    maintainAspectRatio: false,
    scales: {
      yAxes: [{
        stacked: true,
        gridLines: {
          display: true,
          color: "#D6D6D6"
        },
        ticks: {
          beginAtZero: true
        }
      }],
      xAxes: [{
        gridLines: {
          display: false
        }
      }]
    },
    tooltips: {
      intersect: false
    }
  };

  var ctx = document.getElementById("chart").getContext("2d");
  
  caseChart = new Chart(ctx, {
    type: "line",
    data: data,
    options: options
  });
}