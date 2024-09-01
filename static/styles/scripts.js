$(document).ready(function () {
    // Behandlung des Text-Prompt-Formulars
    $('#promptForm').on('submit', function (e) {
        e.preventDefault();  // Verhindert das Standard-Formularverhalten

        var prompt = $('#prompt').val();  // Erfasst den Wert aus dem 'prompt'-Feld

        // Debugging: Überprüfe, ob der prompt korrekt erfasst wurde
        console.log('Prompt eingegeben:', prompt);

        // Überprüfe, ob das 'prompt'-Feld leer ist
        if (!prompt) {
            alert('Bitte geben Sie einen Prompt ein.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/generate_code',
            data: { prompt: prompt },  // Sendet den 'prompt'-Wert an den Server
            success: function (response) {
                console.log('Server-Antwort:', response);  // Debugging: Zeigt die Serverantwort in der Konsole an

                if (response.code) {
                    $('#response').val(response.code);  // Zeigt die generierte Antwort im 'response'-Feld an
                } else {
                    alert('Fehler bei der Codegenerierung.');
                }
            },
            error: function (xhr, status, error) {
                console.error('Fehler bei der Codegenerierung:', status, error);  // Debugging: Zeigt Fehlerdetails in der Konsole an
                alert('Fehler bei der Codegenerierung: ' + xhr.responseText);
            }
        });

        // Optional: Leert das 'prompt'-Feld nach der Anfrage
        $('#prompt').val('');
    });

    // Kopieren der Antwort in die Zwischenablage
    $('#copyButton').on('click', function () {
        var responseText = $('#response');
        responseText.select();
        document.execCommand('copy');
        alert('Antwort wurde in die Zwischenablage kopiert!');
    });

    // Behandlung des Bildgenerierungs-Formulars
    $('#imageForm').on('submit', function (e) {
        e.preventDefault();  // Verhindert das Standard-Formularverhalten

        var prompt = $('#imagePrompt').val();  // Erfasst den Wert aus dem 'imagePrompt'-Feld

        // Debugging: Überprüfe, ob der Bild-Prompt korrekt erfasst wurde
        console.log('Bild-Prompt eingegeben:', prompt);

        if (!prompt) {
            alert('Bitte geben Sie einen Bild-Prompt ein.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/generate_image',
            data: { prompt: prompt },  // Sendet den 'prompt'-Wert für das Bild an den Server
            success: function (response) {
                console.log('Server-Antwort für Bild:', response);  // Debugging: Zeigt die Serverantwort in der Konsole an

                if (response.image_url) {
                    $('#generatedImage').attr('src', response.image_url).show();
                    $('#downloadImageButton')
                        .attr('href', response.image_url)
                        .attr('download', response.image_url.split('/').pop())
                        .show();
                } else {
                    alert('Fehler bei der Bildgenerierung.');
                }
            },
            error: function (xhr, status, error) {
                console.error('Fehler bei der Bildgenerierung:', status, error);  // Debugging: Zeigt Fehlerdetails in der Konsole an
                alert('Fehler bei der Bildgenerierung: ' + xhr.responseText);
            }
        });

        // Optional: Leert das 'imagePrompt'-Feld nach der Anfrage
        $('#imagePrompt').val('');
    });
});
