/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 2/10/13
 * Time: 03:49 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {
    $('#question_type_select').change(function () {
        $('.question').hide();
        var selected_value = this.options[this.selectedIndex].text
        selected_value = selected_value.replace(/ /g, '_').toLowerCase();

        console.log(selected_value);

        switch (selected_value) {
            case 'matriz':
                selected_value = 'matrix'
                break;
            case 'opcion_multiple':
                selected_value = 'multiple_choice'
                break;
            case 'falso_y_verdadero':
                selected_value = 'true_and_false'
                break;
            case 'pregunta_abierta':
                selected_value = 'open_question'
                break;
            case 'rango':
                selected_value = 'range'
                break;
            default:
                caption = "default";
        }

        $("." + selected_value).show();
        //console.log( this.value ); //for the index
        //console.log( this.options[this.selectedIndex].text ); //for text

        var current_question_id = $('#current-question').val();
        $('#' + current_question_id + ' div.optional-content').html('');

    });

    $('.dummy_option').focus(function () {
        var new_option_proto = '<div class="dynamic_inputs"><input type="text" maxlength="100" class="option_added" />';
        var remove_button = '<i class="delete_option icon-remove-sign" onclick="deleteOption(event);"></i></div>';
        new_option_proto += remove_button;

        $(this).before(new_option_proto);
        //$(this).prev('input').focus();
        //$(this).siblings('[type=text]').last().focus();
        var prev = $(this).prev();
        $(prev).find('[type=text]').last().focus();
    });


    //TODO: Fix this! I can't tell why is not working
    //for now I'm using the funcion deleteOption
    $('.delete_option').on('click', function (event) {
        event.preventDefault();
        //$(this).parent().remove();
    });

    $('#add_matrix').click(function (event) {
        event.preventDefault();

        var con = tinymce.get('tinymce-editor-new-question').getContent();
        var content = con.replace(/(<([^>]+)>)/ig, "");
        $('.question-title').val(content);

        var check = $("input[id=add-m-to-catalog]:checked").length;

        var question = get_question_object();
        question.title = $('.matrix_title').val();
        var rows = new Array();
        var cols = new Array();

        $(".matrix_cols .option_added").each(function () {
            cols.push({'label': $(this).val()});
        });

        $(".matrix_rows .option_added").each(function () {
            rows.push({'label': $(this).val()});
        });

        question.rows = rows;
        question.cols = cols;

        if (check == 1) {
            question.add_catalog = true;
        } else {
            question.add_catalog = false;
        }

        var survey_id = $('#survey_id').val()

        question.survey_id = survey_id

        manage_question_ajax(question);
    });

    $('#add_multiple_choice').click(function (event) {
        event.preventDefault();

        var con = tinymce.get('tinymce-editor-new-question').getContent();
        var content = con.replace(/(<([^>]+)>)/ig, "");
        $('.question-title').val(content);

        var check = $("input[id=add-mc-to-catalog]:checked").length;

        var question = get_question_object();
        question.title = $('.multiple_choice_title').val();

        var data = new Array();
        $(".multiple_choice_options_set .option_added").each(function () {
            console.log($(this).val());
            data.push({'label': $(this).val()});
        });
        question.options = data;

        if (check == 1) {
            question.add_catalog = true;
        } else {
            question.add_catalog = false;
        }

        var survey_id = $('#survey_id').val()

        question.survey_id = survey_id

        console.log(question)

        manage_question_ajax(question);
    });

    $('#add_open_question').click(function (event) {
        event.preventDefault();

        var con = tinymce.get('tinymce-editor-new-question').getContent();
        var content = con.replace(/(<([^>]+)>)/ig, "");
        $('.question-title').val(content);

        var check = $("input[id=add-o-to-catalog]:checked").length;

        var question = get_question_object();
        question.title = $('.open_question_title').val();

        if (check == 1) {
            question.add_catalog = true;
        } else {
            question.add_catalog = false;
        }

        var survey_id = $('#survey_id').val()

        question.survey_id = survey_id

        manage_question_ajax(question);
    });

    $('#add_range_question').click(function (event) {
        event.preventDefault();

        var con = tinymce.get('tinymce-editor-new-question').getContent();
        var content = con.replace(/(<([^>]+)>)/ig, "");
        $('.question-title').val(content);

        var check = $("input[id=add-r-to-catalog]:checked").length;

        var question = get_question_object();
        question.title = $('.range_title').val();
        var data = {};
        data.start_number = $(".range_field_set .start_number").val();
        data.start_label = $(".range_field_set .start_label").val();
        data.end_number = $(".range_field_set .end_number").val();
        data.end_label = $(".range_field_set .end_label").val();
        question.options = data;

        if (check == 1) {
            question.add_catalog = true;
        } else {
            question.add_catalog = false;
        }

        var survey_id = $('#survey_id').val()

        question.survey_id = survey_id

        manage_question_ajax(question);
    });

    $('#add_true_and_false_question').click(function (event) {
        event.preventDefault();

        var con = tinymce.get('tinymce-editor-new-question').getContent();
        var content = con.replace(/(<([^>]+)>)/ig, "");
        $('.question-title').val(content);

        var check = $("input[id=add-tf-to-catalog]:checked").length;

        var question = get_question_object();
        question.title = $('.true_and_false_title').val();

        if (check == 1) {
            question.add_catalog = true;
        } else {
            question.add_catalog = false;
        }

        var survey_id = $('#survey_id').val()

        question.survey_id = survey_id

        console.log(question);

        manage_question_ajax(question);
    });

    $(".remove_question").click(function (event) {
        event.preventDefault();
        var url = $(event.target).attr('href');
        delete_question(url);
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

    $('#edit_multiple_choice').click(function (event) {
        event.preventDefault();
        var question = {};
        question.id = $('#question_id').val();
        question.title = $('.multiple_choice_title').val();
        var options = new Array();

        $(".multiple_choice_options_set .dynamic_inputs").each(function () {
            options.push({
                'id': $(this).find(':input:hidden').first().val(),
                'label': $(this).find(':input:text').first().val()
            });
        });

        question.options = options;
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


    $('div.multiple_choice').on('keyup', '.option_added', function () {
        addQuestionOptions();
    });

    $('.multiple_choice_options_set').change(function () {
        addQuestionOptions();
    });


});

function get_question_object() {
    var question = {};
    question.type = $('#question_type_select').val();
    //question.type_name = $("#question_type_select option").children("option").is("selected").text;
    var type_name = $("#question_type_select option:selected").text().replace(/ /g, '_').toLowerCase();

    switch (type_name) {
            case 'matriz':
                type_name = 'matrix'
                break;
            case 'opcion_multiple':
                type_name = 'multiple_choice'
                break;
            case 'falso_y_verdadero':
                type_name = 'true_and_false'
                break;
            case 'pregunta_abierta':
                type_name = 'open_question'
                break;
            case 'rango':
                type_name = 'range'
                break;
            default:
                type_name = "default";
        }

    question.type_name = type_name
    return question;
};

function manage_question_ajax(question) {
    $.ajax({
        type: "POST",
        url: "/surveys/add/ajax/",
        'contentType': "application/json",
        dataType: "json",
        data: JSON.stringify(question),
        //data: question,
        success: function (data) {
            if (data.question_added) {
                var current_question = $('#current-question').val();
                $('#' + current_question + ' div.db_question_id').attr('id', data.question_id);
                saveSurvey();
            }
        },
        error: function (xhr, textStatus, errorThrown) {


            setTimeout(function () {
                            window.location.reload(true);
                        }, 0);


            //alert("Please report this error: " + errorThrown +
            //    " - Status :" + xhr.status +
            //    " - Message : " + xhr.responseText);
        }
    });
};

function delete_question(url) {
    if (!confirm("Are you sure?")) {
        return;
    }

    $.ajax({
        type: "POST",
        url: url,
        'contentType': "application/json",
        dataType: "json",
        data: "{}",
        success: function (data) {
            //TODO: Delete and make a proper AJAX request
            window.location.href = '';
        },
        error: function (xhr, textStatus, errorThrown) {

            setTimeout(function () {
                            window.location.reload(true);
                        }, 0);

            //alert("Please report this error: " + errorThrown +
            //    " - Status :" + xhr.status +
            //    " - Message : " + xhr.responseText);
        }
    });
};

function deleteOption(event) {
    $(event.target).parent().remove();
    addQuestionOptions();
}

function addQuestionOptions() {
    var current_question_id = $('#current-question').val();
    $('#' + current_question_id + ' div.optional-content').html('<div style="clear: both;"><ul class="question_options"></ul></div>');
    $('div.multiple_choice input.option_added').each(function () {
        var list_value = $(this).val();
        $('#' + current_question_id + ' ul.question_options').append(
            '<li>' + list_value + '</li>'
        );
    })
}


function saveSurvey() {

    var survey_configuration = {}
    var blocks = new Array();
    $('#survey-main-content div.row-block').each(function (index) {
        var questions = new Array();
        var selector = $(this).attr('id');
        var class_default = true;
        if($(this).hasClass('row-no-block')){
            class_default = false;
        }
        $('#' + selector + ' div.question-content').each(function (ind) {
            questions.push(
                {
                    'question_content_id': $(this).attr('id'),
                    'db_id': $(this).find('div.db_question_id').attr('id') | '',
                    'question_survey_id': $(this).find('div.question_id').text()
                }
            );
        });
        blocks.push(
            {
                'block_id': selector,
                'class_default': class_default,
                'block_title': $(this).find('header.block-title').text(),
                'block_description': $(this).find('div.panel-body').html(),
                'questions': questions
            }
        );

    });

    survey_configuration.blocks = blocks;

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
                window.location.href = '';
            }
            window.location.href = '';
        },
        error: function (xhr, textStatus, errorThrown) {

            setTimeout(function () {
                            window.location.reload(true);
                        }, 0);
            //alert("Please report this error: " + errorThrown +
            //    " - Status :" + xhr.status +
            //    " - Message : " + xhr.responseText);
        }
    });

}