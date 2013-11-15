/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 15/11/13
 * Time: 09:47 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){

    $('#id_zone').on('change click', function(){
        $('#form_select_zone').submit();
    });

    $('.btn_send_subsidiary').click(function(){
        $(this).closest('form').submit();
    });

});