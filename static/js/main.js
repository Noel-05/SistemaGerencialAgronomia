$(document).ready(function(){
  $('.btn-sideBar-SubMenu').on('click', function(){
    var SubMenu=$(this).next('ul');
    var iconBtn=$(this).children('.zmdi-caret-down');
    if(SubMenu.hasClass('show-sideBar-SubMenu')){
      iconBtn.removeClass('zmdi-hc-rotate-180');
      SubMenu.removeClass('show-sideBar-SubMenu');
    }else{
      iconBtn.addClass('zmdi-hc-rotate-180');
      SubMenu.addClass('show-sideBar-SubMenu');
    }
  });
  $('.btn-exit-system').on('click', function(){
    swal({
        title: 'Are you sure?',
        text: "The current session will be closed",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#03A9F4',
        cancelButtonColor: '#F44336',
        confirmButtonText: '<i class="zmdi zmdi-run"></i> Yes, Exit!',
        cancelButtonText: '<i class="zmdi zmdi-close-circle"></i> No, Cancel!'
    }).then(function () {
      window.location.href="index.html";
    });
  });
  $('.btn-menu-dashboard').on('click', function(){
    var body=$('.dashboard-contentPage');
    var sidebar=$('.dashboard-sideBar');
    if(sidebar.css('pointer-events')=='none'){
      body.removeClass('no-paddin-left');
      sidebar.removeClass('hide-sidebar').addClass('show-sidebar');
    }else{
      body.addClass('no-paddin-left');
      sidebar.addClass('hide-sidebar').removeClass('show-sidebar');
    }
  });
  $('.btn-Notifications-area').on('click', function(){
    var NotificationsArea=$('.Notifications-area');
    if(NotificationsArea.css('opacity')=="0"){
      NotificationsArea.addClass('show-Notification-area');
    }else{
      NotificationsArea.removeClass('show-Notification-area');
    }
  });
  $('.btn-search').on('click', function(){
    swal({
      title: '¿Dime que estás buscando?',
      confirmButtonText: '<i class="zmdi zmdi-search"></i>  Buscar',
      confirmButtonColor: '#03A9F4',
      showCancelButton: true,
      cancelButtonColor: '#F44336',
      cancelButtonText: '<i class="zmdi zmdi-close-circle"></i> Cancelar',
      html: '<div class="form-group label-floating">'+
            '<label class="control-label" for="InputSearch">Escribe aquí..</label>'+
            '<input class="form-control" id="InputSearch" type="text">'+
        '</div>'
    }).then(function () {
      swal(
        'Excelente',
        ''+$('#InputSearch').val()+'',
        'success'
      )
    });
  });
  $('.btn-modal-help').on('click', function(){
    $('#Dialog-Help').modal('show');
  });
});
(function($){
    $(window).on("load",function(){
        $(".dashboard-sideBar-ct").mCustomScrollbar({
          theme:"light-thin",
          scrollbarPosition: "inside",
          autoHideScrollbar: true,
          scrollButtons: {enable: true}
        });
        $(".dashboard-contentPage, .Notifications-body").mCustomScrollbar({
          theme:"dark-thin",
          scrollbarPosition: "inside",
          autoHideScrollbar: true,
          scrollButtons: {enable: true}
        });
    });
})(jQuery);


function abrir_modal_edicion(url) {
  $('#edicion').load(url, function () {
    $(this).modal('show');
  });
}
function abrir_modal_creacion(url) {
  $('#creacion').load(url, function () {
    $(this).modal('show');
  });
}
function abrir_modal_eliminacion(url) {
  $('#eliminacion').load(url, function () {
    $(this).modal('show');
  });
}
function cerrar_modal_creacion(){
  $('#creacion').modal('hide');
}
function cerrar_modal_edicion() {
  $('#edicion').modal('hide');
}
function cerrar_modal_eliminacion() {
  $('#eliminacion').modal('hide');
}
function activarBoton(){
  if($('#boton_creacion').prop('disabled')){
    $('#boton_creacion').prop('disabled',false);
  }else{
    $('#boton_creacion').prop('disabled', true);
  }
}
function mostrarErroresCreacion(errores){
  $('#errores').html("");
  let error = "";
  for(let item in errores.responseJSON.error){
    error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error[item] + '</strong></div>';
  }
  $('#errores').append(error);
}
function mostrarErroresEdicion(errores) {
  $('#erroresEdicion').html("");
  let error = "";
  for (let item in errores.responseJSON.error) {
    error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error[item] + '</strong></div>';
  }
  $('#erroresEdicion').append(error);
}
function notificacionError(mensaje){
  Swal.fire({
    title: 'Error!',
    text: mensaje,
    icon: 'error'
  })
}

function notificacionSuccess(mensaje) {
  Swal.fire({
    title: 'Buen Trabajo!',
    text: mensaje,
    icon: 'success'
  })
}