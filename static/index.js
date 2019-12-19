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
  let ctx = $("#mainChart");
  let likeCounts = [];
  for (var i = 0; i < data.mostLikes.length; i++) {
    likeCounts.push(parseInt(data.mostLikes[i].favorite_count));
  }
  var mainChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: likeCounts,
      datasets: [{
        data: likeCounts,
        backgroundColor: "#1dcaff"
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Most Likes of " + new Date().getFullYear(),
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

function toggleTweetCards(selection) {
  if (selection == "retweets") {
    $("#mostLikes-cards").fadeOut(500).addClass("hide");
    $("#mostRts-cards").fadeIn(500).removeClass("hide");
  }
  else {
    $("#mostRts-cards").fadeOut(500).addClass("hide");
    $("#mostLikes-cards").fadeIn(500).removeClass("hide");
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
