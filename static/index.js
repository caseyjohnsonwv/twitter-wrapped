function renderMainChart(selection) {
  selection == "retweets" ? renderRetweetChart() : renderLikesChart();
}

function renderRetweetChart() {
  let ctx = $("#mainChart");
  let retweetCounts = [];
  let dates = [];
  let full_texts = [];
  for (var i = 0; i < data.mostRts.length; i++) {
    retweetCounts.push(parseInt(data.mostRts[i].retweet_count));
    dates.push(data.mostRts[i].created_at);
    full_texts.push(data.mostRts[i].full_text);
  }
  var mainChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: dates,
      datasets: [{
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
            display: false
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
  renderMainChart("retweets");

  //bind event listeners
  $("#select-retweets-chart").click(function(e) {
    e.preventDefault();
    renderMainChart("retweets");
  });
  $("#select-likes-chart").click(function(e) {
    e.preventDefault();
    renderMainChart("likes")
  });
});
