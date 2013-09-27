$(document).ready(function () {
    $('#question_type_select').change(function () {
        $('.question').hide();
        var selected_value = this.options[this.selectedIndex].text
        selected_value = selected_value.replace(/ /g, '_').toLowerCase();
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
        manage_question_ajax(question);
    });

    $('#add_multiple_choice').click(function (event) {
        event.preventDefault();

        var con = tinymce.get('tinymce-editor-new-question').getContent();
        var content = con.replace(/(<([^>]+)>)/ig, "");
        $('.question-title').val(content);

        var check = $( "input[id=add-mc-to-catalog]:checked" ).length;

        var question = get_question_object();
        question.title = $('.multiple_choice_title').val();

        var data = new Array();
        $(".multiple_choice_options_set .option_added").each(function () {
            console.log($(this).val());
            data.push({'label': $(this).val()});
        });
        question.options = data;

        if(check == 1){
            question.add_catalog = true;
        } else {
            question.add_catalog = false;
        }

        manage_question_ajax(question);
    });

    $('#add_open_question').click(function (event) {
        event.preventDefault();

        var question = get_question_object();
        question.title = $('.open_question_title').val();
        manage_question_ajax(question);
    });

    $('#add_range_question').click(function (event) {
        event.preventDefault();

        var question = get_question_object();
        question.title = $('.range_title').val();
        var data = {};
        data.start_number = $(".range_field_set .start_number").val();
        data.start_label = $(".range_field_set .start_label").val();
        data.end_number = $(".range_field_set .end_number").val();
        data.end_label = $(".range_field_set .end_label").val();
        question.options = data;
        manage_question_ajax(question);
    });

    $('#add_true_and_false_question').click(function (event) {
        event.preventDefault();

        var question = get_question_object();
        question.title = $('.true_and_false_title').val();
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
    question.type_name = $("#question_type_select option:selected").text().replace(/ /g, '_').toLowerCase();
    return question;
};

function manage_question_ajax(question) {
    $.ajax({
        type: "POST",
        url: "/questions/add/ajax/",
        'contentType': "application/json",
        dataType: "json",
        data: JSON.stringify(question),
        //data: question,
        success: function (data) {

            alert("Operation complete! The question id is: "+data.question_id);
            //TODO: Delete and make a proper AJAX request
            window.location.href = '';
        },
        error: function (xhr, textStatus, errorThrown) {
            alert("Please report this error: " + errorThrown +
                " - Status :" + xhr.status +
                " - Message : " + xhr.responseText);
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
            alert("Please report this error: " + errorThrown +
                " - Status :" + xhr.status +
                " - Message : " + xhr.responseText);
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