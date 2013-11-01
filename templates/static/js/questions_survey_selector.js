/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 2/10/13
 * Time: 03:49 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {

    $("#survey-main-content ul").sortable();
    /*
    var helper = '<div><a class="btn btn-success">Hello</a></div>';


    $('#pane1, #pane2').sortable(
        {
            connectWith: ".connected",
            helper: 'clone'
            --
            helper: function() {
                return $('<div>hsjkdhskdhaksdja</div>');
            }--
        }
    );
    */
    //TODO: Fix this! I can't tell why is not working
    //for now I'm using the funcion deleteOption
    $('.delete_option').on('click', function (event) {
        event.preventDefault();
        //$(this).parent().remove();
    });

    $('#edit_matrix').click(function (event) {
        event.preventDefault();
        var question = {};
        question.id = $('#question_id').val();
        question.title = $('.matrix_title').val();
        var rows = new Array();
        var cols = new Array();

        $(".matrix_cols .dynamic_inputs").each(function () {
            cols.push({
                'id': $(this).find(':input:hidden').first().val(),
                'label': $(this).find(':input:text').first().val()
            });
        });

        $(".matrix_rows .dynamic_inputs").each(function () {
            rows.push({
                'id': $(this).find(':input:hidden').first().val(),
                'label': $(this).find(':input:text').first().val()
            });
        });

        question.rows = rows;
        question.cols = cols;
        manage_question_ajax(question);
    });


    $('#edit_open_question').click(function (event) {
        event.preventDefault();
        var question = {};
        question.id = $('#question_id').val();
        question.title = $('.open_question_title').val();
        manage_question_ajax(question);
    });

    $('#edit_true_and_false_question').click(function (event) {
        event.preventDefault();
        var question = {};
        question.id = $('#question_id').val();
        question.title = $('.true_and_false_title').val();
        manage_question_ajax(question);
    });

    $('#edit_range_question').click(function (event) {
        event.preventDefault();
        var question = {};
        question.id = $('#question_id').val();
        question.title = $('.range_title').val();

        var data = {};
        data.start_number = $(".range_field_set .start_number").val();
        data.start_label = $(".range_field_set .start_label").val();
        data.end_number = $(".range_field_set .end_number").val();
        data.end_label = $(".range_field_set .end_label").val();
        question.options = data;

        console.log(question);
        manage_question_ajax(question);
    });

});

function deleteOption(event) {
        $(event.target).parent().remove();
        addQuestionOptions();
}

function saveSurvey() {

    var survey_configuration = {}
    var blocks = new Array();
    $('#survey-main-content div.row-block').each(function (index) {
        var questions = new Array();
        var selector = $(this).attr('id');
        var style = $(this).find('section.question-block').attr('style');
        var class_default = true;

        var block_type = 'questions-block';

        if($(this).hasClass('text-block')){
            block_type = 'text-block';
        } else if($(this).hasClass('question-block')){
            block_type = 'question-block';
        }

        if ($(this).hasClass('row-no-block')) {
            class_default = false;
        }

        if($(this).find('input.block_moment_associated_id').hasClass('true')){
            console.log('recovering moment id');
            var moment_associated_id = $(this).find('input.block_moment_associated_id').val();
            console.log('moment id: '+moment_associated_id);
        } else {
            var moment_associated_id = false;
        }

        $('#' + selector + ' div.question-content').each(function (ind) {
            questions.push(
                {
                    'question_content_id': $(this).attr('id'),
                    'db_id': $(this).find('div.db_question_id').attr('id') | '',
                    'question_survey_id': $(this).find('div.question_id').text(),
                    'question_style': $(this).attr('style')
                }
            );
        });
        blocks.push(
            {
                'block_id': selector,
                'class_default': class_default,
                'block_title': $(this).find('header.block-title').text(),
                'block_description': $(this).find('div.panel-body').html(),
                'questions': questions,
                'style': style,
                'block_type': block_type,
                'block_moment_associated_id': moment_associated_id
            }
        );

    });
    /*
    $('#survey-main-content div.introduction_panel').each(function(ind){
        text_blocks.push(
            {
                'block_id': $(this).attr('id'),
                'block_content': $(this).find('div.panel-body').html()
            }
        )
    })
    */
    survey_configuration.blocks = blocks;

    if($('#survey_has_blocks_style').val() == 'True'){
        survey_configuration.blocks_style = $('#survey_blocks_style').val();
    } else if($('#survey_has_blocks_style').val() == 'False'){
        if($('#apply_design_to_all_blocks').is(':checked')){
            survey_configuration.blocks_style = setStyleToBlock();
            $('#survey_blocks_style').val(setStyleToBlock());
        }
    }

    if($('#survey_has_question_style').val() == 'True'){
        survey_configuration.questions_style = $('#survey_question_style').val();
    } else if($('#survey_has_question_style').val() == 'False'){
        if($('#apply_design_to_all_questions').is(':checked')){
            survey_configuration.questions_style = setStyleToQuestion();
            $('#survey_question_style').val(setStyleToQuestion());
        }
    }

    survey_configuration.block_border_color = rgb2hex($('#survey_global_content').css('border-color'));
    survey_configuration.block_border_style = $('#survey_global_content').css('border-style');
    survey_configuration.block_border_width = $('#survey_global_content').css('border-width');
    survey_configuration.block_background_color = $('#survey_global_content').css('background-color');
    survey_configuration.block_box_shadow = $('#survey_global_content').css('box-shadow');

    var survey_id = $('#survey_id').val();

    $.ajax({
        type: "POST",
        url: "/surveys/save_conf/" + survey_id,
        'contentType': "application/json",
        dataType: "json",
        data: JSON.stringify(survey_configuration),
        //data: question,
        success: function (data) {
            if (data.answer) {
                //window.location.href = '';
                showDefaultButtons();
                set_current_operation_inactive();
                console.log('The survey has been saved!')
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log('!Houston, we have a problem¡');
        }
    });

}