/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 30/10/13
 * Time: 10:29 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){
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

    $('#')

    $('#id_select_touch_point').on('change', function(){
        $('#form_select_moment').submit();
    });

});