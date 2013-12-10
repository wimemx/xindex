/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 15/11/13
 * Time: 09:46 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){

    //Get subsidiaries for zone
    $('#form_select_zone #id_zone').click(function(){
        var zone_id = $('#id_zone').val();
        $('#form_select_subsidiary input#id_zone').val(zone_id);
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
                } else {
                    $('select#id_subsidiary').attr('disabled', true);
                    $('select#id_subsidiary').html('<option value="invalid">Sin sucursales</option>');
                }
            },
            error: function(){
                console.log('');
            }
        });
    });

    $('#id_subsidiary').on('change click', function(){
        $('#form_select_subsidiary').submit();
    });

    $('.btn_send_business_unit').click(function(){
        $(this).closest('form').submit();
    });

});