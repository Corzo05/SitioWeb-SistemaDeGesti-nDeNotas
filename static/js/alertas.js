//Alerta de botones de carga de notas Finales
document.querySelectorAll('.boton-cargar').forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault();

    const href = this.href;
    Swal.fire({
      title: "Notas Definitivas Cargadas",
      icon: "success"
    }).then((result) => {
          if (result.isConfirmed) {
              window.location.href = href;
          }
      });
  });
});

//Alerta botones salir
document.getElementById('boton-salir').addEventListener('click', function(event) { 
  event.preventDefault();  
  Swal.fire({
    title: "¿Seguro que desea salir?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    cancelButtonText: "Cancelar",
    confirmButtonText: "Salir"
  }).then((result) => { 
    if (result.isConfirmed) { 
      document.getElementById('form-salir').submit(); 
    } 
  }); 
});

//Alerta botones eliminar
document.querySelectorAll('.boton-eliminar').forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault();

    const href = this.href;

    Swal.fire({
      title: "¿Desea eliminar el registro seleccionado?",
      text: "Los datos se perderán",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Eliminar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Registro Eliminado",
          icon: "success"
        }).then((result) => {
          if(result.isConfirmed){
            window.location.href = href;
          }
        });
      }
    });
  });
});

//Alerta de botones cargar notas lapsos
document.querySelectorAll('.editButton').forEach(button => { 
  button.addEventListener('click', function() { 
    const modalId = this.getAttribute('data-bs-target'); 
    const form = document.querySelector(`${modalId} .editForm`); 
    form.addEventListener('submit', function(event) { 
      event.preventDefault(); 
      Swal.fire({
        title: "Datos Actualizados",
        icon: "success"
      }).then((result) => { 
        if (result.isConfirmed) { 
          form.submit(); 
        } 
      }); 
    }); 
  }); 
});

// Alerta de botones promedio
document.querySelectorAll('.boton-promedio').forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault();

    const href = this.href;
    Swal.fire({
      title: "Promedio Calculado",
      icon: "success",
    }).then((result) => {
          if (result.isConfirmed) {
              window.location.href = href;
          }
      });
  });
});

//Alerta de boton de agregar formulario A
document.getElementById('btn_agregar_A').addEventListener('click', function(event) { 
  event.preventDefault();

  const nombre_completo_A = document.getElementById('nombre_completo_A').value;
  const sexo_A = document.getElementById('sexo_A').value;
  const cedula_A = document.getElementById('cedula_A').value;

  const cedulaConfirm = document.querySelectorAll('#input-cedula');
  const nombreConfirm = document.querySelectorAll('#input-nombre');

  const cedulasConfirm = [];

  cedulaConfirm.forEach(input => {
    cedulasConfirm.push(input.value);
  });

  const nombresConfirm = [];

  nombreConfirm.forEach(input => {
    nombresConfirm.push(input.value);
  });

  if(nombre_completo_A === "" || sexo_A === "" || cedula_A === ""){
    Swal.fire({
      icon: "error",
      title: "Datos Faltantes",
      text: "No deje campos vacíos!!",
    });
  }else if(cedulasConfirm.includes(cedula_A) || nombresConfirm.includes(nombre_completo_A)){
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Datos ya existentes!!",
    });
  }else{
    let respuesta = true
    console.log(respuesta)
    Swal.fire({
      title: "Estudiante Agregado con Éxito",
      icon: "success"
    }).then((result) => { 
      if (result.isConfirmed) { 
        document.getElementById('formulario-agregarA').submit(); 
      } 
    }); 
  }
});

//Alerta de boton de agregar formulario B
document.getElementById('btn_agregar_B').addEventListener('click', function(event) { 
  event.preventDefault(); 
  
  const nombre_completo_B = document.getElementById('nombre_completo_B').value;
  const sexo_B = document.getElementById('sexo_B').value;
  const cedula_B = document.getElementById('cedula_B').value;

  const cedulaConfirmB = document.querySelectorAll('#input-cedulaB');
  const nombreConfirmB = document.querySelectorAll('#input-nombreB');

  const cedulasConfirmB = [];

  cedulaConfirmB.forEach(input => {
    cedulasConfirmB.push(input.value);
  });

  const nombresConfirmB = [];

  nombreConfirmB.forEach(input => {
    nombresConfirmB.push(input.value);
  });
  
  if(nombre_completo_B === "" || sexo_B === "" || cedula_B === ""){
    Swal.fire({
      icon: "error",
      title: "Datos Faltantes",
      text: "No deje campos vacíos!!",
    });
  }else if(cedulasConfirmB.includes(cedula_B) || nombresConfirmB.includes(nombre_completo_B)){
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Datos ya existentes!!",
    });
  }else{
    Swal.fire({
      title: "Estudiante Agregado con Éxito",
      icon: "success"
    }).then((result) => { 
      if (result.isConfirmed) { 
        document.getElementById('formulario-agregarB').submit(); 
      } 
    }); 
  }
});

//Alerta de boton de editar registro A
document.querySelectorAll('.editButtonA').forEach(button => { 
  button.addEventListener('click', function() { 
    const modalId = this.getAttribute('data-bs-target'); 
    const form = document.querySelector(`${modalId} .editFormA`); 
    form.addEventListener('submit', function(event) { 
      event.preventDefault();

        Swal.fire({
          icon: "success",
          title: "Datos Editados",
        }).then((result) => { 
          if (result.isConfirmed) { 
            form.submit(); 
          } 
        }); 
    }); 
  }); 
});

//Alerta de boton de editar registro B
document.querySelectorAll('.editButtonB').forEach(button => { 
  button.addEventListener('click', function() { 
    const modalId = this.getAttribute('data-bs-target'); 
    const form = document.querySelector(`${modalId} .editFormB`); 
    form.addEventListener('submit', function(event) { 
      event.preventDefault(); 

        Swal.fire({
          icon: "success",
          title: "Datos Editados",
        }).then((result) => { 
          if (result.isConfirmed) { 
            form.submit(); 
          } 
        }); 
    }); 
  }); 
});