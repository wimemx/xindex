/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 20/09/13
 * Time: 09:44 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {

    $("#id_name").keyup(function () {
        if ($(this).val().length >= 1) {
            $('#save-link').removeClass('hidden');
        } else {
            $('#save-link').addClass('hidden');
        }
    });

    $('#step-one-next').on('click', function (e) {
        e.preventDefault();
        if ($('#id_name').val().length > 1) {
            $.ajax({
                url: '/surveys/save/next/2/empty',
                type: 'POST',
                data: $('#new-survey-form').serialize(),
                dataType: 'Json',
                success: function (msg) {
                    if (msg.save) {
                        alert('Se ha guardado la encuesta');
                        window.location.href = msg.url;
                    }
                },
                error: function (msg_error) {
                    alert(msg_error.error);
                }
            });
        } else {
            return false;
        }

    });


    /*Funciones para insertar bloques de preguntas*/
    $('#add-block-questions').on('click', function () {
        $('div.default-buttons').fadeOut();
        $('#survey-main-content').append(
            '<div class="animated rollIn">' +
                '<div class="col-lg-12">' +
                '<section class="panel">' +
                '<div class="panel-body">' +
                    '<header class="h4 text-center">'+
                        'Este es el nombre del bloque de preguntas'+
                    '</header>'+
                    '<small class="wrapper">'+
                        '<p>'+
                            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'+
                        '</p>'+
                    '</small>'+
                '</div>' +
                '</section>' +
                '</div>' +
                '</div>');
    });


})