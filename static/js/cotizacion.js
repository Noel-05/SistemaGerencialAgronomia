var lineasDeDetalle = [];
var cotizacion = {};
var listaDetalleHTML = document.getElementById('lista-detalle');
var total = 0.0;
var totalHTML = document.getElementById('total');

function agregarLinea(){
                    var listaProductos = document.querySelector('select');
                    var nombreProducto = listaProductos.options[listaProductos.selectedIndex].textContent;

                    var listaSubtipos = document.getElementById('tipoProducto');
                    var subtipo = listaSubtipos.options[listaSubtipos.selectedIndex].textContent;

                    var cantidades = document.getElementById('cantidades');
                    var cantidades2 = cantidades.options[cantidades.selectedIndex].textContent;

                    var cantidad = document.getElementById('cantidad').value;
                    var largo = document.getElementById('largo').value;
                    var ancho = document.getElementById('ancho').value;

                    var tablaCotizacion = document.getElementById('cotizacion');
                    var tbodyDetalles = document.getElementById('detalles');

                    var fila = tbodyDetalles.insertRow();

                    var columnaCant = fila.insertCell();
                    var columnaProducto = fila.insertCell();
                    var columnaTipo = fila.insertCell();
                    var columnaPunitario = fila.insertCell();
                    var columnaSubtotal = fila.insertCell();
                    var columnaEliminar = fila.insertCell();

                    var prod = document.createTextNode(nombreProducto);
                    columnaProducto.appendChild(prod);

                    if(nombreProducto == 'Banner' || nombreProducto == 'Vinil'){
                        if(subtipo == 'Ojetes'){
                            var sub = document.createTextNode(subtipo);
                            columnaTipo.appendChild(sub);
                        }else{
                            var sub = document.createTextNode(subtipo + ' ' + largo + 'x' + ancho + ' m²');
                            columnaTipo.appendChild(sub);
                        }
                    }else{
                        var sub = document.createTextNode(subtipo);
                        columnaTipo.appendChild(sub);
                    }


                    //If para mostrar en Cotización la cantidad a partir de si es fija o variable
                    if(nombreProducto == 'Banner' || nombreProducto == 'Vinil'){
                        var cantidad = document.getElementById('cantidad').value;
                        var cant = document.createTextNode(cantidad);
                        columnaCant.appendChild(cant);
                    }else{
                        var cantidades = document.getElementById('cantidades');
                        var cantidad = cantidades.options[cantidades.selectedIndex].textContent;
                        var cant = document.createTextNode(cantidad);
                        columnaCant.appendChild(cant);
                    }

                    var subtipo = listaSubtipos.options[listaSubtipos.selectedIndex];
                    var precioU = subtipo.getAttribute('precio'); //Precio que se va al objeto
                    var precioUni = '$' + subtipo.getAttribute('precio'); //Precio que se muestra en la cotización
                    var precio = document.createTextNode(precioUni);
                    columnaPunitario.appendChild(precio);

                    var subtotal = 0.0;

                    //Calculando subtotal incluyendo restriciones de precios por metro cuadrado para Banner y Vinil
                    var subtip = listaSubtipos.options[listaSubtipos.selectedIndex].textContent;

                    if(nombreProducto == 'Banner' || nombreProducto == 'Vinil'){
                        if(nombreProducto == 'Banner' && subtip == 'Ojetes'){
                            subtotal1 = cantidad * precioU;
                        }else{
                            subtotal1 = cantidad * precioU * largo * ancho;
                        }
                    }else{
                        subtotal1 = precioU*1;
                    }

                    //producto contendra las seleciones del usuario, son lineas de cotizacion o detalle
                    var producto = {
                        cant: cantidad * 1,
                        producto: listaProductos.options[listaProductos.selectedIndex].textContent,
                        subtipo: listaSubtipos.options[listaSubtipos.selectedIndex].textContent,
                        subtotal: subtotal1,
                        preciouni: precioU*1,
                    };

                    lineasDeDetalle.push(producto); //ingreso de nuevo producto o una nueva linea de detalle
                    total += producto.subtotal;

                    var subtotal1 = '$' + Number.parseFloat(producto.subtotal).toFixed(2);
                    var subtotal2 = document.createTextNode(subtotal1);
                    columnaSubtotal.appendChild(subtotal2);

                    totalHTML.textContent = '$' + Number.parseFloat(total).toFixed(2);

                    //Limpiar el formulario
                    var div = document.getElementById('bv');
                    var div2 = document.getElementById("bfat");
                    var div3 = document.getElementById('cant');

                    div.style.display = 'none';
                    div2.style.display = 'none';
                    div3.style.display = 'none';
                    document.getElementById('formulario').reset();

                    console.log(lineasDeDetalle);
}

