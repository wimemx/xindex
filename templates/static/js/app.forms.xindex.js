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
                "id='removeQuestions'/>  Eliminar preguntas asociadas" +
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




    //<--- REMOVE Business Unit --->//
    $(document).on('click', '.remove-business-unit', function (e) {
    //$('.remove-business-unit').on('click', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message: "¿Esta seguro que desea eliminar esta unidad de servicio?" +
                " Esta accion no se puede deshacer<br><br>" +
                "<small>" +
                "<input type='checkbox' " +
                "id='removeALGO'/>  Eliminar servicios asociados" +
                "</small>",
            title: "Eliminar un unidad de servicio",
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
                                        '<strong>¡La unidad de servicio se elimino con exito!</strong>' +
                                        '</div>';
                                    $('#news_section').html(alerta);
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 500);
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

    //--- Función corregir problema modal  Business Units---//
    $('#myBUGrid').on('click', 'a.update_bu', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        if (url.indexOf('#') == 0) {
            $(url).modal('open');
        } else {
            $.get(url,function (data) {
                $('<div class="modal" id="update-businessUnit">' + data + '</div>').modal();
            }).success(function () {
                    $('input:text:visible:first').focus();
                });
        }


    });


    //--- Función para elimar registro de SERVICIO del sistema---//
    $(document).on('click', '.remove-service', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message:
                    "¿Esta seguro que desea eliminar éste servicio ",
            title: "Eliminarservicio",
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
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 0);
                                    return true;
                                }
                            },
                            error: function (msg) {
                            }

                        });
                    }
                }
            }
        });
    });


    //--- Función corregir problema modal Services (SERVICIOS)---//
    $('#mySGrid').on('click', 'a.update_service', function (e) {
        //alert('entra');
        e.preventDefault();
        var url = $(this).attr('href');
        if (url.indexOf('#') == 0) {
            $(url).modal('open');
        } else {
            $.get(url,function (data) {
                $('<div class="modal" id="update-service">' + data + '</div>').modal();
            }).success(function () {
                    $('input:text:visible:first').focus();
                });
        }


    });

    //--- Función corregir problema modal  Subsidiary Types---//
    $('#mySTGrid').on('click', 'a.edit-subType', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        if (url.indexOf('#') == 0) {
            $(url).modal('open');
        } else {
            $.get(url,function (data) {
                $('<div class="modal" id="edit-subType">' + data + '</div>').modal();
            }).success(function () {
                    $('input:text:visible:first').focus();
                });
        }


    });

    //--- Función para elimar registro de Subsidiary Types---//
    $("#mySTGrid").on('click', '.remove-subsidiaryType', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message:
                    "¿Esta seguro que desea eliminar éste tipo de sucursal? ",
            title: "Eliminar una Tipo sucursal",
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
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 0);
                                    return true;
                                }
                            },
                            error: function (msg) {
                            }

                        });
                    }
                }
            }
        });
    });



    //--- Función para elimar registro de Zona---//
    $(document).on('click', '.remove-zone', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message:
                    "¿Esta seguro que desea eliminar ésta zona ",
            title: "Eliminar una zona",
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
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 0);
                                    return true;
                                }
                            },
                            error: function (msg) {
                            }

                        });
                    }
                }
            }
        });
    });


    //--- Función para elimar registro de usario del sistema---//
    $(document).on('click', '.remove-user', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message:
                    "¿Esta seguro que desea eliminar éste usuario ",
            title: "Eliminar usuario",
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
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 0);
                                    return true;
                                }
                            },
                            error: function (msg) {
                            }

                        });
                    }
                }
            }
        });
    });

    //--- Función corregir problema modal  Edit User---//
    $('#myULGrid').on('click', 'a.edit-user', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        if (url.indexOf('#') == 0) {
            $(url).modal('open');
        } else {
            $.get(url,function (data) {
                $('<div class="modal" id="edit-user">' + data + '</div>').modal();
            }).success(function () {
                    $('input:text:visible:first').focus();
                });
        }


    });


    //--- Función para elimar registro de cliente del sistema---//
    $(document).on('click', '.remove-client', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        bootbox.dialog({
            message:
                    "¿Esta seguro que desea eliminar éste cliente ",
            title: "Eliminar cliente",
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
                                    setTimeout(function () {
                                        window.location.reload(true);
                                    }, 0);
                                    return true;
                                }
                            },
                            error: function (msg) {
                            }

                        });
                    }
                }
            }
        });
    });

    //--- Función corregir problema modal  Edit User---//
    $('#myCGrid').on('click', 'a.edit-client', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        if (url.indexOf('#') == 0) {
            $(url).modal('open');
        } else {
            $.get(url,function (data) {
                $('<div class="modal" id="edit-client">' + data + '</div>').modal();
            }).success(function () {
                    $('input:text:visible:first').focus();
                });
        }


    });


})