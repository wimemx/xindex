/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 14/11/13
 * Time: 04:02 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){

    //Get subsidiaries for zone
    $('#form_select_zone #id_zone').click(function(){
        var zone_id = $('#id_zone').val();
        $('#form_select_subsidiary input#id_zone').val(zone_id);
        $('#form_select_business_unit input#id_zone').val(zone_id);
        $.ajax({
            url: $('#form_select_zone').attr('action'),
            method: 'POST',
            data: $('#form_select_zone').serialize(),
            dataType: 'Json',
            success: function(msg){
                if(msg.answer == true){
                    $('#form_select_subsidiary #id_subsidiary').html('');
                    var coincidences = 0;
                    $.each(msg.subsidiaries,function(index, object){
                        if(object.subsidiary_id == 'all'){
                            coincidences += 1;
                        }
                        $('#form_select_subsidiary #id_subsidiary').append(
                            '<option value="'+object.subsidiary_id+'">'+object.subsidiary_name+'</option>'
                        );
                    });
                    if(coincidences == 0){
                        $('#form_select_subsidiary #id_subsidiary').append(
                            '<option value="all">Todas</option>'
                        );
                    }
                    $('select#id_business_unit').attr('disabled', 'disabled');
                    $('select#id_business_unit').html(
                        '<option value="default">Seleccione una sucursal</option>'
                    )
                } else {
                    $('#form_select_subsidiary #id_subsidiary').html('<option value="invalid">Sin sucursales</option>');
                    $('#form_select_subsidiary #id_subsidiary').attr('disabled', true);
                }
            },
            error: function(){
                console.log('');
            }
        });
    });

    //Get business units for subsidiary
    $('#form_select_subsidiary #id_subsidiary').click(function(){
        var subsidiary_id = $('#form_select_subsidiary #id_subsidiary').val();
        $('#form_select_business_unit input#id_subsidiary').val(subsidiary_id);
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
                    });
                    $('select#id_business_unit').attr('disabled', false);
                } else {
                    $('select#id_business_unit').html('<option value="invalid">No hay unidades de servicio</option>');
                    $('select#id_business_unit').attr('disabled', true);
                }
            },
            error: function(){
                console.log('');
            }
        });
    });

    $('#id_business_unit').on('change click', function(){
        $('#form_select_business_unit').submit();
    });

    $('.btn_send_service').click(function(){
        $(this).closest('form').submit();
    });

});