function validarLinea(){

    var listaProductos = document.querySelector('select');
    var nombreProducto = listaProductos.options[listaProductos.selectedIndex].textContent;

    var listaSubtipos = document.getElementById('tipoProducto');
    var subtipo = listaSubtipos.options[listaSubtipos.selectedIndex].textContent;

    var cantidades = document.getElementById('cantidades');
    var cantidades2 = cantidades.options[cantidades.selectedIndex].textContent;

    var cantidad = document.getElementById('cantidad').value;
    var largo = document.getElementById('largo').value;
    var ancho = document.getElementById('ancho').value;

    if (listaProductos.selectedIndex != 0 || listaSubtipos.selectedIndex != 0){
        if(nombreProducto == 'Banner' || nombreProducto == 'Vinil'){
            if(subtipo == 'Lona' || listaSubtipos.selectedIndex != 0 && subtipo != 'Ojetes'){
                if(cantidad == "" || largo == "" || ancho == ""){
                    console.log('No 1');
                    return;
                }else{
                    //Agregar
                    //console.log('SIII');
                    agregarLinea();
                }
            }else{
                if(subtipo == 'Ojetes'){
                    if(cantidad == ""){
                        console.log('No 2');
                        return;
                    }else{
                        //Agregar
                        //console.log('SIII');
                        agregarLinea();
                    }
                }
            }

        }else{
            if(cantidades.selectedIndex == 0){
                console.log('No 3');
                return;
            }else{
                //Agregar
                //console.log('SIII');
                agregarLinea();
            }
        }

    }else{
        console.log('No 4');
        return;
    }

    //document.getElementById('formulario').reset();
}

var subtipos;

function obtenerSubtipos() {

    var listaProductos = document.querySelector('select');
    var nombreProducto = listaProductos.options[listaProductos.selectedIndex].textContent;

    var listaSubtipos = document.getElementById('tipoProducto');
    var listaCantidades = document.getElementById('cantidades');

    if (listaProductos.selectedIndex==0) {
        listaSubtipos.innerHTML = '<option>Antes seleciona un producto</option>';
        return;
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

           subtipos = JSON.parse(xhttp.responseText);
           listaSubtipos.innerHTML = '<option>Seleccionar tipo</option>';
           listaCantidades.innerHTML = '<option>Seleccionar cantidad</option>';


           for (var i = 0; i < subtipos.length; i++) {
               var subtipo = subtipos[i];
               var option = document.createElement('option');
               option.value = subtipo.fields.producto;
               option.textContent = subtipo.fields.nombre;

               var option2 = document.createElement('option');
               option2.value = subtipo.fields.producto;
               option2.textContent = subtipo.fields.cantidad;

               option.setAttribute('precio', subtipo.fields.precio);

                   listaSubtipos.appendChild(option);
                   listaCantidades.appendChild(option2);
           }
        }
    };
    xhttp.open("GET", "/cotizacion/subconjunto/"+nombreProducto+"/", true);
    xhttp.send();
}

//Función que muestra el formulario correcto a partir de la seleccion del producto
function obtenerFormulario(){
    var listaProductos = document.querySelector('select');
    var nombreProducto = listaProductos.options[listaProductos.selectedIndex].textContent;
    var listaSubtipos = document.getElementById('tipoProducto');
    var subtip = listaSubtipos.options[listaSubtipos.selectedIndex].textContent;

    var div = document.getElementById('bv');
    var div2 = document.getElementById("bfat");
    var div3 = document.getElementById('cant');

    if(nombreProducto == 'Brochure' || nombreProducto == 'Flyers' || nombreProducto == 'Afiche' ||
        nombreProducto == 'Tarjetas de presentación' || nombreProducto == 'Tarjetas de presentacion'){
        div.style.display = 'none';
        div2.style.display = 'inline';
        div3.style.display = 'none';
    }

    if(nombreProducto == 'Banner' || nombreProducto == 'Vinil'){
        div.style.display = 'none';
        div2.style.display = 'none';
        div3.style.display = 'none';
    }
}

//Función que muestra el formulario correcto a partir de la seleccion del subtipo de producto
function obtenerFormulario2(){

    var listaProductos = document.querySelector('select');
    var nombreProducto = listaProductos.options[listaProductos.selectedIndex].textContent;
    var listaSubtipos = document.getElementById('tipoProducto');
    var subtip = listaSubtipos.options[listaSubtipos.selectedIndex].textContent;

    var div = document.getElementById('bv');
    var div2 = document.getElementById("bfat");
    var div3 = document.getElementById('cant');

    if(nombreProducto == 'Banner' || nombreProducto == 'Vinil'){
        if(nombreProducto == 'Banner' && subtip == 'Ojetes'){
            div.style.display = 'none';
            div2.style.display = 'none';
            div3.style.display = 'inline';
        }else{
            div.style.display = 'inline';
            div2.style.display = 'none';
            div3.style.display = 'inline';
        }
    }else{
        div.style.display = 'none';
        div2.style.display = 'inline';
        div3.style.display = 'none';

    }
}


function obtenerPrecio(){
    var listaSubtipos = document.getElementById('tipoProducto');
    var subtipo = listaSubtipos.options[listaSubtipos.selectedIndex];

    var listaCantidades = document.getElementById('cantidades');
    var cantidad = listaCantidades.options[listaCantidades.selectedIndex];

    var precio = document.getElementById('precio');
    precio.value = subtipo.getAttribute('precio');
    precio.focus();
}

function finalizar() {


    var descripcion = document.getElementById('descripcion').value;

    if(descripcion == "" || lineasDeDetalle.length == 0){
        return;
    }else{

        var datos = JSON.stringify(lineasDeDetalle);
        var params = "registros=" + encodeURI(datos) + "&descripcion=" + descripcion + '&total=' + total;
        var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var xhttp = new XMLHttpRequest();

        xhttp.open("POST", "/cotizacion/guardar", true);
        xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhttp.setRequestHeader('X-CSRFToken', csrfToken);
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200){
                // esto inprime la respuesta
                console.log(xhttp.responseTex);
                window.location.href="/cotizacion/gestionCotizacion/";
            }
        }
        xhttp.send(params);
    }
}

function eliminarLinea(){
    delete lineasDeDetalle;
}