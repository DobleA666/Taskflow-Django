// static/js/confirmations.js
// Confirmaciones para acciones destructivas

document.addEventListener('DOMContentLoaded', function() {
    // Confirmación para eliminar comentarios
    const deleteCommentLinks = document.querySelectorAll('a[href*="eliminar_comentario"]');
    deleteCommentLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
                e.preventDefault();
            }
        });
    });
    
    // Confirmación para eliminar tareas
    const deleteTaskLinks = document.querySelectorAll('a[href*="eliminar_tarea"]');
    deleteTaskLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar esta tarea? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
    
    // // Confirmación para eliminar proyectos
    // const deleteProjectLinks = document.querySelectorAll('a[href*="eliminar_proyecto"]');
    // deleteProjectLinks.forEach(link => {
    //     link.addEventListener('click', function(e) {
    //         if (!confirm('¿Estás seguro de que quieres eliminar este proyecto? Se eliminarán todas las tareas y comentarios asociados.')) {
    //             e.preventDefault();
    //         }
    //     });
    // });
});