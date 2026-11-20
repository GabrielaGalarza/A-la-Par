document.addEventListener('DOMContentLoaded', () => {
    const temas = [
        { nombre: 'OneLake', descripcion: 'Descripción breve de OneLake', ejemplo: 'Ejemplo concreto de OneLake' },
        { nombre: 'Lakehouse', descripcion: 'Descripción breve de Lakehouse', ejemplo: 'Ejemplo concreto de Lakehouse' },
        { nombre: 'Arquitectura de medallón', descripcion: 'Descripción breve de Arquitectura de medallón', ejemplo: 'Ejemplo concreto de Arquitectura de medallón' }
    ];

    let progreso = JSON.parse(localStorage.getItem('progreso')) || 0;
    const progresoElement = document.getElementById('progreso');
    const continuarButton = document.getElementById('continuar');
    const temaElement = document.createElement('div');

    function actualizarProgreso() {
        progresoElement.textContent = `${progreso} de ${temas.length} temas completados`;
        if (progreso >= temas.length) {
            continuarButton.textContent = 'Ruta completada';
        }
    }

    function mostrarTema() {
        if (progreso < temas.length) {
            const tema = temas[progreso];
        temaElement.innerHTML = `
                <h3>${tema.nombre}</h3>
                <p>${tema.descripcion}</p>
                <p><strong>Ejemplo:</strong> ${tema.ejemplo}</p>
                <button id="completado">Marcar como completado</button>
            `;
            document.body.appendChild(temaElement);
            document.getElementById('completado').onclick = () => {
                progreso++;
                localStorage.setItem('progreso', JSON.stringify(progreso));
                temaElement.innerHTML = '';
                actualizarProgreso();
                mostrarTema();
            };
        } else {
            temaElement.innerHTML = '<p>Has completado todos los temas.</p>';
            document.body.appendChild(temaElement);
        }
    }

    continuarButton.onclick = () => {
        mostrarTema();
        continuarButton.style.display = 'none';
    };

    actualizarProgreso();
});
