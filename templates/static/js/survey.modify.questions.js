/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 8/10/13
 * Time: 12:38 PM
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function(){

    /*MULTIPLE CHOICE*/

    $(document).on('focus', '.option_added_u', function () {

        var current_question_updated = $('#current-question-updated').val();

        console.log('keyup event: '+current_question_updated);

        $('#' + current_question_updated + ' div.optional-content').html('<div style="clear: both;"><ul class="question_options"></ul></div>');
        $('div.multiple_choice_u input.option_added_u').each(function () {
            var list_value = $(this).val();
            $('#' + current_question_updated + ' ul.question_options').append(
                '<li>' + list_value + '</li>'
            );
        })
    });

    $(document).on('keyup', '.option_added_u', function () {

        var current_question_updated = $('#current-question-updated').val();

        console.log('keyup event: '+current_question_updated);

        $('#' + current_question_updated + ' div.optional-content').html('<div style="clear: both;"><ul class="question_options"></ul></div>');
        $('div.multiple_choice_u input.option_added_u').each(function () {
            var list_value = $(this).val();
            $('#' + current_question_updated + ' ul.question_options').append(
                '<li>' + list_value + '</li>'
            );
        })
    });

    $(document).on('change', '.multiple_choice_options_set_u', function () {

        var current_question_updated = $('#current-question-updated').val();

        console.log('Este es el id de la pregunta: '+current_question_updated);

        $('#' + current_question_updated + ' div.optional-content').html('<div style="clear: both;"><ul class="question_options"></ul></div>');
        $('div.multiple_choice_u input.option_added').each(function () {
            var list_value = $(this).val();
            $('#' + current_question_updated + ' ul.question_options').append(
                '<li>' + list_value + '</li>'
            );
        })
    });

    $(document).on('focus', '.dummy_option_u', function () {
        var new_option_proto = '<div class="dynamic_inputs input-close"><input type="text" maxlength="100" class="option_added_u form-control input-query" />';
        var remove_button = '<i class="delete_option icon-remove-sign" onclick="deleteOption(event);"></i></div>';
        new_option_proto += remove_button;

        $(this).before(new_option_proto);
        //$(this).prev('input').focus();
        //$(this).siblings('[type=text]').last().focus();
        var prev = $(this).prev();
        $(prev).find('[type=text]').last().focus();
    });


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
        alert('false and true');
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
                location.href = '';
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            //alert("Please report this error: " + errorThrown +
            //    " - Status :" + xhr.status +
            //    " - Message : " + xhr.responseText);
        }
    });
};