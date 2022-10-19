//
// js/anuncio.js
//

function confirmDelAnuncioImg(imgFilename, jfilerIndex) {
    const result = window.confirm('Tem certeza que deseja remover essa imagem do anúncio?');

    if (result) {
        delAnuncioImg(imgFilename);                 

        const divId = `id_jfiler_item_${jfilerIndex}`;

        $(`#${divId}`).remove();
    }                   
}

function addAnuncioImg(imgFilename) {
    const strImgList = $('#id_img_lista').val();

    if (strImgList)
        // converte a string para um vetor.
        ANUNCIO_IMG_LIST = strImgList.replace(/\'|\[|\]/g, '').split(',');
    
    ANUNCIO_IMG_LIST.push(imgFilename);

    $('#id_img_lista').val(ANUNCIO_IMG_LIST);
}

function delAnuncioImg(imgFilename) {
    const strImgList = $('#id_img_lista').val();                

    if (strImgList) {
       // converte a string para um vetor.
       ANUNCIO_IMG_LIST = strImgList.replace(/\'|\[|\]/g, '').split(',');   

       ANUNCIO_IMG_LIST = ANUNCIO_IMG_LIST.map(s => s.trim());
    
       const removeImgIndex = ANUNCIO_IMG_LIST.indexOf(imgFilename);

       console.log(removeImgIndex);
    
       if (removeImgIndex >= 0) {
          ANUNCIO_IMG_LIST.splice(removeImgIndex, 1);                      
          $('#id_img_lista').val(ANUNCIO_IMG_LIST);
       }
    }
}               

$(document).ready(function() {       

    $('#id_preco').maskMoney({symbol:'R$ ', thousands:'.', decimal:',', symbolStay: true});

    $('#id_select_moto_marca').empty();
    $('#id_select_moto_marca').append('<option value="">Selecione a Marca</option>'); 

    $('#id_select_moto_modelo').empty();
    $('#id_select_moto_modelo').append('<option value="">Selecione o Modelo</option>');                
    
    $('#id_select_moto_marca').on('change', function() {        
        let marcaId = this.value;

        if (marcaId) {
            getMotoModelo(marcaId); 
        }           
        else {
            $('#id_select_moto_modelo').prop('disabled', true); 
            $('#id_select_moto_modelo').empty();
            $('#id_select_moto_modelo').append('<option value="">Selecione o Modelo</option>');            
        }
    });  

    $('#id_zero_km').click(function() {
          let zeroKm = $('#id_zero_km').prop('checked');

          if (zeroKm) {
             $('#id_km').prop('readonly', true)
             $('#id_km').val(0);
          }                   
          else {
             $('#id_km').prop('readonly', false)
             $('#id_km').val('');
          }                   
    });    

    const preco = parseFloat($('#id_preco').val());

    if (preco) {
       const brPreco = preco.toLocaleString('pt-br', {style: 'currency', currency: 'BRL'});
       $('#id_preco').val(brPreco);
    }       

    $('#id_anuncio_form').submit(function(e) {         

        const anuncioImgList = $('#id_img_lista').val();        

        if (anuncioImgList.length <= 0) {
            alert('Seu anúncio necessita de imagen(s) para ser publicado!');
            e.preventDefault();
        }
        else {
            submitAnuncio();                  
        }
    });

    function submitAnuncio() {
        let formHasErrors = false;        

        $.blockUI({ 
            message: '<h2>Por favor aguarde ...</h2>',
            overlayCSS: { backgroundColor: '#dee2e6' } 
        });  

        return true;              
    }    
});