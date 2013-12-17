/**
 * Created with PyCharm.
 * User: martin
 * Date: 5/12/13
 * Time: 05:53 PM
 * To change this template use File | Settings | File Templates.
 */
$('#id_client_date').datepicker();
$('#wait').hide();

    //// <------ Remove modal with close class ->
    $('.close').on('click', function (e) {
        e.preventDefault();
        $('div.modal').modal('hide');
        $('#ajaxModal').remove();
    });

    $("#id_client_csv").change(function(e) {

        var fileName = $("input#id_client_csv").val().replace(/C:\\fakepath\\/i, '');
        var ext = fileName.split(".").pop().toLowerCase();

        if($.inArray(ext, ["csv"]) == -1) {
            alert('Formato de archivo incorrecto');
            return false;
        }
        if (e.target.files != undefined) {

            if ($("#csvRow").children().length != 0){
                $('#add-new-csv').removeClass("hidden");
            }

            $('#tab-header').addClass("hidden");
            $('#csvimport').removeClass("hidden");
            $("a#process-file").removeClass("hidden");
            $("#csvRow").children().remove();
            $("#addClientModal").css("width","900px");
            $("#id_modal_body").addClass("hidden");
            $('#form-csv-div').addClass("hidden");
            $(".modal-title").html("Vista previa de los datos del archivo: "
                    + "<label>"
                    + fileName +"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                    + "</label>"
                    + "<small><a href='#' id='add-new-csv' class='text-muted'>"
                    +"<i class='icon-file-text'></i>"
                    +"Cambiar</a></small>"
                    +"&nbsp;&nbsp;&nbsp;"
                    + "<a href='#' id='csv-next' class='text-muted btn btn-success btn-modal-xindex'>"
                    +"<i class='icon-arrow-right text-white'></i>"
                    +"Siguiente</a>");
            var reader = new FileReader();
            reader.onload = function(e) {
                var csvval=e.target.result.split("\n");
                var csvStartValue=csvval[0].split(","),
                    totalClients = 0;

                for(var a=0;a<csvStartValue.length;a++){

                    $("#csvRow").append("<div class='col-sm-3 padder-v'>" +
                            "<div class='row'>" +
                            "<div class='col-sm-9'><select class='form-control field'>" +
                            "<option value='null'>Sin asignar</option>" +
                            "<option value='first_name'>Nombre</option>" +
                            "<option value='last_name'>Apellido</option>" +
                            "<option value='sex'>Sexo</option>" +
                            "<option value='phone'>Teléfono</option>" +
                            "<option value='email'>Email</option>" +
                            "<option value='country'>País</option>" +
                            "<option value='state'>Estado</option>" +
                            "<option value='city'>Ciudad</option>" +
                            "<option value='company'>Compañia</option>" +
                            "</select></div>" +

                            "<div class='ck-button btn col-sm-2'>" +
                               "<label>" +
                                  "<input type='checkbox' id='checkbox"+a+"' class='checkbox hidden'><span>OK</span>" +
                               "</label>" +
                            "</div>" +
                            "</div>" +

                            "<br><div class='h-defined-description'>" +
                            "<table " +
                            "id='table"+a+"'" +
                            "class='table'" +
                            "style='margin: auto !important; width: 100%'></table>" +
                            "" +
                            "</div></div>");
                }

                for (var k=0; k<csvval.length; k++){
                    var csvvalue=csvval[k].split(","),
                        str1 = false;

                    totalClients ++;

                    for(var j=0;j<csvvalue.length;j++){
                        var dataValue=csvvalue[j],
                            myTable = $("#table"+j);

                        if( dataValue == ""){
                            continue;
                        }else{
                            myTable.append("<tr class="+k+"><td>"+dataValue+"</td></tr>");
                            //Verificar si el archivo tiene algun encabezado
                            if (k==0){
                                var str2 = "fist name",
                                    str3 = "nombre",
                                    str4 = "last name",
                                    str5 = "apellido",
                                    str6 = "email",
                                    str7 = "correo",
                                    str8 = "phone",
                                    str9 = "telefono",
                                    str10 = "teléfono",
                                    str11 = "sex",
                                    str12 = "sexo";


                                switch(true) {
                                    case (dataValue.toLowerCase().indexOf(str2) != -1 ||
                                        dataValue.toLowerCase().indexOf(str3) != -1 ):
                                        myTable.closest("div.col-sm-3").find("select").children("option[value='first_name']").prop("selected", true);
                                        str1 = true;
                                        break;
                                    case (dataValue.toLowerCase().indexOf(str4) != -1 ||
                                        dataValue.toLowerCase().indexOf(str5) != -1 ):
                                        myTable.closest("div.col-sm-3").find("select").children("option[value='last_name']").prop("selected", true);
                                        str1 = true;
                                        break;
                                    case (dataValue.toLowerCase().indexOf(str6) != -1 ||
                                        dataValue.toLowerCase().indexOf(str7) != -1 ):
                                        myTable.closest("div.col-sm-3").find("select").children("option[value='email']").prop("selected", true);
                                        str1 = true;
                                        break;
                                    case (dataValue.toLowerCase().indexOf("@") != -1 ):
                                        myTable.closest("div.col-sm-3").find("select").children("option[value='email']").prop("selected", true);
                                        break;
                                    case (dataValue.toLowerCase().indexOf(str8) != -1 ||
                                        dataValue.toLowerCase().indexOf(str9) != -1 ||
                                        dataValue.toLowerCase().indexOf(str10) != -1):
                                        myTable.closest("div.col-sm-3").find("select").children("option[value='phone']").prop("selected", true);
                                        str1 = true;
                                        break;
                                    case (dataValue.toLowerCase().indexOf(str11) != -1 ||
                                        dataValue.toLowerCase().indexOf(str12) != -1 ):
                                        myTable.closest("div.col-sm-3").find("select").children("option[value='sex']").prop("selected", true);
                                        str1 = true;
                                        break;
                                }
                            }
                        }
                    }
                    if (str1){
                        $("tr."+ k).remove();
                        totalClients -= 1;
                    }
                }
                $("#total-clients").prop("value", totalClients);
            };
            reader.readAsText(e.target.files.item(0));

        }

        return false;

    });

    $(document).on('click', '#add-new-csv', function () {
        $("#id_modal_body").removeClass("hidden");
        $("#form-csv-div").removeClass("hidden");
        $(this).addClass("hidden");
        $("#csv-next").addClass("hidden");
    });

    $(document).on('click', '#csv-next', function () {
        if ($("#ask-too").is(":checked")){
            $("#send-survey").removeClass("hidden");
            $("#id_modal_body").removeClass("hidden");
            $('#csvimport').addClass("hidden");
            $('#add-new-csv').addClass("hidden");
            $("#csv-next").addClass("hidden");
            $(".modal-title").html("Sucursal y servicios: ");
            $("#addClientModal").css("width","422px");
        } else {
            console.log("Not checked");
            onlyAddClient();
        }

    });

    $('#process-file').on('click', function () {
        if ($("#ask-too").is(":checked")){
            $("#send-survey").removeClass("hidden");
            $('#process-file-div').addClass("hidden");
            $('#form-csv-div').addClass("hidden");
        } else {
            console.log("Not checked");
            onlyAddClient();
        }
    });

    /*
    * Función para deshabilitar las opciones seleccionadas en los <select>*/
    $(document).on('change', 'select.field', function () {
        var $fields = $("select.field");
        $("option", $fields).prop("disabled", false);
        $fields.each(function() {
            var $select = $(this),
                $options = $fields.not($select).find('option'),
                selectedText = $select.children('option:selected').val();
            $options.each(function() {
                if($(this).val() == selectedText && $(this).val() != 'null'){
                    $(this).prop("disabled", true);
                }
            });
        });
    });
    //$fields.eq(0).trigger('change');

    /*
    * Función para limitar el numero de <checkbox> checked*/
    $(document).on('change', '.checkbox', function(e) {

        /*
        * Verificar que la opción seleccionada no tenga un valor 'null'*/
        if ($(this).is(":checked")){
            var selectedValue = $(this).closest("div.col-sm-3").find("select").children('option:selected').val();
            if(selectedValue=='null') {
                $(this).prop('checked', false);
            } else {
                $(this).closest("div.col-sm-3").find("select").prop('disabled', true);
            }
        } else {
            $(this).closest("div.col-sm-3").find("select").prop('disabled', false);
        }
        var num_checked = 0;

        $('.checkbox').each(function() {
            if ( $(this).prop('checked') ) num_checked++;
        });

        var max_checked = 9;

        /*
        * Verificar que se exceda el número máximo de elementos <checkbox> con
        * el atributo 'checked, true' y no deshabilite el select cuando se exceda*/
        if ( num_checked > max_checked ) {
            $(this).prop('checked', false);
            $(this).closest("div.col-sm-3").find("select").prop('disabled', false);
      }
    });

