//// <------ Remove modal with close class ->
    $('.close').on('click', function (e) {
        e.preventDefault();
        $('div.modal').modal('hide');
        $('#ajaxModal').remove();
    });

/*
* Obtener sucursales de la zona
* */
    $("select.callCenterZone").change(function (e) {
        e.preventDefault();

        var zone_filter = $(this).children('option:selected').val();
        var url = "/callcenter/zone/" + zone_filter;

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

                $('select.callCenterZone option[value='+zone_filter+']').prop('selected',true);
                $("select.callCenterSubsidiary").html(subOptions);
                $("select.callCenterBusiness").html(busOptions);
                $("select.callCenterService").html(serOptions);
            },
            error: function (response) {
                alert('Zona inválida')
            }
        });

    });

/*
* Obtener unidades de servicio de la sucursal
* */
    $("select.callCenterSubsidiary").change(function (e) {
        e.preventDefault();

        var subsidiary_filter = $(this).children('option:selected').val();
        var url = "/callcenter/subsidiary/" + subsidiary_filter;

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

                $('select.callCenterSubsidiary option[value='+subsidiary_filter+']').prop('selected',true);
                $("select.callCenterBusiness").html(busOptions);
                $("select.callCenterService").html(serOptions);
            },
            error: function (response) {
                alert('Subsidiaria inválida')
            }
        });

    });

/*
* Obtener servicios de la unidad de servicio
* */
    $("select.callCenterBusiness").change(function (e) {
        e.preventDefault();

        var business_filter = $(this).children('option:selected').val();
        var url = "/callcenter/business/" + business_filter;

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

                $('select.callCenterBusiness option[value='+business_filter+']').prop('selected',true);
                $("select.callCenterService").html(serOptions);
            },
            error: function (response) {
                alert('Unidad de servicio inválida')
            }
        });

    });

/*
* Igualar servicios para la clase
* */
    $("select.callCenterService").change(function (e) {
        e.preventDefault();

        var service_filter = $(this).children('option:selected').val();
        $('select.callCenterService option[value='+service_filter+']').prop('selected',true);
    });

    $("#start-survey").click(function (){
            $("#before-starting").addClass("hidden");
            $("#starting-survey").removeClass("hidden");
        }
    );

    $("#get-survey").click(function (){
        var business = $("select.callCenterBusiness").children("option:selected").val(),
            service = $("select.callCenterService").children("option:selected").val(),
            option = $("select.options-client").children("option:selected").val();

        $("#id_cc-business").val(business);
        $("#id_cc-service").val(service);

        alert(option);

        if(option=="random"){

        }else if(option=="search"){

        }else if(option=="new"){

        }
    });