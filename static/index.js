function renderMainChart() {
  selection = $("input[name=chartType]:checked").val()
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
        label: "Most Retweets",
        data: retweetCounts
      }]
    }
  });
}

function renderLikesChart() {

}

$(document).ready(function() {
  //load the page
  $("[name=chartType]").val(["retweets"]);
  renderMainChart();

  //bind event listeners
  $("[name=chartType]").change(function() {
    renderMainChart();
  });
});