/*
* Obtener sucursales de la zona
* */
    $("select#zone-to").on('change', function (e) {
        e.preventDefault();

        var zone_filter = $(this).children('option:selected').val();
        var url = "/clients/zone/" + zone_filter;

        $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            data: 'nocache' + Math.random(),
            success: function (response) {
                var subOptions = '', busOptions = '', serOptions = '';
                $.each(response["subsidiaries"], function(idx,subsidiary) {
                    subOptions += '<option value="' + subsidiary.id + '">' +
                               subsidiary.name + '</option>'
                });

                $.each(response["business"], function(idx,business) {
                    busOptions += '<option value="' + business.id + '">' +
                               business.name + '</option>'
                });

                $.each(response["services"], function(idx,service) {
                    serOptions += '<option value="' + service.id + '">' +
                               service.name + '</option>'
                });

                $("select#subsidiary-to").html(subOptions);
                $("select#business-unit-to").html(busOptions);
                $("select#service-to").html(serOptions);
            },
            error: function (response) {
                alert('NO!')
            }
        });

    });

/*
* Obtener unidades de servicio de la sucursal
* */
    $("select#subsidiary-to").on('change', function (e) {
        e.preventDefault();

        var subsidiary_filter = $(this).children('option:selected').val();
        var url = "/clients/subsidiary/" + subsidiary_filter;

        $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            data: 'nocache' + Math.random(),
            success: function (response) {
                var busOptions = '', serOptions = '';

                $.each(response["business"], function(idx,business) {
                    busOptions += '<option value="' + business.id + '">' +
                               business.name + '</option>'
                });

                $.each(response["services"], function(idx,service) {
                    serOptions += '<option value="' + service.id + '">' +
                               service.name + '</option>'
                });

                $("select#business-unit-to").html(busOptions);
                $("select#service-to").html(serOptions);
            },
            error: function (response) {
                alert('NO!')
            }
        });

    });

