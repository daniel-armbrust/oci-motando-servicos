//
// js/cadastro-particular.js
//

$(document).ready(function() {        

    $('#id_select_brasil_estado').empty();
    $('#id_select_brasil_cidade').empty();

    getBrasilEstados();   

    $('#id_select_brasil_cidade').append('<option value="" id="id_option_brasil_cidade_empty">Selecione a Cidade</option>');            

    let estadoId = 0;   
    
    $('#id_select_brasil_estado').on('change', function() {  
        estadoId = this.value;
        
        if (estadoId) {
            getBrasilCidade(estadoId); 
        }           
        else {
            $('#id_select_brasil_cidade').prop('disabled', true); 
            $('#id_select_brasil_cidade').empty();
            $('#id_select_brasil_cidade').append('<option value="" id="id_option_brasil_cidade_empty">Selecione a Cidade</option>');            
        }
    });      

    $("#id_cadastro_particular_form").submit(function() {         
        submitCadastroParticular();                  
    });
});

function submitCadastroParticular() {
   
    let formHasErrors = false;

    const formIdFields = {
        'id_select_brasil_estado': /[0-9]+$/,
        'id_select_brasil_cidade': /[0-9]+$/,
        'id_input_nome': /[A-Za-z ]{10,}$/,
        'id_input_email': /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i,
        'id_input_email_confirm': /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i,
        'id_input_telefone': /(?=.{8,})/,
        'id_input_senha': /(?=.{8,})/,
        'id_input_senha_confirm': /(?=.{8,})/
    };

    let fieldValues = {
        'brasil_estado': '', 
        'brasil_cidade': '', 
        'nome': '', 
        'email': '', 
        'email_confirm': '', 
        'telefone': '', 
        'senha': '', 
        'senha_confirm': ''
    };

    $.blockUI({ 
        message: '<h2>Por favor aguarde ...</h2>',
        overlayCSS: { backgroundColor: '#dee2e6' } 
    });     

    let [fieldId, value, regexp] = ['', '', ''];
   
    for (fieldId in formIdFields) {
        $(`#${fieldId}`).attr('readonly', true);

        regexp = formIdFields[fieldId];        
        value = $(`#${fieldId}`).val();

        if (regexp.test(value)) {
            
            $(`#${fieldId}`).addClass('is-valid');

            if (fieldId === 'id_input_telefone')
               value = value.replace(/[()\-\ ]/g, '') 

            fieldValues[$(`#${fieldId}`).attr('name')] = value;
        }       
        else {
            
            $(`#${fieldId}`).addClass('is-invalid');
            
            formHasErrors = true;
        } 
    }
   
    if (formHasErrors) {             

        $.unblockUI();

        for (fieldId in formIdFields) {
            $(`#${fieldId}`).attr('readonly', false);
        }

        $('#id_modal_message').text('Erro ao realizar o cadastro! Por favor, corrija os erros do formulário.');
        $('#id_modal').modal('show');
        $('#id_senha').val('');           

        return false;   
    }   
    else {
       return true;
    }
}