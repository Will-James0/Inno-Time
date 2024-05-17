$(document).ready(function() {
    $('#calendar').fullCalendar({
      defaultView: 'dayGridMonth', // Afficher le mois par défaut
      initialDate: moment(), // Définir la date initiale sur aujourd'hui
      dayRender: function(dayRenderInfo) {
        // Mettre en évidence la date du jour
        if (moment().isSame(dayRenderInfo.date, 'day')) {
          dayRenderInfo.el.style.backgroundColor = 'lightblue';
        }
      }
    });
  });