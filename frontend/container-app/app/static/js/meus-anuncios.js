//
// js/meus-anuncios.js
//

$(document).ready(function() {
     getMeusAnuncios();
});

function getMeusAnuncios() {

    return $.ajax({
        url: anuncioUrl,
        type: 'GET', 
        dataType: 'json', 
        beforeSend: function() {
        },
        success: function(jsonResp) {
            console.log(jsonResp)
        },
        error: function(xhr, textStatus, errorThrown) {
            console.error(textStatus);
        }

    });
}