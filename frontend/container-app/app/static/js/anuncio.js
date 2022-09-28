//
// js/anuncio.js
//

$(document).ready(function() {       

    $('#id_select_moto_marca').empty();
    $('#id_select_moto_marca').append('<option value="">Selecione a Marca</option>'); 

    $('#id_select_moto_modelo').empty();
    $('#id_select_moto_modelo').append('<option value="">Selecione o Modelo</option>');            

    getMotoMarca();
    
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

    let filesUploaded = new Array();

    $('#filer_input').filer({
        limit: 10,
        maxSize: 5242880,
        extensions: ['jpg', 'jpeg', 'png', 'webp'],       
        changeInput: '<div class="jFiler-input-dragDrop hold-photos"><div class="jFiler-input-inner"><div class="jFiler-input-icon"><i class="icon-jfi-cloud-up-o"></i></div><div class="jFiler-input-text"><h3>Arraste at&eacute; 10 fotos da sua Moto</h3> <p>somente arquivos (jpg, png, webp)</p></div><a class="jFiler-input-choose-btn blue">Selecione as imagens</a></div></div>',
        showThumbs: true,
        theme: 'dragdropbox',
        templates: {
            box: '<ul class="jFiler-items-list jFiler-items-grid"></ul>',
            item: '<li class="jFiler-item">\
                        <div class="jFiler-item-container">\
                            <div class="jFiler-item-inner">\
                                <div class="jFiler-item-thumb">\
                                    <div class="jFiler-item-status"></div>\
                                    <div class="jFiler-item-thumb-overlay">\
                                        <div class="jFiler-item-info">\
                                            <div style="display:table-cell;vertical-align: middle;">\
                                                <span class="jFiler-item-title"><b title="{{fi-name}}">{{fi-name}}</b></span>\
                                                <span class="jFiler-item-others">{{fi-size2}}</span>\
                                            </div>\
                                        </div>\
                                    </div>\
                                    {{fi-image}}\
                                </div>\
                                <div class="jFiler-item-assets jFiler-row">\
                                    <ul class="list-inline pull-left">\
                                        <li>{{fi-progressBar}}</li>\
                                    </ul>\
                                    <ul class="list-inline pull-right">\
                                        <li><a class="icon-jfi-trash jFiler-item-trash-action"></a></li>\
                                    </ul>\
                                </div>\
                            </div>\
                        </div>\
                    </li>',
            itemAppend: '<li class="jFiler-item">\
                            <div class="jFiler-item-container">\
                                <div class="jFiler-item-inner">\
                                    <div class="jFiler-item-thumb">\
                                        <div class="jFiler-item-status"></div>\
                                        <div class="jFiler-item-thumb-overlay">\
                                            <div class="jFiler-item-info">\
                                                <div style="display:table-cell;vertical-align: middle;">\
                                                    <span class="jFiler-item-title"><b title="{{fi-name}}">{{fi-name}}</b></span>\
                                                    <span class="jFiler-item-others">{{fi-size2}}</span>\
                                                </div>\
                                            </div>\
                                        </div>\
                                        {{fi-image}}\
                                    </div>\
                                    <div class="jFiler-item-assets jFiler-row">\
                                        <ul class="list-inline pull-left">\
                                            <li><span class="jFiler-item-others">{{fi-icon}}</span></li>\
                                        </ul>\
                                        <ul class="list-inline pull-right">\
                                            <li><a class="icon-jfi-trash jFiler-item-trash-action"></a></li>\
                                        </ul>\
                                    </div>\
                                </div>\
                            </div>\
                        </li>',
            progressBar: '<div class="bar"></div>',
        itemAppendToEnd: false,
        canvasImage: true,
        removeConfirmation: true,
        _selectors: {
                list: '.jFiler-items-list',
                item: '.jFiler-item',
                progressBar: '.bar',
                remove: '.jFiler-item-trash-action'
            }
        },
        dragDrop: {
            dragEnter: null,
            dragLeave: null,
            drop: null,
            dragContainer: null,
        },
        uploadFile: {
            url: imgUploadUrl,
            data: null,
            type: 'POST',
            enctype: 'multipart/form-data',
            synchron: true,
            beforeSend: function(){},
                success: function(data, itemEl, listEl, boxEl, newInputEl, inputEl, id) {                    
                    filesUploaded.push(data);                
                    $('#id_img_lista').val(JSON.stringify(filesUploaded));
            },
            error: function(el){
                let parent = el.find('.jFiler-jProgressBar').parent();
                
                el.find('.jFiler-jProgressBar').fadeOut('slow', function(){
                    $("<div class=\"jFiler-item-others text-error\"><i class=\"icon-jfi-minus-circle\"></i> Erro</div>").hide().appendTo(parent).fadeIn('slow');
                });
            },
            statusCode: null,
            onProgress: null,
            onComplete: null
        },
        files: null,
        addMore: false,
        allowDuplicates: true,
        clipBoardPaste: true,
        excludeName: null,
        beforeRender: null,
        afterRender: null,
        beforeShow: null,
        beforeSelect: null,
        onSelect: null,
        afterShow: null,
        onRemove: function(itemEl, file, id, listEl, boxEl, newInputEl, inputEl) {
            let filerKit = inputEl.prop("jFiler"); //,
            //file_name = filerKit.files_list[id].name;
            let filename = filerKit.files_list[id].file.name;             

            $.ajax({
                url: imgUploadUrl,
                type: 'DELETE',
                data: {'filename': filename}
            });
        },
        onEmpty: null,
        options: null,
        dialogs: {
            alert: function(text) {
                return alert(text);
            },
            confirm: function (text, callback) {
                confirm(text) ? callback() : null;
            }
        },
        captions: {
            button: 'Escolha o arquivo',
            feedback: 'Escolha arquivos para upload',
            feedback2: 'Arquivos escolhidos',
            drop: 'Arraste aqui seus arquivos (jpg, png, webp)',
            removeConfirmation: 'Tem certeza de que deseja remover este arquivo?',
            errors: {
                filesLimit: 'Somente {{fi-limit}} arquivos s&atilde;o permitidos de serem enviados.',
                filesType: 'Somente imagens s&atilde;o permitidos de serem enviados.',
                filesSize: '{{fi-name}} &eacute; muito grande! Fa&ccedil;a o upload de arquivos de at&eacute; {{fi-maxSize}} MB.',
                filesSizeAll: 'Arquivos muito grandes! Fa&ccedil;a o upload de arquivos de at&eacute; {{fi-maxSize}} MB.'
            }                
        }
    });

    $('#id_cadastro_anuncio_form').submit(function() {         
        submitAnuncio();                  
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