/*
* Obtener servicios de la unidad de servicio
* */
    $("select#business-unit-to").on('change', function (e) {
        e.preventDefault();

        var business_filter = $(this).children('option:selected').val();
        var url = "/clients/business/" + business_filter;

        $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            data: 'nocache' + Math.random(),
            success: function (response) {
                var serOptions = '';

                $.each(response["services"], function(idx,service) {
                    serOptions += '<option value="' + service.id + '">' +
                               service.name + '</option>'
                });

                $("select#service-to").html(serOptions);
            },
            error: function (response) {
                alert('NO!')
            }
        });

    });

/*
* Agregar CLIENTES que sin enviar encuesta ni crear actividad
* */
function onlyAddClient(){
    var $dataTables = $("div.col-sm-3").find('table'),
        serialize = $("#add-csv-form").serializeArray(),
        url = "/clientes/csv/";

    console.log("No. de tablas: "+$dataTables.length);

    $dataTables.each(function(a) {
        var dataRowsClient = $(this).find("tr").length;

        for(var x=0; x<dataRowsClient; x++){
            var newClient = {};
            newClient.name = "newClient";
            newClient.value = [];

        $dataTables.each(function() {

            var $eachTable = $(this),
                $dataRows = $(this).find("tr."+x);

            if($eachTable.closest("div.col-sm-3").find("input.checkbox").is(":checked")){

                $dataRows.each(function() {
                    var client = {};

                    client.name = $eachTable.closest("div.col-sm-3").find("select").children('option:selected').val();
                    client.value = $(this).text();
                    newClient.value.push(JSON.stringify(client));
                });
            }

        });

            serialize.push(newClient);
        }
        return false;

    });
    console.log(serialize);

    $.ajax({
        type: 'POST',
        url: $('#add-csv-form').attr('action'),
        data: serialize,
        success: function () {
            setTimeout(function () {
                window.location.reload()
            }, 0);
        },
        error: function () {
            console.log('Fallo');
        }
    });
}

