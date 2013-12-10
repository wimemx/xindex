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
                var csvStartValue=csvval[0].split(",");

                for(var a=0;a<csvStartValue.length;a++){

                    $("#csvRow").append("<div class='col-lg-3 padder-v'>" +
                            "<div class='row'>" +
                            "<div class='col-lg-9'><select class='form-control field'>" +
                            "<option value='null'>Sin asignar</option>" +
                            "<option value='first_name'>Nombre</option>" +
                            "<option value='last_name'>Apellido</option>" +
                            "<option value='sex'>Sexo</option>" +
                            "<option value='phone'>Teléfono</option>" +
                            "<option value='email'>Email</option>" +
                            "</select></div>" +

                            "<div class='ck-button btn col-lg-2'>" +
                               "<label>" +
                                  "<input type='checkbox' id='checkbox"+a+"' class='checkbox hidden'><span>OK</span>" +
                               "</label>" +
                            "</div>" +
                            "</div>" +

                            "<br>" +
                            "<table " +
                            "id='table"+a+"'" +
                            "class='table'" +
                            "style='margin: auto !important; width: 100%'></table>" +
                            "</div>");
                }

                for (var k=0; k<csvval.length-1; k++){
                    var csvvalue=csvval[k].split(","),
                        str1 = false;
                    for(var j=0;j<csvvalue.length;j++){
                        var dataValue=csvvalue[j],
                            myTable = $("#table"+j);

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
                                    myTable.closest("div.col-lg-3").find("select").children("option[value='first_name']").prop("selected", true);
                                    str1 = true;
                                    break;
                                case (dataValue.toLowerCase().indexOf(str4) != -1 ||
                                    dataValue.toLowerCase().indexOf(str5) != -1 ):
                                    myTable.closest("div.col-lg-3").find("select").children("option[value='last_name']").prop("selected", true);
                                    str1 = true;
                                    break;
                                case (dataValue.toLowerCase().indexOf(str6) != -1 ||
                                    dataValue.toLowerCase().indexOf(str7) != -1 ):
                                    myTable.closest("div.col-lg-3").find("select").children("option[value='email']").prop("selected", true);
                                    str1 = true;
                                    break;
                                case (dataValue.toLowerCase().indexOf("@") != -1 ):
                                    myTable.closest("div.col-lg-3").find("select").children("option[value='email']").prop("selected", true);
                                    break;
                                case (dataValue.toLowerCase().indexOf(str8) != -1 ||
                                    dataValue.toLowerCase().indexOf(str9) != -1 ||
                                    dataValue.toLowerCase().indexOf(str10) != -1):
                                    myTable.closest("div.col-lg-3").find("select").children("option[value='phone']").prop("selected", true);
                                    str1 = true;
                                    break;
                                case (dataValue.toLowerCase().indexOf(str11) != -1 ||
                                    dataValue.toLowerCase().indexOf(str12) != -1 ):
                                    myTable.closest("div.col-lg-3").find("select").children("option[value='sex']").prop("selected", true);
                                    str1 = true;
                                    break;
                            }
                        }
                    }
                    if (str1){
                        $("tr."+ k).remove();
                    }
                }
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
            var selectedValue = $(this).closest("div.col-lg-3").find("select").children('option:selected').val();
            if(selectedValue=='null') {
                $(this).prop('checked', false);
            } else {
                $(this).closest("div.col-lg-3").find("select").prop('disabled', true);
            }
        } else {
            $(this).closest("div.col-lg-3").find("select").prop('disabled', false);
        }
        var num_checked = 0;

        $('.checkbox').each(function() {
            if ( $(this).prop('checked') ) num_checked++;
        });

        var max_checked = 4;

        /*
        * Verificar que se exceda el número máximo de elementos <checkbox> con
        * el atributo 'checked, true' y no deshabilite el select cuando se exceda*/
        if ( num_checked > max_checked ) {
            $(this).prop('checked', false);
            $(this).closest("div.col-lg-3").find("select").prop('disabled', false);
      }
    });

/*
* POST final
* */
    $('#final-post').on('click', function () {
        var myZone = $("select#zone-to").children('option:selected').val(),
            mySubsidiary = $("select#subsidiary-to").children('option:selected').val(),
            myBusinessUnit = $("select#business-unit-to").children('option:selected').val(),
            myService = $("select#service-to").children('option:selected').val();

        var activity = [], zone = {}, subsidiary = {}, businessUnit = {}, service = {};

        zone.name = "id_zone";
        zone.value = myZone;
        activity.push(JSON.stringify(zone));

        subsidiary.name = "subsidiary";
        subsidiary.value = mySubsidiary;
        activity.push(JSON.stringify(subsidiary));

        businessUnit.name = "business_unit";
        businessUnit.value = myBusinessUnit;
        activity.push(JSON.stringify(businessUnit));

        service.name = "service";
        service.value = myService;
        activity.push(JSON.stringify(service));


        addActivityClient(activity);
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
    var $dataTables = $("div.col-lg-3").find('table'),
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

            if($eachTable.closest("div.col-lg-3").find("input.checkbox").is(":checked")){

                $dataRows.each(function() {
                    var client = {};

                    client.name = $eachTable.closest("div.col-lg-3").find("select").children('option:selected').val();
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
    var $dataTables = $("div.col-lg-3").find('table'),
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

            if($eachTable.closest("div.col-lg-3").find("input.checkbox").is(":checked")){

                $dataRows.each(function() {
                    var client = {};

                    client.name = $eachTable.closest("div.col-lg-3").find("select").children('option:selected').val();
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
                window.location.reload()
            }, 0);
        },
        error: function () {
            console.log('Fallo');
        }
    });
}