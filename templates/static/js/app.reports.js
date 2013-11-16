/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 30/10/13
 * Time: 10:29 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){

    //Get subsidiaries for zone
    $('#form_select_zone #id_zone').click(function(){
        var zone_id = $('#id_zone').val();
        $('#form_select_subsidiary input#id_zone').val(zone_id);
        $('#form_select_business_unit input#id_zone').val(zone_id);
        $('#form_select_service input#id_zone').val(zone_id);
        $('#form_select_moment input#id_zone').val(zone_id);
        $.ajax({
            url: $('#form_select_zone').attr('action'),
            method: 'POST',
            data: $('#form_select_zone').serialize(),
            dataType: 'Json',
            success: function(msg){
                if(msg.answer == true){
                    $('#form_select_subsidiary #id_subsidiary').html('');
                    $.each(msg.subsidiaries,function(index, object){
                        $('#form_select_subsidiary #id_subsidiary').append(
                            '<option value="'+object.subsidiary_id+'">'+object.subsidiary_name+'</option>'
                        );
                    })
                }
            },
            error: function(){
                console.log('');
            }
        });
    });

    //Get business units for subsidiary
    $('#form_select_subsidiary #id_subsidiary').click(function(){
        var subsidiary_id = $('#form_select_subsidiary input#id_zone').val();
        $('#form_select_business_unit input#id_subsidiary').val(subsidiary_id);
        $('#form_select_service input#id_subsidiary').val(subsidiary_id);
        $('#form_select_moment input#id_subsidiary').val(subsidiary_id)
        $.ajax({
            url: $('#form_select_subsidiary').attr('action'),
            method: 'POST',
            data: $('#form_select_subsidiary').serialize(),
            dataType: 'Json',
            success: function(msg){
                if(msg.answer == true){
                    $('#form_select_business_unit #id_business_unit').html('');
                    $.each(msg.business_units,function(index, object){
                        $('#form_select_business_unit #id_business_unit').append(
                            '<option value="'+object.business_unit_id+'">'+object.business_unit_name+'</option>'
                        );
                    })
                }
            },
            error: function(){
                console.log('');
            }
        });
    });

    //Get services for business unit
    $('#form_select_business_unit #id_business_unit').on('click', function(){
        var business_unit_id = $('#form_select_business_unit #id_business_unit').val();
        $('#form_select_service input#id_business_unit').val(business_unit_id);
        $('#form_select_moment input#id_business_unit').val(business_unit_id);
        $.ajax({
            url: $('#form_select_business_unit').attr('action'),
            method: 'POST',
            data: $('#form_select_business_unit').serialize(),
            dataType: 'Json',
            success: function(msg){
                if(msg.answer == true){
                    $('#form_select_service #id_service').html('');
                    $.each(msg.services,function(index, object){
                        $('#form_select_service #id_service').append(
                            '<option value="'+object.service_id+'">'+object.service_name+'</option>'
                        );
                    })
                }
            },
            error: function(){
                console.log('---Can´t get DA business unit---')
            }
        });
    });

    //Get moments for service
    $('#form_select_service #id_service').on('click', function(){
        var service_id = $('#form_select_service #id_service').val();
        $('#form_select_moment #id_service').val(service_id);
        $.ajax({
            url: $('#form_select_service').attr('action'),
            method: 'POST',
            data: $('#form_select_service').serialize(),
            dataType: 'Json',
            success: function(msg){
                if(msg.answer == true){
                    $('#id_moment').html('');
                    $.each(msg.moments,function(index, object){
                        $('#id_moment').append(
                            '<option value="'+object.moment_id+'">'+object.moment_name+'</option>'
                        );
                    })
                }
            },
            error: function(){
                console.log('');
            }
        });
    });

    $('#id_moment').on('change click', function(){
        $('#form_select_moment').submit();
    });

});