/*
* Agregar CLIENTES-ACTIVIDAD y enviarles una encuesta
* */
function addActivityClient(activity){
    var $dataTables = $("div.col-sm-3").find('table'),
        serialize = $("#add-csv-form").serializeArray(),
        url = "/clientes/csv/";

    console.log("No. de tablas: "+$dataTables.length);

    $dataTables.each(function(a) {
        var dataRowsClient = $(this).find("tr").length;

        for(var x=1; x<dataRowsClient; x++){
            var newClient = {};
            newClient.name = "newClient";
            newClient.value = [];

        $dataTables.each(function() {

            var $eachTable = $(this),
                $dataRows = $(this).find("tr."+x);

            if($eachTable.closest("div.col-sm-3").find("input.checkbox").is(":checked")){

                $dataRows.each(function() {
                    var client = {};

                    client.name = $eachTable.closest("div.col-sm-3").find("select").children('option:selected').val();
                    client.value = $(this).text();
                    newClient.value.push(JSON.stringify(client));
                });
            }

        });

            serialize.push(newClient);
        }
        serialize.push({name: 'id_activity', value: activity});
        return false;

    });
    console.log(serialize);

    $('#wait').show();
    $.ajax({
        type: 'POST',
        url: $('#add-csv-form').attr('action'),
        data: serialize,
        success: function () {

            $('#wait').hide();

            setTimeout(function () {
                clientsReady();
            }, 0);
        },
        error: function () {
            console.log('Fallo');
        }
    });
}

function clientsReady(){
    $(".modal-title").html("Clientes agregados correctamente");
    $("form#add-csv-form").addClass("hidden");
    setTimeout(function () {
        window.location.reload()
    }, 5000);
    $("div#client-success").html("<label class='h2'>"
        + "Listo!"
        + "</label><br>"
        + "En este momento se está enviando tu encuesta a tus clientes."
        +"<br><br>"
        + "<small class='text-success'>"
        +"<i class='icon-ok icon-7x'></i>"
        +"</small><br><br>"
        + "<a href='#' id='back-to-client-list' class='text-muted btn btn-success'>"
        +"<i class='icon-arrow-left text-white'></i>"
        +"Volver a mis clientes</a>");
}

//--- Función para confirmar envío de encuestas a los clientes ---//
    $(document).on('click', '#final-post', function (e) {
        e.preventDefault();

        var myZone = $("select#zone-to").children('option:selected').val(),
            mySubsidiary = $("select#subsidiary-to").children('option:selected'),
            myBusinessUnit = $("select#business-unit-to").children('option:selected').val(),
            myService = $("select#service-to").children('option:selected'),
            myTotalClients = $("#total-clients").val();

        var activity = [], zone = {}, subsidiary = {}, businessUnit = {}, service = {};

        zone.name = "id_zone";
        zone.value = myZone;
        activity.push(JSON.stringify(zone));

        subsidiary.name = "subsidiary";
        subsidiary.value = mySubsidiary.val();
        activity.push(JSON.stringify(subsidiary));

        businessUnit.name = "business_unit";
        businessUnit.value = myBusinessUnit;
        activity.push(JSON.stringify(businessUnit));

        service.name = "service";
        service.value = myService.val();
        activity.push(JSON.stringify(service));

        /*
        * Obtener encuesta
        * */
        var url = "/clients/survey/" + myBusinessUnit + "/"+ myService.val(),
            surveyName = "";

        $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            data: 'nocache' + Math.random(),
            success: function (response) {

                $.each(response["survey"], function(idx,survey) {
                    surveyName = survey.name;
                });
                bootbox.dialog({
                    message:
                            "Está a punto de enviar un correo a "+ myTotalClients +
                            " clientes con la " +
                            "encuesta '"+ surveyName + "', para el servicio " +
                            myService.text() + " de la sucursal "+mySubsidiary.text()+
                            ". <br><br> ¿Está seguro?",
                    title: "Comfirmación de envío",
                    buttons: {
                        success: {
                            label: "No",
                            className: "bg-danger btn-modal-xindex",
                            callback: function () {
                            }
                        },
                        main: {
                            label: "Si",
                            className: "bg-success btn-modal-xindex",
                            callback: function () {
                                addActivityClient(activity);
                            }
                        }
                    }
                });
            },
            error: function (response) {
                bootbox.dialog({
                    message:
                            "Este servicio no tiene encuestas disponibles para " +
                            "su envío.<br><br>¿Desea registrar los "+ myTotalClients +
                            " clientes del servicio " +
                            myService.text() + " de la sucursal "+mySubsidiary.text()+
                            "?",
                    title: "Comfirmación de registro",
                    buttons: {
                        success: {
                            label: "No",
                            className: "bg-danger btn-modal-xindex",
                            callback: function () {
                            }
                        },
                        main: {
                            label: "Si",
                            className: "bg-success btn-modal-xindex",
                            callback: function () {
                                addActivityClient(activity);
                            }
                        }
                    }
                });
            }
        });
    });

