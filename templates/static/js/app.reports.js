/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 30/10/13
 * Time: 10:29 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){

    //Filtrado a nivel Business Unit
    $('#id_select_businessUnit').on('click', function(){
        var businessUnit_id = $('#id_select_businessUnit').val();
        var dataForm = $('#form_select_businessUnit');

        $('#id_businessUnit').val(businessUnit_id);
        $.ajax({
            url: dataForm.attr('action'),
            method: 'POST',
            data: dataForm.serialize(),
            dataType: 'Json',
            success: function(msg){
                if(msg.answer == true){
                    $('#id_select_service').html('');
                    $.each(msg.services,function(index, object){
                        $('#id_select_service').append(
                            '<option value="'+object.service_id+'">'
                                +
                                object.service_name
                                +
                                '</option>'
                        );
                    })
                }
            },
            error: function(){
                console.log('---Can´t get DA business unit---')
            }
        });
    });

    //Control to set the moments of current selected service
    $('#id_select_service').on('click', function(){
        var service_id = $('#id_select_service').val();
        $('#id_service').val(service_id);
        $.ajax({
            url: $('#form_select_service').attr('action'),
            method: 'POST',
            data: $('#form_select_service').serialize(),
            dataType: 'Json',
            success: function(msg){
                if(msg.answer == true){
                    $('#id_select_touch_point').html('');
                    $.each(msg.moments,function(index, object){
                        $('#id_select_touch_point').append(
                            '<option value="'+object.moment_id+'">'+object.moment_name+'</option>'
                        );
                    })
                }
            },
            error: function(){
                console.log('')
            }
        });
    });

    $('#id_select_touch_point').on('change', function(){
        $('#form_select_moment').submit();
    });

});