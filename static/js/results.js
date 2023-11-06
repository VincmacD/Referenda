var vote_results = {{ vote_results|safe|safe }};

google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  
    vote_results.unshift(["Choice", "Vote Count"]);
    var data = google.visualization.arrayToDataTable(vote_results);

    var options = {
        width: 550,
        height: 300,
        colors: ['#90ff94','#ff5c5c'],
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
    google.visualization.events.addListener(chart, 'ready', function () {
        var svg = document.getElementById('piechart').getElementsByTagName('svg')[0];
        var textElements = svg.getElementsByTagName('text');

        for (var i = 0; i < textElements.length; i++) {
            if (textElements[i].textContent.includes('%')) {
                textElements[i].classList.add('pie-chart-text');
            }
        }
    });
    chart.draw(data, options);
}