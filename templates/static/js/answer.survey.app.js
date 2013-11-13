/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 25/10/13
 * Time: 04:02 PM
 * To change this template use File | Settings | File Templates.
 */



$(document).ready(function(){
    $('#btn_send_data').on('click', function(e){
        e.preventDefault();
        var answers_json = {};
        answers_json.client_id =$('#id_client').val();
        answers_json.survey_id =$('#id_survey').val();
        answers_json.question = [];

        //fields of question json
        var question_id,
            question_type,
            option_id,
            option_value = false,
            errors = 0;
        $('div.question-content').each(function(){
            question_id = $(this).find('div.db_question_id').attr('id');
            //TODO: create function to validate if there is an option selected
            if($(this).hasClass('Range')){
                question_type = 'range_question';
                option_id = $('input[name='+question_id+']:checked', this).attr('id');
                option_value = false;

                var parent_container = $(this);
                var validation = validateQuestions(parent_container, option_id, question_type);
                if(validation != true){
                    answers_json.question.push(
                        {
                            'question_id': question_id,
                            'question_type': question_type,
                            'option_id': option_id,
                            'option_value': option_value,
                            'client_id': $('#id_client').val()
                        }
                    );
                    hideErrorContainer(parent_container);
                } else{
                    errors ++;
                }
            } else if($(this).hasClass('False')){
                question_type = 'false_question';
                option_id = $('input[name='+question_id+']:checked', this).attr('id');
                option_value = false;

                var parent_container = $(this);
                var validation = validateQuestions(parent_container, option_id, question_type);
                if(validation != true){
                    answers_json.question.push(
                        {
                            'question_id': question_id,
                            'question_type': question_type,
                            'option_id': option_id,
                            'option_value': option_value,
                            'client_id': $('#id_client').val()
                        }
                    );
                    hideErrorContainer(parent_container);
                } else {
                    errors ++;
                }

            } else if($(this).hasClass('Matrix')){
                question_type = 'matrix_question';
                //TODO: fix this, ¿How matrix?
                var sub_in_matrix =$(this).find('.sub_question').length;
                $(this).find('.sub_question').each(function(){
                    question_id = $(this).find('input.sub_question_id').val();
                    question_type = 'multiple_choice';
                    option_id = $(this).find('input.sub_question_option:checked').val();
                    option_value = false;

                    var parent_container = $(this).closest('div.question-content');
                    var validation = validateQuestions(parent_container, option_id, 'matrix_question');
                    if(validation != true){
                        answers_json.question.push(
                            {
                                'question_id': question_id,
                                'question_type': question_type,
                                'option_id': option_id,
                                'option_value': option_value,
                                'client_id': $('#id_client').val()
                            }
                        );
                        sub_in_matrix --;
                    } else {
                        errors ++;
                    }
                    if(sub_in_matrix === 0){
                        hideErrorContainer(parent_container);
                    }
                });
                option_value = false;
            } else if($(this).hasClass('Multiple')){
                question_type = 'multiple_choice_question';
                option_id = $('input:checked', this).attr('id');
                option_value = false;

                var parent_container = $(this);
                var validation = validateQuestions(parent_container, option_id, question_type);
                if(validation != true){
                    answers_json.question.push(
                        {
                            'question_id': question_id,
                            'question_type': question_type,
                            'option_id': option_id,
                            'option_value': option_value,
                            'client_id': $('#id_client').val()
                        }
                    );
                    hideErrorContainer(parent_container);
                } else {
                    errors ++;
                }

            } else if($(this).hasClass('Open')){

                question_type = 'open_question';
                if($(this).find('input.not_apply_option').is(':checked')){
                    option_id = $(this).find('input.not_apply_option').attr('id');
                    option_value = false;
                } else {
                    option_id = $(this).find('textarea.open_question_option').attr('id');
                    option_value = $(this).find('textarea.open_question_option').val();
                }

                var parent_container = $(this);
                var validation = validateQuestions(parent_container, option_id, question_type);
                if(validation != true){
                    answers_json.question.push(
                        {
                            'question_id': question_id,
                            'question_type': question_type,
                            'option_id': option_id,
                            'option_value': option_value,
                            'client_id': $('#id_client').val()
                        }
                    );
                    hideErrorContainer(parent_container);
                } else {
                    errors ++;
                }

            }
        });
        if(errors > 0){
            $('div.error_question').each(function(){
                if($(this).hasClass('active')){
                    $(this).slideDown(300);
                }
            });
        } else {
            send_answers_ajax(answers_json);
        }

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
                location.reload();
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log('¡Houston, we have a problem!');
        }
    });
};

/*
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
*/

function validateQuestions(question_container, option_id, question_type){
    var html_error = 'Seleccione una opci&oacute;n';
    switch(question_type){
        case 'open_question':
            if(option_id == undefined){
                var content = question_container.find('textarea.open_question_option').val();
                //Check if answer could be empty
            }
            break;
        case 'matrix_question':
            html_error = 'Seleccione una opcion por cada rengl&oacute;n';
            break;
    }
    if(option_id == undefined){
        var error_container = question_container.find('div.error_question');
        error_container.addClass('active');
        error_container.html(html_error);
        return true;
    }
}

function hideErrorContainer(parent_container){
    parent_container.find('div.error_question').slideUp(300);
    parent_container.find('div.error_question').removeClass('active');
}