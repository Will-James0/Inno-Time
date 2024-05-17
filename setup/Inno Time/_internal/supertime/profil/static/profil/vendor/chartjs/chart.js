// Graphe camembert

const ctxPie = document.getElementById("pie-chart").getContext("2d");

const pieChart = new Chart(ctxPie, {
  type: "pie",
  data: {
    labels: ["Présences", "Absences"],
    datasets: [{
      data: [90, 10],
      backgroundColor: ["#007bff", "#dc3545"],
      borderWidth: 1
    }]
  }
});

// Graphe linéaire

const ctxLine = document.getElementById("line-chart").getContext("2d");

const lineChart = new Chart(ctxLine, {
  type: "line",
  data: {
    labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
    datasets: [{
      label: "Taux de présence",
      data: [80, 85, 90, 95, 90, 85, 80, 85, 90, 95, 90, 85], // Sample presence data
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      borderColor: "rgba(75, 192, 192, 1)",
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          max: 100 // Set the maximum value for the y-axis (presence percentage)
        }
      }]
    }
  }
});


const ctxLine2 = document.getElementById("line2-chart-2").getContext("2d");

const lineChart2 = new Chart(ctxLine2, {
  type: "line2",
  data: {
    labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
    datasets: [{
      label: "Taux de présence",
      data: [80, 85, 90, 95, 90, 85, 80, 85, 90, 95, 90, 85], // Sample presence data
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      borderColor: "rgba(75, 192, 192, 1)",
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          max: 100 // Set the maximum value for the y-axis (presence percentage)
        }
      }]
    }
  }
});