/*=============================================================================
* Agregar cliente manualmente
* */

$("#ask-too-manually").change(function(){

    if($(this).is(":checked")){
        $("#next-step-one").removeClass("hidden");
        $("#save-one").addClass("hidden");
    } else {
        $("#next-step-one").addClass("hidden");
        $("#save-one").removeClass("hidden");
    }
});

$("#next-step-one").click(function(){
    $("#first-side").addClass("hidden");
    $("#send-survey-one").removeClass("hidden");
});

/*
* Obtener sucursales de la zona
* */
    $("select#zone-to-one").on('change', function (e) {
        e.preventDefault();

        var zone_filter = $(this).children('option:selected').val();
        var url = "/clients/zone/" + zone_filter;

        $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            data: 'nocache' + Math.random(),
            success: function (response) {
                var subOptions = '', busOptions = '', serOptions = '';
                $.each(response["subsidiaries"], function(idx,subsidiary) {
                    subOptions += '<option value="' + subsidiary.id + '">' +
                               subsidiary.name + '</option>'
                });

                $.each(response["business"], function(idx,business) {
                    busOptions += '<option value="' + business.id + '">' +
                               business.name + '</option>'
                });

                $.each(response["services"], function(idx,service) {
                    serOptions += '<option value="' + service.id + '">' +
                               service.name + '</option>'
                });

                $("select#subsidiary-to-one").html(subOptions);
                $("select#business-unit-to-one").html(busOptions);
                $("select#service-to-one").html(serOptions);

                $("#id_client_subsidiary").val($("select#subsidiary-to-one").children("option:selected").val());
                $("#id_client_business").val($("select#business-unit-to-one").children("option:selected").val());
                $("#id_client_service").val($("select#service-to-one").children("option:selected").val());
            },
            error: function (response) {
                alert('NO!')
            }
        });

    });

/*
* Obtener unidades de servicio de la sucursal
* */
    $("select#subsidiary-to-one").on('change', function (e) {
        e.preventDefault();

        var subsidiary_filter = $(this).children('option:selected').val();
        var url = "/clients/subsidiary/" + subsidiary_filter;

        $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            data: 'nocache' + Math.random(),
            success: function (response) {
                var busOptions = '', serOptions = '';

                $.each(response["business"], function(idx,business) {
                    busOptions += '<option value="' + business.id + '">' +
                               business.name + '</option>'
                });

                $.each(response["services"], function(idx,service) {
                    serOptions += '<option value="' + service.id + '">' +
                               service.name + '</option>'
                });

                $("select#business-unit-to-one").html(busOptions);
                $("select#service-to-one").html(serOptions);

                $("#id_client_business").val($("select#business-unit-to-one").children("option:selected").val());
                $("#id_client_service").val($("select#service-to-one").children("option:selected").val());
            },
            error: function (response) {
                alert('NO!')
            }
        });

    });

/*
* Obtener servicios de la unidad de servicio
* */
    $("select#business-unit-to-one").on('change', function (e) {
        e.preventDefault();

        var business_filter = $(this).children('option:selected').val();
        var url = "/clients/business/" + business_filter;

        $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            data: 'nocache' + Math.random(),
            success: function (response) {
                var serOptions = '';

                $.each(response["services"], function(idx,service) {
                    serOptions += '<option value="' + service.id + '">' +
                               service.name + '</option>'
                });

                $("select#service-to-one").html(serOptions);

                $("#id_client_service").val($("select#service-to-one").children("option:selected").val());
            },
            error: function (response) {
                alert('NO!')
            }
        });

    });

    $("select#service-to-one").change(function(){
        $("#id_client_service").val($("select#service-to-one").children("option:selected").val());
    });

    $("#final-post-one").click(function(){
        $("form#add-client-form").submit();
    });