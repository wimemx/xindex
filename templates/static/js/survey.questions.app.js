/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 11/10/13
 * Time: 01:41 PM
 * Functions to manage question features in surveys module
 */

//function to add a matrix question
function addMatrix() {
    var content = $('#new_question_title').val();
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

    var survey_id = $('#survey_id').val();

    question.survey_id = survey_id;

    manage_question_ajax(question);
}

//function to add multiple choice question
function addMultipleChoice() {
    var content = $('#new_question_title').val();
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

    var survey_id = $('#survey_id').val();

    question.survey_id = survey_id;

    manage_question_ajax(question);
}

//function to add open question
function addOpenQuestion() {
    var content = $('#new_question_title').val();
    $('.question-title').val(content);

    var check = $("input[id=add-o-to-catalog]:checked").length;

    var question = get_question_object();
    question.title = $('.open_question_title').val();

    if (check == 1) {
        question.add_catalog = true;
    } else {
        question.add_catalog = false;
    }

    var survey_id = $('#survey_id').val();

    question.survey_id = survey_id;

    manage_question_ajax(question);
}

//function to add range question
function addRangeQuestion() {
    var content = $('#new_question_title').val();
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
}

//function to add true and false question
function addTrueAndFalseQuestion() {
    var content = $('#new_question_title').val();
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

    manage_question_ajax(question);
}

/**
 * function to create and return the object question with type,
 * also with moment and attribute ids
 * @returns {{question}}
 */
function get_question_object() {
    var question = {};
    question.type = $('#question_type_select').val();
    var type_name = $("#question_type_select option:selected").text().replace(/ /g, '_').toLowerCase();
    //Determine the question type based on selected text
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

    var moment_id = $('#add_moment_association').val();

    if (moment_id == 'default') {
        question.moment_id = false;
    } else {
        question.moment_id = moment_id;
    }

    var attribute_id = $('#add_attribute_association').val();

    if (attribute_id == 'default') {
        question.attribute_id = false;
    } else {
        question.attribute_id = attribute_id;
    }
    return question;
};


//function to add options to multiple option and matrix questions
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

/**
 * ajax function to add questions
 * @param question object
 */
function manage_question_ajax(question) {
    $.ajax({
        type: "POST",
        url: "/surveys/add/ajax/",
        'contentType': "application/json",
        dataType: "json",
        data: JSON.stringify(question),
        success: function (data) {
            if (data.question_added) {
                var current_question = $('#current-question').val();
                $('#' + current_question + ' div.db_question_id').attr('id', data.question_id);
                saveSurvey();
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log('Ha ocurrido un error en la petición');
        }
    });
};


/**
 * function to insert questions blocks in DOM
 */
function insertQuestionsBlock() {
    $('#main-configuration-panel').addClass('hidden');
    $('#questions-block-configuration-panel').removeClass('hidden');

    $('div.default-buttons').fadeOut(300);

    //Determine next block id

    var n = $('#survey-main-content div.row-block').length;

    $('#survey-main-content div.row-block').each(function (index) {
        $(this).find('section.question-block').removeClass('selected-block');
    });

    var new_block_id = 'block-' + (n + 1);

    var new_questions_block_content = '<div class="row row-block animated fadeIn" id="' + new_block_id + '">' +
        '<div class="col-lg-12">' +
        '<section class="padder padder-v question-block selected-block">' +
        '<div class="panel-body">' +
        '<div>' +
        '<header class="block-title">' +
        'Este es el nombre del bloque de preguntas' +
        '</header>' +
        '<small class="block-description">' +
        '<p>' +
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.' +
        '</p>' +
        '</small>' +
        '</div>' +
        '</div>' +
        '<footer class="wrapper text-center">' +
        '<a class="btn btn-info wrapper add-question-to-block">' +
        '<i class="icon-plus-sign-alt"></i>' +
        'Da click aquí para añadir una pregunta' +
        '</a>' +
        '</footer>' +
        '</section>' +
        '</div>' +
        '</div>';

    $('#survey-main-content').append(new_questions_block_content);

    var block_selected_id = $('#survey-main-content').find('section.selected-block').closest('div.row').attr('id');

    $('#current-question-block').val(block_selected_id);

    tinymce.get('tinymce-editor').setContent(
        '<div>' +
            '<header class="">' +
            'Este es el nombre del bloque de preguntas' +
            '</header>' +
            '<small class="">' +
            '<p>' +
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.' +
            '</p>' +
            '</small>' +
            '</div>'
    );
}



$(document).ready(function () {

    //button to add new block of questions
    $('#add-block-questions').on('click', function () {
        insertQuestionsBlock();
    });

    //event to show different question forms depending on select
    $('#question_type_select').change(function () {
        $('.question').hide();
        var selected_value = this.options[this.selectedIndex].text;
        selected_value = selected_value.replace(/ /g, '_').toLowerCase();
        switch (selected_value) {
            case 'matriz':
                selected_value = 'matrix';
                break;
            case 'opcion_multiple':
                selected_value = 'multiple_choice';
                break;
            case 'falso_y_verdadero':
                selected_value = 'true_and_false';
                break;
            case 'pregunta_abierta':
                selected_value = 'open_question';
                break;
            case 'rango':
                selected_value = 'range';
                break;
            default:
                selected_value = "default";
                console.log('Question types are not correct');
                break;
        }

        $("." + selected_value).show();
        var current_question_id = $('#current-question').val();
        $('#' + current_question_id + ' div.optional-content').html('');

    });


    <!-- multiple choice functions -->

    //input to add another option before this
    $('.dummy_option').focus(function () {
        var new_option_proto = '<div class="dynamic_inputs input-close" onclick="deleteOption(event);" ><input type="text" maxlength="100" class="option_added input-query form-control" />';
        var remove_button = '';
        new_option_proto += remove_button;

        $(this).before(new_option_proto);
        var prev = $(this).prev();
        $(prev).find('[type=text]').last().focus();
    });

    //detect key up event and make preview in left side
    $('div.multiple_choice').on('keyup', '.option_added', function () {
        addQuestionOptions();
    });

    //detect change event in content from dynamic inputs and make preview
    $('.multiple_choice_options_set').change(function () {
        addQuestionOptions();
    });

    <!-- ends multiple choice functions-->

    //function to change the text of the new question
    $('#new_question_title').on('keyup keypress change', function (e) {
        var content = $(this).val();
        var current_question = $('#current-question').val();
        $('#' + current_question + ' div.question-text').html('');
        $('#' + current_question + ' div.question-text').html(content);

        $('.question-title').val(content);

    })


    //button to save questions detecting which one
    $('#save_new_question').on('click', function () {
        var question_type_name = $('#question_type_select option:selected').text();
        switch (question_type_name) {
            case 'Opcion Multiple':
                //call the add multiple choice question function
                addMultipleChoice();
                break;
            case 'Rango':
                //call the add range question function
                addRangeQuestion();
                break;
            case 'Pregunta Abierta':
                //call the add open question function
                addOpenQuestion();
                break;
            case 'Matriz':
                //call the add matrix question function
                addMatrix();
                break;
            case 'Falso y Verdadero':
                //call the true and false question function
                addTrueAndFalseQuestion();
                break;
            default:
                break;
        }
    });


})