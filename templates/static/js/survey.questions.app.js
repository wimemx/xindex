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
function addQuestionOptions(from) {
    var current_question_id = $('#current-question').val();

    if (from=='multiple'){

        $('#' + current_question_id + ' div.optional-content').html('<div style="clear: both;"><div class="question_options"></div></div>');

        $('div.multiple_choice input.option_added').each(function () {
            var list_value = $(this).val();
            $('#' + current_question_id + ' div.question_options').append(
                '<input type="checkbox"/>&nbsp;&nbsp;' + list_value + '</br>'
            );
        })
    } else if (from=='matrix'){

        var counter_td = 0;
        var td_to_complete = '';

        $('#' + current_question_id + ' div.optional-content').html('<div style="clear: both;">' +
            '<table border=0 class="question_options">' +
                '<tr class="tr-cols" style="border-bottom: 1px solid #d3d3d3;">' +
                '<td style="border-right: 1px solid #d3d3d3;">' +
                '</td>' +
                '</tr>' +
            '</table>' +
            '</div>');

        $('div.matrix div.matrix_cols input.option_added').each(function () {
            var col_value = $(this).val();
            $('#' + current_question_id + ' tr.tr-cols').append(
                '<td class="padder">' + col_value + '</td>'
            );
            counter_td ++;
        });

        for (i=0; i < parseInt(counter_td); i ++){

            td_to_complete += '<td style=" text-align: center !important;' +
                'border-bottom: 1px solid #d3d3d3;">' +
                '<label class="radio-custom" style="margin-left: 0px !important;">' +
                '<input type="radio">' +
                '<i class="icon-circle-blank"></i>' +
                '</label>' +
                '</td>';
        }


        $('div.matrix div.matrix_rows input.option_added').each(function () {
            var row_value = $(this).val();
            $('#' + current_question_id + ' table.question_options').append(
                '<tr style="border-bottom: 1px solid #d3d3d3;">' +
                    '<td style="' +
                        'border-right: 1px solid #d3d3d3;' +
                        'padding-bottom: 5px !important;' +
                        'padding-top: 5px !important;' +
                        'padding-left: 10px !important;' +
                        'padding-right: 10px !important;' +
                    '">' + row_value + '</td>' +
                    td_to_complete +
                '</tr>'
            );
        });
    } else if (from=='range'){
        var start_value = $('.start_number').val();
        var start_label = $('.start_label').val();
        var end_value = $('.end_number').val();
        var end_label = $('.end_label').val();
        var i;
        var header_value = '<td></td>';
        var circle_btn = '';

        for (i=parseInt(start_value); i <= parseInt(end_value); i ++){

            header_value += '<td  style=" text-align: center !important;">' +
               '<small>' +

               i +

               '</small>' +
               '</td>';

            circle_btn += '<td  style=" text-align: center !important;">'+

                '<label class="radio-custom" style="margin-left: 0px !important;">' +
                '<input type="radio">' +
                '<i class="icon-circle-blank"></i>' +
                '</label>' +
               '</td>';
        }

        $('#' + current_question_id + ' div.optional-content').html('' +
            '<div class="col-sm-12" ' +
                '' +
                'style="padding-left: 35px !important; ' +
                'padding-right: 35px !important;' +
                'padding-top: 10px;' +
                'padding-bottom: 20px;' +
                'clear: both;">' +
            '<table border=0 class="question_options">' +
                 '<tr>'+ header_value +'</tr>' +
                '<tr class="tr-options">' +
                '<td class="padder" ' +
                    'style="padding-bottom: 5px !important;' +
                    'padding-top: 5px !important;' +
                    'padding-left: 10px !important;' +
                    'padding-right: 10px !important;' +
                    'width: 100px !important;">' + start_label + '</td>' +
                '</tr>' +
            '</table>' +
            '</div>');

        $('div#question_type_4 div.range_field_set input.start_number').each(function () {
            $('#' + current_question_id + ' tr.tr-options ').append(
                circle_btn +

                '<td class="padder" ' +
                    'style="padding-bottom: 5px !important;' +
                    'padding-top: 5px !important;' +
                    'padding-left: 10px !important;' +
                    'padding-right: 10px !important;' +
                    'width: 100px !important;">' + end_label + '</td>'
            );
        })
    } else if (from=='open_question'){

        $('#' + current_question_id + ' div.optional-content').html('' +
            '<div class="col-sm-12" style="padding-left: 35px !important;' +
            'padding-right: 35px !important;' +
            'padding-top: 10px;' +
            'padding-bottom: 20px">' +
            '<textarea class="form-control" name="comment" cols="30" rows="5"  ' +
            'maxlength="100"' +
            'placeholder="Vista previa de pregunta abierta"></textarea>' +
            '</div>'
        );
    } else if (from=='true_and_false'){

        $('#' + current_question_id + ' div.optional-content').html('' +
            '<div class="col-sm-12" style="padding-left: 35px !important;">' +
            '<div class="radio">' +
            '<br> <label class="radio-custom">' +
            '<input type="radio">' +
            '<i class="icon-circle-blank"></i>' +
            'Verdadero' +
            '</label> <br>' +
            '<label class="radio-custom">' +
            '<input type="radio">' +
            '<i class="icon-circle-blank"></i>' +
            'Falso' +
            '</label>' +
            '</div>' +
            '</div>'
        );
    }
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

        //cargar la vista previa de los valores por default para 'range'
        if (selected_value == 'range'){
            addQuestionOptions('range');
        }

        if (selected_value == 'open_question'){
            addQuestionOptions('open_question');
        }

        if (selected_value == 'true_and_false'){
            addQuestionOptions('true_and_false');
        }
    });


    <!-- multiple choice functions -->

    //input to add another option before this
    $('.dummy_option').focus(function () {
        var new_option_proto = '<div class="dynamic_inputs input-close"><i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>';
        var remove_button = '<input type="text" maxlength="100" class="option_added input-query form-control"/></div>';

        new_option_proto += remove_button;

        $(this).before(new_option_proto);
        var prev = $(this).prev();
        $(prev).find('[type=text]').last().focus();
    });

    //detect key up event and make preview in left side
    $('div.multiple_choice').on('keyup', '.option_added', function () {
        addQuestionOptions('multiple');
    });

    $('div.matrix').on('keyup', '.option_added', function () {
        addQuestionOptions('matrix');
    });

    //detect change event in content from dynamic inputs and make preview
    $('.multiple_choice_options_set').change(function () {
        addQuestionOptions('multiple');
    });

    $('#question_type_4').on('keyup', (function () {
        addQuestionOptions('range');
    })
    );

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


    //button to create a new question inside of block
    $(document).on('click', 'a.add-question-to-block', function () {
        $('#main-configuration-panel').addClass('hidden');
        $('#questions-block-configuration-panel').addClass('hidden');
        $('#add-question-option-panel').removeClass('hidden');

        $(this).closest('footer').fadeOut(400);

        var before = $(this)[0];

        var new_question_block = '';

        var parent_block = '';

        $('<div class="wrapper question-content active-question" style="display: table; min-width: 100%; min-heigth: 50px;"><div class="question_id" style="float:left;"></div><div class="question-text" style="float: left; margin-left: 5px; display: table;"></div><div class="optional-content" style="margin-top: 15px;"></div><div class="db_question_id"></div></div>').insertBefore($(this).parent());

        /*Find question id*/
        $('#survey-main-content div.question-content').each(function (index) {
            $(this).attr('id', 'question-' + (index + 1));
            $(this).children('div.question_id').text(index + 1 + '.- ');
        })
        /*end*/

    });

