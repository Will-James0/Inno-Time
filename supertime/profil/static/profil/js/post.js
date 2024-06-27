document.addEventListener('DOMContentLoaded', function() {
    var posteSelect = document.getElementById('poste');
    var salaryInput = document.querySelector('input[name="salary"]');

    posteSelect.addEventListener('change', function() {
        var selectedPosteId = this.value;
        if (selectedPosteId) {
            // Envoyer une requête AJAX pour récupérer la valeur de somme associée à ce poste
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Mettre à jour la valeur du champ salaire avec la valeur récupérée
                        var response = JSON.parse(xhr.responseText);
                        salaryInput.value = response.somme;
                    } else {
                        console.error('Une erreur s\'est produite');
                    }
                }
            };
            xhr.open('GET', '{% url "profil:get_somme_for_poste" %}?poste_id=' + selectedPosteId, true);
            xhr.send();
        } else {
            salaryInput.value = ''; // Effacer la valeur si aucun poste n'est sélectionné
        }
    });
});