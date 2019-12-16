function renderMainChart() {
  selection = $("input[name=chartType]:checked").val()
  selection == "retweets" ? renderRetweetChart() : renderLikesChart();
}

function renderRetweetChart() {
  let ctx = $("#mainChart");
  let retweetCounts = [];
  let dates = [];
  let full_texts = [];
  for (var i = 0; i < data.mostRts.length; i++) {
    retweetCounts.push(parseInt(data.mostRts[i].retweet_count));
    dates.push(data.mostRts[i].created_at.slice(5, 17));
    full_texts.push(data.mostRts[i].full_text);
  }
  var mainChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: dates,
      datasets: [{
        label: "Most Retweets",
        data: retweetCounts,
        backgroundColor: "#1dcaff"
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: 'Most retweeted tweets of the year.'
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
            fontSize: 20
          }
        }],
        xAxes: [{
          ticks: {
            fontSize: 14
          }
        }]
      },
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

function renderLikesChart() {
  //copy over from retweets chart later
}

$(document).ready(function() {
  //load the page
  $("[name=chartType]").val(["retweets"]);
  renderMainChart();

  //bind event listeners
  $("[name=chartType]").change(function(e) {
    e.preventDefault();
    renderMainChart();
  });
});
