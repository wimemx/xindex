/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 12/09/13
 * Time: 01:10 PM
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function () {

    $('.check').on('click', function (e) {
        if($(".check").is(':checked')) {
            $("#options-survey").attr('disabled', false);
            $("#remove-survey").attr('disabled', false);
            //$(".check").attr('checked', true);
        } else {
            $("#options-survey").attr('disabled', true);
            $("#remove-survey").attr('disabled', true);
        }
    });

    $('.remove-moment').on('click', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message: "¿Esta seguro que desea eliminar este punto de contacto?" +
                " Esta accion no se puede deshacer<br><br>" +
                "<small>" +
                "<input type='checkbox' " +
                "class='form-control' " +
                "id='removeQuestions'/>Eliminar preguntas asociadas" +
                "</small>",
            title: "Eliminar un punto de contacto",
            buttons: {
                success: {
                    label: "Cancelar",
                    className: "bg-danger btn-modal-xindex",
                    callback: function () {
                    }
                },
                main: {
                    label: "Aceptar",
                    className: "bg-success btn-modal-xindex",
                    callback: function () {
                        $.ajax({
                            type: 'GET',
                            url: href,
                            success: function (msg) {
                                if (msg == 'Si') {
                                    var alerta = '<div class="alert alert-warning">' +
                                        '<button type="button" class="close" data-dismiss="alert">' +
                                        '<i class="icon-remove"></i>' +
                                        '</button>' +
                                        '<i class="icon-ok-sign"></i>' +
                                        '<strong>¡El punto de contacto se elimino con exito!</strong>' +
                                        '</div>';
                                    $('#news_section').html(alerta);
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 1000);
                                    return true;
                                }
                            },
                            error: function (msg) {
                                var alerta = '<div class="alert alert-danger">' +
                                    '<button type="button" class="close" data-dismiss="alert">' +
                                    '<i class="icon-remove"></i>' +
                                    '</button>' +
                                    '<i class="icon-ban-circle"></i>' +
                                    '<strong>¡No fue posible realizar su peticion, intente mas tarde!</strong>' +
                                    '</div>';
                                $('#news_section').html(alerta);
                            }

                        });
                    }
                }
            }
        });
    });

    $('#myAttributesGrid').on('click', 'a.delete-attribute', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message: "¿Esta seguro que desea eliminar el atributo? Se eliminaran la relacion con las preguntas asociadas en las encuestas",
            title: "Eliminar Atributo",
            buttons: {
                success: {
                    label: "Cancelar",
                    className: "btn-white",
                    callback: function () {
                        return true;
                    }
                },
                main: {
                    label: "Eliminar",
                    className: "btn-twitter",
                    callback: function () {
                        $.ajax({
                            type: 'GET',
                            url: href,
                            success: function (msg) {
                                if (msg == 'Si') {
                                    var alerta = '<div class="alert alert-success">' +
                                        '<button type="button" class="close" data-dismiss="alert">' +
                                        '<i class="icon-remove"></i>' +
                                        '</button>' +
                                        '<i class="icon-ok-sign"></i>' +
                                        '<strong>¡El indicador se elimino con exito!</strong>' +
                                        '</div>';
                                    $('#news_section').html(alerta);
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 2000);
                                    return true;
                                }
                            },
                            error: function (msg) {
                                var alerta = '<div class="alert alert-danger">' +
                                    '<button type="button" class="close" data-dismiss="alert">' +
                                    '<i class="icon-remove"></i>' +
                                    '</button>' +
                                    '<i class="icon-ban-circle"></i>' +
                                    '<strong>¡No fue posible realizar su peticion, intente mas tarde!</strong>' +
                                    '</div>';
                                $('#news_section').html(alerta);
                            }

                        });
                    }
                }
            }
        });
    })


    $('#myAttributesGrid').on('click', 'a.update-attribute', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        if (url.indexOf('#') == 0) {
            $(url).modal('open');
        } else {
            $.get(url,function (data) {
                $('<div class="modal" id="update-modal">' + data + '</div>').modal();
            }).success(function () {
                    $('input:text:visible:first').focus();
                });
        }


    });

    $(document).on('click', 'a.close-update-modal', function(){
        $('div.modal').modal('hide');
        $('#ajaxModal').remove();
    })


    $(document).on('submit', '#update-moment-form', function (e) {
        e.preventDefault();
        var action = $(this).attr('action');
        $.ajax({
            type: "POST",
            url: action,
            data: $(this).serialize(),
            success: function (msg) {
                if (msg == 'Si') {
                    var alerta = '<div class="alert alert-success">' +
                        '<button type="button" class="close" data-dismiss="alert">' +
                        '<i class="icon-remove"></i>' +
                        '</button>' +
                        '<i class="icon-ok-sign"></i>' +
                        '<strong>¡El punto de contacto ha sido actualizado!</strong>' +
                        '</div>';
                    $('#news_section').html(alerta);
                    $('div.modal').modal('hide');
                    setTimeout(function () {
                        window.location.reload(true);
                    }, 2000);
                } else if (msg == 'No') {
                    alert('Verifique los errores en el formulario e intente de nuevo')
                }
            },
            error: function (msg_failu) {
                var alerta = '<div class="alert alert-danger">' +
                    '<button type="button" class="close" data-dismiss="alert">' +
                    '<i class="icon-remove"></i>' +
                    '</button>' +
                    '<i class="icon-ban-circle"></i>' +
                    '<strong>¡No fue posible realizar la operacion, intente mas tarde!< /strong>' +
                    '</div>';
                $('#news_section').html(alerta);
                $('div.modal').modal('hide');
            }
        });
    });


})