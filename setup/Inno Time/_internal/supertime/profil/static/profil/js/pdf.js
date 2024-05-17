document.getElementById('generate-pdf-button').addEventListener('click', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/generate_pdf/', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Télécharger le fichier PDF généré
            var blob = new Blob([xhr.response], { type: 'application/pdf' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'fiche_de_paie.pdf';
            a.click();
            window.URL.revokeObjectURL(url);
        }
    };
    xhr.responseType = 'arraybuffer';
    xhr.send();
});
