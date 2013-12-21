    $(function() {
        var availableTags = [],
            inputSearch = $("#search-client"),
            inputTags = $( "#tags" );

        inputSearch.keyup(function(){
            if ($(this).val().length > 3){
                var inputValue = inputSearch.val(),
                    url = "/callcenter/search/"+ inputValue,
                    business = $("select.callCenterBusiness").children("option:selected").val(),
                    service = $("select.callCenterService").children("option:selected").val();

                if (inputValue.length > 3){
                    $.ajax({
                        type: "GET",
                        url: url,
                        dataType: 'json',
                        data: 'nocache' + Math.random(),
                        success: function (response) {
                            availableTags = [];
                            $.each(response["client"], function(idx,client) {
                                availableTags.push({
                                    "value": client.id,
                                    "label": client.name
                                });
                            });
                            inputSearch.autocomplete({
                                source: availableTags,
                                select: function (event, ui) {
                                    inputSearch.val(ui.item.label);
                                    inputTags.val( ui.item.value );

                                    var url = "/callcenter/getsearch/" + inputTags.val() + "/" + business + "/" + service;
                                    if (url.indexOf('#') == 0) {
                                        $(url).modal('open');
                                    } else {
                                        $.get(url,function (data) {
                                            $('<div class="modal" id="cc-modal">' + data + '</div>').modal();
                                        }).success(function () {
                                                $('input:text:visible:first').focus();
                                            });
                                    }

                                    return false;
                                },
                                focus: function( event, ui ) {
                                    inputSearch.val( ui.item.label );
                                    return false;
                                }
                            });
                        },
                        error: function (response) {
                        }
                    });
                }
            }
        });
    });

    $("select#options-client").change(function(){
        var option = $("select#options-client").children("option:selected").val(),
            selectRandom = $("#get-survey"),
            selectSearch = $("#search-client");

        if (option=="1"){
            if(selectRandom.hasClass("hidden")){
                selectRandom.removeClass("hidden");
                selectSearch.addClass("hidden").val("");
            }
        } else if (option=="2"){
            if(selectSearch.hasClass("hidden")){
                selectSearch.removeClass("hidden");
                selectRandom.addClass("hidden");
            }
        } else if (option=="3"){
            var url = "/callcenter/add/";
            if (url.indexOf('#') == 0) {
                $(url).modal('open');
            } else {
                $.get(url,function (data) {
                    $('<div class="modal" id="cc-modal">' + data + '</div>').modal();
                }).success(function () {
                        $('input:text:visible:first').focus();
                    });
            }
        }
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
                alert('Get was not successfull');
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
                alert('Get was not successfull');
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
                alert('Get was not successfull');
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
            option = $("select#options-client").children("option:selected").val();

        $("#id_cc-business").val(business);
        $("#id_cc-service").val(service);

        if(option==1){
            var url = "/callcenter/random/" + business + "/" + service;
            if (url.indexOf('#') == 0) {
                $(url).modal('open');
            } else {
                $.get(url,function (data) {
                    $('<div class="modal" id="cc-modal">' + data + '</div>').modal();
                }).success(function () {
                        $('input:text:visible:first').focus();
                    });
            }
        }else if(option==2){
            alert("SEARCH");
        }else if(option==3){
            alert("NEW");
        }
    });