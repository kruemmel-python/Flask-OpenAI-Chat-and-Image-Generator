$(document).ready(function () {
    $('#promptForm').on('submit', function (e) {
        e.preventDefault();
        var prompt = $('#prompt').val();
        $.ajax({
            type: 'POST',
            url: '/generate_code',
            data: { prompt: prompt },
            success: function (response) {
                $('#response').val(response.code);
            }
        });
    });

    $('#copyButton').on('click', function () {
        var responseText = $('#response');
        responseText.select();
        document.execCommand('copy');
        alert('Antwort wurde in die Zwischenablage kopiert!');
    });

    $('#imageForm').on('submit', function (e) {
        e.preventDefault();
        var prompt = $('#imagePrompt').val();
        $.ajax({
            type: 'POST',
            url: '/generate_image',
            data: { prompt: prompt },
            success: function (response) {
                if (response.image_url) {
                    $('#generatedImage').attr('src', response.image_url).show();
                    $('#downloadImageButton').attr('href', response.image_url).show();
                } else {
                    alert('Fehler bei der Bildgenerierung.');
                }
            },
            error: function () {
                alert('Fehler bei der Bildgenerierung.');
            }
        });
    });
});
