//
// js/home.js
//

$(document).ready(function() {
    
    getMotoMarca();
    getBrasilEstados();   

    let [marcaId, modeloId, estadoId] = [0, 0, 0];

    $('#id_select_moto_marca').on('change', function() {        
        marcaId = this.value;

        if (marcaId) {
            getMotoModelo(marcaId); 
        }           
        else {
            $('#id_select_moto_modelo').prop('disabled', true); 
            $('#id_select_moto_modelo').empty();
            $('#id_select_moto_modelo').append('<option value="" id="id_option_moto_modelo_empty">Selecione o Modelo</option>');            
        }
    });  

    $('#id_select_moto_modelo').on('change', function() {        
        modeloId = this.value;

        if (marcaId && modeloId) {
            getMotoModeloVersao(marcaId, modeloId); 
        }           
        else {
            $('#id_select_moto_versao').prop('disabled', true); 
            $('#id_select_moto_versao').empty();
            $('#id_select_moto_versao').append('<option value="" id="id_option_moto_modelo_versao_empty">Selecione a Versão</option>');            
        }
    });  
    
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

    $('#id_owl_carousel_top_ofertas').owlCarousel({        
        loop:true,
        responsiveClass:true,
        margin:10,
        nav:true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:5
            }
        }
    });

    $('#id_owl_carousel_noticias').owlCarousel({        
        loop:false,
        margin:10,
        items:1,
        nav: true,
        autoWidth:true,
        responsiveClass:true
    });

});