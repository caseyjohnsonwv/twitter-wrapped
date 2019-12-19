function renderMainChart(selection) {
  selection == "retweets" ? renderRetweetChart() : renderLikesChart();
}

function renderRetweetChart() {
  let ctx = $("#mainChart");
  let retweetCounts = [];
  for (var i = 0; i < data.mostRts.length; i++) {
    retweetCounts.push(parseInt(data.mostRts[i].retweet_count));
  }
  var mainChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: retweetCounts,
      datasets: [{
        data: retweetCounts,
        backgroundColor: "#1dcaff"
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Most Retweets of " + new Date().getFullYear(),
        fontSize: 20
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
            fontSize: 14
          }
        }],
        xAxes: [{
          ticks: {
            fontSize: 14
          }
        }]
      },
      responsive: true,
      maintainAspectRatio: false,
      hover: {mode: null},
      tooltips: {enabled: false}
    }
  });
}

function renderLikesChart() {
  //copy over from retweets chart later
}

function toggleTweetCards(selection) {
  if (selection == "retweets") {
    $("#mostLikes-cards").addClass("hide");
    $("#mostRts-cards").removeClass("hide");
  }
  else {
    $("#mostRts-cards").addClass("hide");
    $("#mostLikes-cards").removeClass("hide");
  }
}

$(document).ready(function() {
  //load the page
  renderMainChart("retweets");
  toggleTweetCards("retweets");

  //bind event listeners
  $("#select-retweets-chart").click(function(e) {
    renderMainChart("retweets");
    toggleTweetCards("retweets");
    e.preventDefault();
  });
  $("#select-likes-chart").click(function(e) {
    renderMainChart("likes");
    toggleTweetCards("likes");
    e.preventDefault();
  });
});
