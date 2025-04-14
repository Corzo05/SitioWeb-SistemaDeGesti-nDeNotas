//Alertas botones generar reportes
document.querySelectorAll('.boton-imprimir').forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault();
  
    const href = this.href;
    Swal.fire({
      title: "Reporte de Notas Generado",
      icon: "success"
    }).then((result) => {
          if (result.isConfirmed) {
              window.location.href = href;
          }
      });
  });
});

//Alerta boton Reiniciar Numeracion
document.querySelectorAll('.btn-numeracion').forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault();

    const href = this.href;

    Swal.fire({
      title: "¿Desea reiniciar la numeración de los estudiantes?",
      text: "ADVERTENCIA: Si reinicia la numeración con registros existentes pueden ocurrir conflictos con las operaciones.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Si",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "¿Está Seguro?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#d33",
          cancelButtonColor: "#3085d6",
          confirmButtonText: "Reiniciar",
          cancelButtonText: "Cancelar",
        }).then((result) => {
          if(result.isConfirmed){
            Swal.fire({
              title: 'Numeración reiniciada a "1"',
              icon: "success"
            }).then((result) => {
              if(result.isConfirmed){
                window.location.href = href;
              }
            });
          }
        });
      }
    });
  });
});

//Alertas botones generar reportes pack completo
document.querySelectorAll('.botones-pdfs').forEach(button => {
  button.addEventListener('click', function() {

    const form = this.closest('form');
    form.addEventListener('submit', function(event){
      event.preventDefault();
      Swal.fire({
        title: "Reporte de Notas Generado",
        icon: "success"
      }).then((result) => {
            if (result.isConfirmed) {
                form.submit();
            }
      });
    })
  });
});

//No poner nada debajo de estos 2 bloques de codigo de abajo

//Alerta de boton agregar Admins
document.getElementById('btn_agregar_admin').addEventListener('click', function(event) { 
  event.preventDefault();
    
  const nombre = document.getElementById('nombre').value;
  const usuario = document.getElementById('usuario').value;
  const contraseña = document.getElementById('contraseña').value;
  const rol = document.getElementById('rol').value;
  const materia = document.getElementById('materia').value;
    
  if(nombre === "" || usuario === "" || contraseña === "" || rol === "" || materia === ""){
    Swal.fire({
      icon: "error",
      title: "Datos Faltantes",
      text: "No deje campos vacíos!!",
    });
  }else{
    Swal.fire({
      title: "Administrador Agregado con Éxito",
      icon: "success"
    }).then((result) => { 
      if (result.isConfirmed) { 
        document.getElementById('formulario-agregar-administradores').submit(); 
      } 
    }); 
  }
});
    
//Alerta de editar Admins
document.querySelectorAll('.editAdmins').forEach(button => { 
  button.addEventListener('click', function() { 
    const modalId = this.getAttribute('data-bs-target'); 
    const form = document.querySelector(`${modalId} .editFormAdmins`); 
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