//flag
    //button to show the editor for a new question
    $('a.btn-create-new-question').on('click', function () {
        $('#survey-main-content div.question-content').each(function (index) {
            $(this).attr('id', 'question-' + (index + 1));
            $(this).children('div.question_id').text(index + 1 + '.- ');
            if ($(this).hasClass('active-question')) {

                var question_id = $(this).attr('id');
                $(this).children('div.question-text').text('Este es el texto de la pregunta');

                $('#current-question').val(question_id);

                $('#new_question_title').attr('placeholder', 'Este es el texto de la pregunta');

                $('#add-new-question-configuration-panel').removeClass('hidden');
                $('#add-question-option-panel').addClass('hidden');

            }
        })

        addQuestionOptions('range');
    });


    //function to create a new question within block
    $('#add-question').on('click', function () {

        $('#main-configuration-panel').addClass('hidden');
        $('#questions-block-configuration-panel').addClass('hidden');
        $('#add-question-option-panel').removeClass('hidden');

        $('div.default-buttons').fadeOut(300);

        //Determine next block id

        var n = $('#survey-main-content div.row-block').length;

        $('#survey-main-content div.row-block').each(function (index) {
            $(this).find('section.question-block').removeClass('selected-block');
        });

        var new_block_id = 'block-' + (n + 1);

        var new_questions_block_content = '<div class="row row-block row-no-block animated fadeIn" id="' + new_block_id + '">' +
            '<div class="col-lg-12">' +
            '<section class="padder padder-v question-block selected-block">' +
            /*
             '<div class="wrapper question-blocks-content">' +
             '</div>' +*/
            '<div class="wrapper question-content active-question" style="display: table; min-width: 100%; min-heigth: 50px;"><div class="question_id" style="float:left;"></div><div class="question-text" style="float: left; margin-left: 5px; display: table;">Texto de la pregunta</div><div class="optional-content" style="margin-top: 15px;"></div><div class="db_question_id"></div></div>' +
            '</section>' +
            '</div>' +
            '</div>';

        $('#survey-main-content').append(new_questions_block_content);
        enumerateQuestionBlocks();
        enumerateQuestions();

        var block_selected_id = $('#survey-main-content').find('section.selected-block').find('div.question_id').attr('id')

        $('#current-question-block').val(block_selected_id);
    });


});