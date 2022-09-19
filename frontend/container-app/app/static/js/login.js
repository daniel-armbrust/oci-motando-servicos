//
// js/login.js
//

$(document).ready(function() {
    $("#id_login_form").submit(function(e) {         
         submitLogin();                  
    });
});

function submitLogin() {

    let formHasErrors = false;

    const formIdFields = {
        'id_email': /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i,
        'id_senha': /(?=.{8,})/
    };

    let fieldValues = {
        'email': '', 
        'senha': ''
    }

    $('#id_email').attr('readonly', true);
    $('#id_senha').attr('readonly', true);

    $.blockUI({ 
        message: '<h2>Por favor aguarde ...</h2>',
        overlayCSS: { backgroundColor: '#dee2e6' } 
    });       

    let [fieldId, value, regexp] = ['', '', ''];
    
    for (fieldId in formIdFields) {
        regexp = formIdFields[fieldId];
        value = $(`#${fieldId}`).val();

        if (regexp.test(value)) {            
            fieldValues[$(`#${fieldId}`).attr('name')] = value;
        }       
        else {                        
            formHasErrors = true;
        } 
    }

    if (formHasErrors) { 
                        
        $.unblockUI();

        $('#id_email').attr('readonly', false);
        $('#id_senha').attr('readonly', false);

        $('#id_modal_message').text('E-mail ou senha inválido(s)!');
        $('#id_modal').modal('show');
        $('#id_senha').val('');              

        return false;
    }
    else {
        return true;
    }    
}