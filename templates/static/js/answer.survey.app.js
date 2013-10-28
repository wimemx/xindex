/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 25/10/13
 * Time: 04:02 PM
 * To change this template use File | Settings | File Templates.
 */

var answers_json = {};
        answers_json.question = [];

        //fields of question json
        var question_id,
            question_type,
            option_id,
            option_value = false;

$(document).ready(function(){
    $('#btn_send_data').on('click', function(e){
        e.preventDefault();

        $('div.question-content').each(function(){
            question_id = $(this).find('div.db_question_id').attr('id');
            //TODO: create function to validate if there is an option selected
            if($(this).hasClass('Range')){
                question_type = 'range_question';
                option_id = $('input[name='+question_id+']:checked', this).attr('id');
                option_value = false;

                addObjectQuestion(question_id, question_type, option_id, option_value);
            } else if($(this).hasClass('False')){
                question_type = 'false_question';
                option_id = $('input[name='+question_id+']:checked', this).attr('id');
                option_value = false;
                addObjectQuestion(question_id, question_type, option_id, option_value);
            } else if($(this).hasClass('Matrix')){
                question_type = 'matrix_question';
                //TODO: fix this, ¿How matrix?
                $(this).find('.sub_question').each(function(){
                    question_id = $(this).find('input.sub_question_id').val();
                    question_type = 'multiple_choice';
                    option_id = $(this).find('input.sub_question_option:checked').val();
                    option_value = false;
                    addObjectQuestion(question_id, question_type, option_id, option_value);
                });
                option_value = false;
            } else if($(this).hasClass('Multiple')){
                question_type = 'multiple_choice_question';
                option_id = $('input:checked', this).attr('id');
                option_value = false;
                addObjectQuestion(question_id, question_type, option_id, option_value);
            } else if($(this).hasClass('Open')){

                question_type = 'open_question';
                if($(this).find('input.not_apply_option').is(':checked')){
                    option_id = $(this).find('input.not_apply_option').attr('id');
                    option_value = false;
                } else {
                    option_id = $(this).find('textarea.open_question_option').attr('id');
                    option_value = $(this).find('textarea.open_question_option').val();
                }
                addObjectQuestion(question_id, question_type, option_id, option_value);
            }
        });

        send_answers_ajax(answers_json);
    });

    //Select just one option of groups of checkboxes
    $("input:checkbox").click(function() {
        if ($(this).is(":checked")) {
            var group = "input:checkbox[name='" + $(this).attr("name") + "']";
            $(group).prop("checked", false);
            $(this).closest('div.options-content').find('i').each(function(){
                $(this).removeClass('checked');
            })
            $(this).prop("checked", true);
            $(this).closest('label.checkbox-custom').find('i').addClass('checked');
        } else {
            $(this).prop("checked", false);
            $(this).closest('label.checkbox-custom').find('i').removeClass('checked');
        }
    });

    //When text area has activity the 'not apply option' is disabled
    $('textarea.open_question_option').on('keyup change', function(){
        $(this).closest('div.options-content').find('input:checkbox').prop('checked', false);
        $(this).closest('div.options-content').find('i').removeClass('checked');
    });

    //When input 'not apply option' is checked the text area value is empty
    $('input.open_question_option').on('click', function(){
        $(this).closest('div.options-content').find('textarea.open_question_option').val('');
        return true;
    });
})

function send_answers_ajax(answers_json) {
    $.ajax({
        type: "POST",
        url: "/surveys/save_answers/",
        'contentType': "application/json",
        dataType: "json",
        data: JSON.stringify(answers_json),
        success: function (data) {
            if(data.response){
                console.log('La encuesta ha sido guardada con exito');
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log('¡Houston, we have a problem!');
        }
    });
};

function addObjectQuestion(question_id, question_type, option_id, option_value){
    answers_json.question.push(
        {
            'question_id': question_id,
            'question_type': question_type,
            'option_id': option_id,
            'option_value': option_value
        }
    );
};