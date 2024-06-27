// setTimeout(function() {
//     location.reload();
// }, 10000);

// $(document).ready(function() {
//     // Fonction pour recharger le contenu du statut
//     function reloadStatut() {
//       $('.list_t').each(function() {
//         var table = $(this);
//         $.ajax({
//           url: "liste ternimal", // URL de votre vue Django
//           type: 'GET',
//           success: function(data) {
//             table.html(data); // Mettre à jour le contenu du <td> avec la nouvelle valeur
//           }
//         });
//       });
//     }
  
//     // Recharger toutes les 10 secondes
//     setInterval(reloadStatut, 5000);
//   });

//2//

// $(document).ready(function() {
//     // Fonction pour recharger le contenu du tableau
//     function reloadTableContent() {
//       var table = $('.list_t');
//       var tableContainer = $('.emp');
//       var homeContent = $('.bx');
//       $.ajax({
//         url: "liste ternimal", // Utilisation de la syntaxe Django pour spécifier l'URL
//         type: 'GET',
//         success: function(data) {
//           var newBodyContent = $(data).not(homeContent);
//           tableContainer.html(newBodyContent); // Mettre à jour le contenu du conteneur de
//         }
//       });
//     }
  
//     // Recharger toutes les 10 secondes
//     setInterval(reloadTableContent, 10000);
//   });

//3//

// $(document).ready(function() {
//     // Fonction pour recharger le contenu du body
//     function reloadBodyContent() {
//       var bodyElement = $('.bod');
//       var homeContent = $('.home-content');
//       var button = $('.bx'); // Remplacez '.your-button' par le sélecteur approprié pour votre bouton
  
//       if (!button.hasClass('bx')) {
//         $.ajax({
//           url: 'liste ternimal', // Utilisation de la syntaxe Django pour spécifier l'URL
//           type: 'GET',
//           success: function(data) {
//             var newBodyContent = $(data).not(homeContent); // Exclure le contenu de home-content de la réponse AJAX
//             bodyElement.html(newBodyContent); // Mettre à jour le contenu du body
//           }
//         });
//       }
//     }
  
//     // Recharger le contenu du body une fois au chargement initial
//     reloadBodyContent();
  
//     // Recharger toutes les 10 secondes
//     setInterval(reloadBodyContent, 10000);
//   });

/*4*/

$(document).ready(function() {
    // Fonction pour recharger le contenu du tableau
    function reloadTableContent() {
        $.ajax({
            url: 'liste ternimal', // URL de votre vue Django pour récupérer les données du tableau
            type: 'GET',
            success: function(data) {
                $('.table-container').html($(data).find('.table-container').html());
            }
        });
    }

    // Recharger le contenu du tableau toutes les 10 secondes
    setInterval(reloadTableContent, 10000);
});
