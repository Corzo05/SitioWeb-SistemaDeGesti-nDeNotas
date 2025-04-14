//Scroll de pagina al recargar
window.addEventListener('beforeunload', function() {
  localStorage.setItem('scrollPosition', window.scrollY);
});

window.addEventListener('load', function() {
  const scrollPosition = localStorage.getItem('scrollPosition');
  if (scrollPosition) {
    window.scrollTo(0, parseInt(scrollPosition, 10));
  }
});

//--BUSCADORES--

//Buscador Notas Finales
$(document).ready(function(){
  $("#barra-finales").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tablas-finales tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

//Buscador Pestaña Agregar
$(document).ready(function(){
  $("#barra-agregar").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tablas-agregar tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

//Buscador Pestaña Eliminar
$(document).ready(function(){
  $("#barra-eliminar").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tablas-eliminar tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

//Buscador Pestaña Lapsos
$(document).ready(function(){
  $("#barra-lapsos").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tablas-lapsos tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

//Buscador Pestaña Reportes
$(document).ready(function(){
  $("#barra-reportes").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tablas-reportes tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

//Para evitar que se oculte la barra con texto dentro
const input = document.querySelector('.contenedor_barra input');
  input.addEventListener('input', () => {
  if (input.value.length > 0) {
    input.classList.add('show');
  } else {
    input.classList.remove('show');
  }
});

//Modal agregar Actividades con %
// const btnAñadirCampo = document.getElementById('añadir_campo');
// const con_materias = document.getElementById('con_materias');
// const divFooter = document.getElementById('modal-footer')

// let contadorCampos = 0;

// btnAñadirCampo.addEventListener('click', () => {
//   contadorCampos++;

//   //Contenedor
//   const contenedorCampos = document.createElement('div');
//   contenedorCampos.className = 'contenedor-camposNuevos';

//   //Label
//   const label = document.createElement('label');
//   label.for = `label${contadorCampos}`;
//   label.textContent = `Actividad ${contadorCampos}`;
//   label.className = 'text-white';

//   //Input descripcion
//   const input = document.createElement('input');
//   input.type = 'text';
//   input.name = `input${contadorCampos}`;
//   input.id = `input${contadorCampos}`;
//   input.className = 'input-actividades'

//   //Input porcentaje
//   const inputPorcentaje = document.createElement('input');
//   inputPorcentaje.type = 'text';
//   inputPorcentaje.name = `inputPorcentaje${contadorCampos}`;
//   inputPorcentaje.id = `inputPorcentaje${contadorCampos}`;
//   inputPorcentaje.className = 'input-porcentaje'

//   //Input fecha
//   const inputFecha = document.createElement('input');
//   inputFecha.type = 'date';
//   inputFecha.name = `inputFecha${contadorCampos}`;
//   inputFecha.id = `inputFecha${contadorCampos}`;
//   inputFecha.className = 'input-fecha'

//   //Input nota maxima
//   const inputNotaMaxima = document.createElement('input');
//   inputNotaMaxima.type = 'text';
//   inputNotaMaxima.name = `inputNotaMaxima${contadorCampos}`;
//   inputNotaMaxima.id = `inputNotaMaxima${contadorCampos}`;
//   inputNotaMaxima.className = 'input-nota'

//   //Btn Eliminar
//   const btnEliminar = document.createElement('button');
//   btnEliminar.type = 'button';
//   btnEliminar.textContent = 'Remover Actividad';
//   btnEliminar.addEventListener('click', () => {
//     con_materias.removeChild(contenedorCampos);
//     contadorCampos = 0;
//   });

//   //Agregar todo al contenedor
//   contenedorCampos.appendChild(label);
//   contenedorCampos.appendChild(input);
//   contenedorCampos.appendChild(inputPorcentaje);
//   contenedorCampos.appendChild(inputFecha);
//   contenedorCampos.appendChild(inputNotaMaxima);
//   contenedorCampos.appendChild(btnEliminar);

//   //Agregar el contenedor al formulario
//   con_materias.appendChild(contenedorCampos);
// });