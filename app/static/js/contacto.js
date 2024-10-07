emailjs.init('CjHAQVH9qwdZeYKH5');

const btn = document.getElementById('button-contacto');

document.getElementById('form').addEventListener('submit', function(event) {
    event.preventDefault();

    const serviceID = "service_vevfpz3";
    const templateID = "template_b28anlm";

    const templateParams = {
        from_name: document.getElementById('nombre').value,
        to_name: 'Nombre del Destinatario',
        correo: document.getElementById('correo').value,
        celular: document.getElementById('celular').value,
        mensaje: document.getElementById('mensaje').value
    };

    emailjs.send(serviceID, templateID, templateParams)
        .then(() => {
            Swal.fire({
                icon: 'success',
                title: 'Se envió el mensaje',
                timer: 2500,
                showConfirmButton: false
            });
            window.location = "contacto.html";
        }, (err) => {
            btn.value = 'Send Email';
            alert(JSON.stringify(err));
        });
});
