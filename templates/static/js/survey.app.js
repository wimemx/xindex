/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 20/09/13
 * Time: 09:44 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {

    $("#survey_name").keyup(function () {
        if ($(this).val().length >= 1) {
            $('#save-link').removeClass('hidden');
        } else {
            $('#save-link').addClass('hidden');
        }
    });

    $('a.step-one-next').on('click', function(){
        $.ajax({
            type: 'POST',
            url: '/survey/save/2/',
            data: $('#new-survey-form').serialize(),
            success: function(msg){

            },
            error: function(msg_error){

            }
        });
    });


})