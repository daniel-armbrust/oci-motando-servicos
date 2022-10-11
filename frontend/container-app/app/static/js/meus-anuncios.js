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

            $('#id_meus_anuncios').html('');
            $('#id_ajax_loading').toggleClass('d-none d-block');

        },
        complete: function () {

            $('#id_ajax_loading').toggleClass('d-block d-none');
            
        },
        success: function(jsonResp) {

            if (jsonResp['status'] === 'success') {             

               let jsonData = jsonResp['data'];

               const totalPublicado = jsonResp['meta'].total_publicado;
               const totalNaoPublicado = jsonResp['meta'].total_nao_publicado;

               for (let i = 0 ; i < jsonData.length ; i++) {
                  let anuncioStatus = '';

                  if (jsonData[i].status === 'publicado')
                     anuncioStatus = `<span class="text-success text-uppercase fw-bolder">${jsonData[i].status}</span>`;
                  else
                     anuncioStatus = `<span class="text-dark text-uppercase fw-bolder">${jsonData[i].status}</span>`;                     

                  $('#id_meus_anuncios').append(`
                      <br>             
                      <div class="card mb-3">
                          <div class="row g-0">
                             <div class="col-md-4">                                
                                <a href="#" class="text-decoration-none">
                                   <img src="${jsonData[i].img_lista[0]}" class="img-fluid rounded pt-4 p-2" 
                                        alt="${jsonData[i].moto_marca} - ${jsonData[i].moto_modelo}">
                                </a>
                             </div>
                             <div class="col-md-8">
                                <div class="card-body">
                                    <a href="#" class="text-decoration-none">
                                       <h5 class="card-title text-uppercase h4">${jsonData[i].moto_marca} - ${jsonData[i].moto_modelo}</h5>
                                    </a>
                                    <p class="card-text pt-3">
                                        <span> <i class="fas fa-tachometer-alt"></i>&nbsp;${jsonData[i].km} Km </span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                        <span> <i class="fas fa-fill-drip"></i>&nbsp;${jsonData[i].cor} </span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                        <span> <i class="far fa-calendar-alt"></i>&nbsp;${jsonData[i].ano_fabricacao} / ${jsonData[i].ano_modelo} </span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                                  
                                    </p>
                                    <p class="card-text"> <span class="text-success h5 fw-bold"> R$ ${jsonData[i].preco} </span>
                                    <div class="row pt-2">
                                        <div class="col">
                                            <button type="button" class="btn btn-outline-success">Destacar Anúncio</button>&nbsp;&nbsp;                                 
                                            <button type="button" class="btn btn-outline-info">Editar</button>&nbsp;&nbsp;                                 
                                            <button type="button" class="btn btn-outline-danger">Excluir</button>
                                        </div>
                                    </div>
                                    <div class="row pt-4">
                                        <div class="col">
                                            Status: ${anuncioStatus} &nbsp;&nbsp;&nbsp;&nbsp;                                                                              
                                            Criado em: <span class="fw-normal"> ${jsonData[i].data_cadastro} </span>
                                        </div>
                                    </div>
                                    <div class="row pt-2">                                    
                                        <div class="col">
                                            Compartilhar: &nbsp;
                                            <a href="#" class="text-decoration-none">
                                               <img src="/static/img/whatapp-icon.png" class="img-fluid" width="5%">
                                            </a> 
                                            &nbsp;
                                            <a href="#" class="text-decoration-none">
                                               <img src="/static/img/facebook-icon.png" class="img-fluid" width="5%">
                                            </a> 
                                            &nbsp;
                                            <a href="#" class="text-decoration-none">
                                               <img src="/static/img/twiter-icon.png" class="img-fluid" width="5%">
                                            </a>
                                            &nbsp;
                                            <a href="#" class="text-decoration-none">
                                               <img src="/static/img/linkedin-icon.png" class="img-fluid" width="5%">
                                            </a>
                                        </div>
                                    </div>                                  
                                </div>
                             </div>
                          </div>
                      </div>`);  
               }         
               
               
            }
            else {
               $('#id_motando_modal').modal('show');
               $('#id_modal_title').text('ERRO');
               $('#id_modal_message').html('Houve um erro ao consultar dados do servidor. <br> Por favor, tente novamente mais tarde...');
            }
        },
        error: function(xhr, textStatus, errorThrown) {    

            $('#id_motando_modal').modal('show');
            $('#id_modal_title').text('ERRO');
            $('#id_modal_message').html('Houve um erro ao consultar dados do servidor. <br> Por favor, tente novamente mais tarde...');

            console.error(textStatus);
        }         
    });
}