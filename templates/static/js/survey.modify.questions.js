/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 8/10/13
 * Time: 12:38 PM
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function(){

    /*Multiple Choice Question
    $(document).on('focus', '.option_added_u', function () {

        var current_question_updated = $('#current-question-updated').val();

        console.log('keyup event: '+current_question_updated);

        $('#' + current_question_updated + ' div.optional-content').html('<div style="clear: both;"><div class="question_options"></div></div>');
        $('div.multiple_choice_u input.option_added_u').each(function () {
            var list_value = $(this).val();
            $('#' + current_question_updated + ' div.question_options').append(
                '<input type="checkbox"/>&nbsp;&nbsp;' + list_value + '</br>'
            );
        })
    });*/

    /*Mostrar en tiempo real una nueva opción (Multiple Choice - Modificando)*/
    $(document).on('keyup', '.multiple_choice_options_set_u', function () {

        var current_question_updated = $('#current-question-updated').val();

        console.log('keyup event: '+current_question_updated);

        $('#' + current_question_updated + ' div.optional-content').html('<div style="clear: both;"><div class="question_options"></div></div>');
        $('div.multiple_choice_u input.option_added_u').each(function () {
            var list_value = $(this).val();
            $('#' + current_question_updated + ' div.question_options').append(
                '<input type="checkbox"/>&nbsp;&nbsp;' + list_value + '</br>'
            );
        })
    });

    $(document).on('change', '.multiple_choice_options_set_u', function () {

        var current_question_updated = $('#current-question-updated').val();

        console.log('Este es el id de la pregunta: '+current_question_updated);

        $('#' + current_question_updated + ' div.optional-content').html('<div style="clear: both;"><div class="question_options"></div></div>');
        $('div.multiple_choice_u input.option_added_u').each(function () {
            var list_value = $(this).val();
            $('#' + current_question_updated + ' div.question_options').append(
                '<input type="checkbox"/>&nbsp;&nbsp;' + list_value + '</br>'
            );
        })
    });

    /*Mostrar en tiempo real la matriz (Matrix - Modificando)*/
    $(document).on('keyup', '#question_type_1_form', function () {

        var current_question_updated = $('#current-question-updated').val();
        var counter_td = 0;
        var td_to_complete = '';
        var i;

        $('#' + current_question_updated + ' div.optional-content').html('<div style="clear: both;">' +
            '<table border=0 class="question_options">' +
                '<tr class="tr-cols" style="border-bottom: 1px solid #d3d3d3;">' +
                '<td style="border-right: 1px solid #d3d3d3;">' +
                '</td>' +
                '</tr>' +
            '</table>' +
            '</div>');

        $('div.matrix_cols_u input.option_added_u').each(function () {
            var col_value = $(this).val();
            $('#' + current_question_updated + ' tr.tr-cols').append(
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


        $('div.matrix_rows_u input.option_added_u').each(function () {
            var row_value = $(this).val();
            $('#' + current_question_updated + ' table.question_options').append(
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
    });

    /*Mostrar en tiempo real la escala del rango (Range - Modificando)*/
    $(document).on('keyup', '.range_field_set_u', (function () {

        var current_question_updated = $('#current-question-updated').val();
        var start_value = $('div.range_field_set_u input.start_number').val();
        var start_label = $('div.range_field_set_u input.start_label').val();
        var end_value = $('div.range_field_set_u input.end_number').val();
        var end_label = $('div.range_field_set_u input.end_label').val();
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

        $('#' + current_question_updated + ' div.optional-content').html('' +
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

        $('div#question_type_4 div.range_field_set_u input.start_number').each(function () {
            $('#' + current_question_updated + ' tr.tr-options ').append(
                circle_btn +

                '<td class="padder" ' +
                    'style="padding-bottom: 5px !important;' +
                    'padding-top: 5px !important;' +
                    'padding-left: 10px !important;' +
                    'padding-right: 10px !important;' +
                    'width: 100px !important;">' + end_label + '</td>'
            );
        })
    })
    );

    /*Crear una nueva opcion (Modificando)*/
    $(document).on('focus', '.dummy_option_u', function () {
        //var new_option_proto = '<div class="dynamic_inputs input-close" onclick="deleteOption(event);"><input type="text" maxlength="100" class="option_added_u form-control input-query" />';
        var new_option_proto = '<div class="dynamic_inputs input-close"><i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>';
        var remove_button = '<input type="text" maxlength="100" class="option_added_u input-query form-control"/></div>';
        new_option_proto += remove_button;

        $(this).before(new_option_proto);
        //$(this).prev('input').focus();
        //$(this).siblings('[type=text]').last().focus();
        var prev = $(this).prev();
        $(prev).find('[type=text]').last().focus();
    });

    /*Guardar*/
    $(document).on('click', '#edit_multiple_choice', function (event) {
        event.preventDefault();
        var question = {};
        var current_question_updated = $('#current-question-updated').val();
        question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
        question.title = $('.question_title_updated').val();

        var options = new Array();

        $(".multiple_choice_options_set_u .dynamic_inputs").each(function () {
            options.push({
                'id': $(this).find(':input:hidden').first().val(),
                'label': $(this).find(':input:text').first().val()
            });
        });

        question.options = options;

        var moment_id = $('#update_moment_association').val();

        if (moment_id == 'default'){
            question.moment_id = false;
        } else {
            question.moment_id = moment_id;
            console.log('El momento es: '+moment_id)
        }

        var attribute_id = $('#update_attribute_association').val();

        if (attribute_id == 'default'){
            question.attribute_id = false;
        } else {
            question.attribute_id = attribute_id;
            console.log('El attributo es: '+attribute_id);
        }


        manage_question_ajax_edited(question);
    });
    /*ENDS MULTIPLE CHOICE*/

    /* ---/Edit
    * ---/Question
    * --/MATRIX
    * */
    $(document).on('click', '#edit_matrix', function (event) {
        event.preventDefault();
        var question = {};
        var current_question_updated = $('#current-question-updated').val();
        question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
        question.title = $('.question_title_updated').val();

        var rows = new Array();
        var cols = new Array();

        $(".matrix_cols_u .dynamic_inputs").each(function () {
            cols.push({
                'id': $(this).find(':input:hidden').first().val(),
                'label': $(this).find(':input:text').first().val()
            });
        });

         $(".matrix_rows_u .dynamic_inputs").each(function () {
            rows.push({
                'id': $(this).find(':input:hidden').first().val(),
                'label': $(this).find(':input:text').first().val()
            });
        });

        question.cols = cols;
        question.rows = rows;

        var moment_id = $('#update_moment_association').val();

        if (moment_id == 'default'){
            question.moment_id = false;
        } else {
            question.moment_id = moment_id;
            console.log('El momento es: '+moment_id)
        }

        var attribute_id = $('#update_attribute_association').val();

        if (attribute_id == 'default'){
            question.attribute_id = false;
        } else {
            question.attribute_id = attribute_id;
            console.log('El attributo es: '+attribute_id);
        }


        manage_question_ajax_edited(question);
    });

    /* ---/Edit
    * ---/Question
    * --/RANGE
    * */
    $(document).on('click', '#edit_range_question', function (event) {
        event.preventDefault();
        var question = {};
        var current_question_updated = $('#current-question-updated').val();
        question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
        question.title = $('.question_title_updated').val();

        var data = {};

        data.start_number = $(".range_field_set_u .start_number").val();
        data.start_label = $(".range_field_set_u .start_label").val();
        data.end_number = $(".range_field_set_u .end_number").val();
        data.end_label = $(".range_field_set_u .end_label").val();

        question.options = data;

        var moment_id = $('#update_moment_association').val();

        if (moment_id == 'default'){
            question.moment_id = false;
        } else {
            question.moment_id = moment_id;
            console.log('El momento es: '+moment_id)
        }

        var attribute_id = $('#update_attribute_association').val();

        if (attribute_id == 'default'){
            question.attribute_id = false;
        } else {
            question.attribute_id = attribute_id;
            console.log('El attributo es: '+attribute_id);
        }

        manage_question_ajax_edited(question);
    });

    /* ---/Edit
    * ---/Question
    * --/Open Question
    * */
    $(document).on('click', '#edit_open_question', function (event) {
        event.preventDefault();
        var question = {};
        var current_question_updated = $('#current-question-updated').val();
        question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
        question.title = $('.question_title_updated').val();

        var moment_id = $('#update_moment_association').val();

        if (moment_id == 'default'){
            question.moment_id = false;
        } else {
            question.moment_id = moment_id;
            console.log('El momento es: '+moment_id)
        }

        var attribute_id = $('#update_attribute_association').val();

        if (attribute_id == 'default'){
            question.attribute_id = false;
        } else {
            question.attribute_id = attribute_id;
            console.log('El attributo es: '+attribute_id);
        }

        manage_question_ajax_edited(question);
    });

    /* ---/Edit
    * ---/Question
    * --/True and False
    * */
    $(document).on('click', '#edit_true_and_false_question', function (event) {
        event.preventDefault();
        var question = {};
        var current_question_updated = $('#current-question-updated').val();
        question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
        question.title = $('.question_title_updated').val();

        var moment_id = $('#update_moment_association').val();

        if (moment_id == 'default'){
            question.moment_id = false;
        } else {
            question.moment_id = moment_id;
            console.log('El momento es: '+moment_id)
        }

        var attribute_id = $('#update_attribute_association').val();

        if (attribute_id == 'default'){
            question.attribute_id = false;
        } else {
            question.attribute_id = attribute_id;
            console.log('El attributo es: '+attribute_id);
        }

        manage_question_ajax_edited(question);
    });


    //Button to save all questions
    $('#save_updated_question').on('click', function(){
        var cadena = $('#question_type_select:disabled option:selected').text();
        cadena = (cadena.replace(/\s/g,'_')).toLowerCase();
        switch(cadena) {
            case 'range':
                update_range();
                break;
            case 'false_and_true':
                update_false_and_true();
                break;
            case 'matrix':
                update_matrix();
                break;
            case 'multiple_choice':
                update_multiple_choice();
                break;
            case 'open_question':
                update_open();
                break;
        }
    });

});

/* ---/Manage
* ---/Question
* --/AjaxEdited
* */

function manage_question_ajax_edited(question) {
    $.ajax({
        type: "POST",
        url: "/surveys/"+question.id+"/edit/ajax/",
        'contentType': "application/json",
        dataType: "json",
        data: JSON.stringify(question),
        //data: question,
        success: function (data) {
            console.log(data);
            if (data.updated) {
                enumerateQuestionBlocks();
                enumerateQuestions();
                saveSurvey();
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            //alert("Please report this error: " + errorThrown +
            //    " - Status :" + xhr.status +
            //    " - Message : " + xhr.responseText);
        }
    });
};

function update_multiple_choice(){
    var question = {};
    var current_question_updated = $('#current-question-updated').val();
    question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
    question.title = $('.question_title_updated').val();

    var options = new Array();

    $(".multiple_choice_options_set_u .dynamic_inputs").each(function () {
        options.push({
            'id': $(this).find(':input:hidden').first().val(),
            'label': $(this).find(':input:text').first().val()
        });
    });

    question.options = options;

    var moment_id = $('#update_moment_association').val();

    if (moment_id == 'default'){
        question.moment_id = false;
    } else {
        question.moment_id = moment_id;
        console.log('El momento es: '+moment_id)
    }

    var attribute_id = $('#update_attribute_association').val();

    if (attribute_id == 'default'){
        question.attribute_id = false;
    } else {
        question.attribute_id = attribute_id;
        console.log('El attributo es: '+attribute_id);
    }


    manage_question_ajax_edited(question);
}

function update_range(){
    var question = {};
    var current_question_updated = $('#current-question-updated').val();
    question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
    question.title = $('.question_title_updated').val();

    var data = {};

    data.start_number = $(".range_field_set_u .start_number").val();
    data.start_label = $(".range_field_set_u .start_label").val();
    data.end_number = $(".range_field_set_u .end_number").val();
    data.end_label = $(".range_field_set_u .end_label").val();

    question.options = data;

    var moment_id = $('#update_moment_association').val();

    if (moment_id == 'default'){
        question.moment_id = false;
    } else {
        question.moment_id = moment_id;
        console.log('El momento es: '+moment_id)
    }

    var attribute_id = $('#update_attribute_association').val();

    if (attribute_id == 'default'){
        question.attribute_id = false;
    } else {
        question.attribute_id = attribute_id;
        console.log('El attributo es: '+attribute_id);
    }

    manage_question_ajax_edited(question);
}

function update_open(){
    var question = {};
    var current_question_updated = $('#current-question-updated').val();
    question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
    question.title = $('.question_title_updated').val();

    var moment_id = $('#update_moment_association').val();

    if (moment_id == 'default'){
        question.moment_id = false;
    } else {
        question.moment_id = moment_id;
        console.log('El momento es: '+moment_id)
    }

    var attribute_id = $('#update_attribute_association').val();

    if (attribute_id == 'default'){
        question.attribute_id = false;
    } else {
        question.attribute_id = attribute_id;
        console.log('El attributo es: '+attribute_id);
    }

    manage_question_ajax_edited(question);
}

function update_matrix(){
    var question = {};
    var current_question_updated = $('#current-question-updated').val();
    question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
    question.title = $('.question_title_updated').val();

    var rows = new Array();
    var cols = new Array();

    $(".matrix_cols_u .dynamic_inputs").each(function () {
        cols.push({
            'id': $(this).find(':input:hidden').first().val(),
            'label': $(this).find(':input:text').first().val()
        });
    });

    $(".matrix_rows_u .dynamic_inputs").each(function () {
        rows.push({
            'id': $(this).find(':input:hidden').first().val(),
            'label': $(this).find(':input:text').first().val()
        });
    });

    question.cols = cols;
    question.rows = rows;

    var moment_id = $('#update_moment_association').val();

    if (moment_id == 'default'){
        question.moment_id = false;
    } else {
        question.moment_id = moment_id;
        console.log('El momento es: '+moment_id)
    }

    var attribute_id = $('#update_attribute_association').val();

    if (attribute_id == 'default'){
        question.attribute_id = false;
    } else {
        question.attribute_id = attribute_id;
        console.log('El attributo es: '+attribute_id);
    }


    manage_question_ajax_edited(question);
}

function update_false_and_true(){
    var question = {};
    var current_question_updated = $('#current-question-updated').val();
    question.id = $('#'+current_question_updated+' div.db_question_id').attr('id');
    question.title = $('.question_title_updated').val();

    var moment_id = $('#update_moment_association').val();

    if (moment_id == 'default'){
        question.moment_id = false;
    } else {
        question.moment_id = moment_id;
        console.log('El momento es: '+moment_id)
    }

    var attribute_id = $('#update_attribute_association').val();

    if (attribute_id == 'default'){
        question.attribute_id = false;
    } else {
        question.attribute_id = attribute_id;
        console.log('El attributo es: '+attribute_id);
    }

    manage_question_ajax_edited(question);
}