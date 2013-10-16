/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 20/09/13
 * Time: 09:44 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {

    /*Funciones para edicion de bloque*/
    $('a.intro_actions').click(function(){
        if($(this).hasClass('update_intro')){
            $('#main-configuration-panel').addClass('hidden');
            $('#questions-block-configuration-panel').addClass('hidden');
            $('#add-add-question-option-panel').addClass('hidden');
            $('#add-add-new-question-configuration-panel').addClass('hidden');
            $('#update-update-question-configuration-panel').addClass('hidden');
            $('#update-survey-block').removeClass('hidden');

            var current_text_block_id = $(this).closest('section.panel').attr('id');
            $('#current-text-block-updated').val(current_text_block_id);

            var current_text_block_content = $('#'+current_text_block_id+' div.panel-body').html();

            tinymce.get('tinymce-editor-update-block').setContent(current_text_block_content);

        } else if($(this).hasClass('remove_intro')){

        }
    });
    /*Terminan funciones para edicion de bloque*/



    $('#save_global_configuration').click(function () {
        enumerateQuestionBlocks();
        enumerateQuestions();
        saveSurvey();

    });

    $('.question_actions .actions').hide();
    $('.intro_block_actions').hide();

    $('#survey_introduction_block').hover(function () {
        $(this).find('div.intro_block_actions').fadeIn(100);
    }, function () {
        $(this).find('div.intro_block_actions').fadeOut(100);
    });


    $('div.block_actions').hide();

    $('#save-survey-from-step3').on('click', function (e) {
        e.preventDefault();
        saveSurvey();
    });

    $("#id_name").keyup(function () {
        if ($(this).val().length >= 1) {
            $('#save-link').removeClass('hidden');
        } else {
            $('#save-link').addClass('hidden');
        }
    });

    $('#step-one-next').on('click', function (e) {
        e.preventDefault();
        if ($('#id_name').val().length > 1) {
            $.ajax({
                url: '/surveys/save/next/2/empty',
                type: 'POST',
                data: $('#new-survey-form').serialize(),
                dataType: 'Json',
                success: function (msg) {
                    if (msg.save) {
                        window.location.href = msg.url;
                    }
                },
                error: function (msg_error) {
                    alert(msg_error.error);
                }
            });
        } else {
            return false;
        }

    });

    $('#step-one-next-header').on('click', function (e) {
        e.preventDefault();
        if ($('#id_name').val().length > 1) {
            $.ajax({
                url: '/surveys/save/next/2/empty',
                type: 'POST',
                data: $('#new-survey-form').serialize(),
                dataType: 'Json',
                success: function (msg) {
                    if (msg.save) {
                        window.location.href = msg.url;
                    }
                },
                error: function (msg_error) {
                    alert(msg_error.error);
                }
            });
        } else {
            return false;
        }

    });


    $('#save-link').on('click', function (e) {
        e.preventDefault();
        $('#form-edit-survey').submit();

    });







    //funciones para editar bloques

    $('div.row-block').hover(function () {
        $(this).find('div.block_actions').fadeIn(100);
    }, function () {
        $(this).find('div.block_actions').fadeOut(100);
    });


    $(document).on('click', 'a.update_block', function () {

        var parent = $(this).closest('div.row-block');

        $('#main-configuration-panel').addClass('hidden');
        $('#add-question-option-panel').addClass('hidden');
        $('#add-new-question-configuration-panel').addClass('hidden');
        $('#questions-block-configuration-panel').removeClass('hidden');

        $('#survey-main-content div.row-block').each(function () {
            $(this).find('section.question-block').removeClass('selected-block');
            $(this).find('div.question-content').removeClass('active-question');
        });

        parent.find('section.question-block').addClass('selected-block');

        var block_title = parent.find('header.block-title').text();
        var block_description = parent.find('div.panel-body').html();
        $('#current-question-block').val(parent.attr('id'));
        tinymce.get('tinymce-editor').setContent(block_title + block_description);


        if (parent.hasClass('row-no-block')) {
            parent.find('section.question-block').removeClass('selected-block');
            parent.find('div.question-content').addClass('active-question');
            $('#questions-block-configuration-panel').removeClass('hidden');
        }

    });


    $('a.actions_block').on('click', function (e) {
        e.preventDefault();
        var action = $(this).attr('id')
        if ($(this).hasClass("remove_block")) {
            var self = $(this);

            bootbox.dialog({
                message: "¿Esta seguro de eliminar el bloque y todas sus preguntas?",
                title: "Eliminar bloque de preguntas",
                buttons: {
                    success: {
                        label: "Cancelar",
                        className: "btn-white",
                        callback: function () {
                            return true;
                        }
                    },
                    main: {
                        label: "Eliminar",
                        className: "btn-twitter",
                        callback: function () {
                            var block_id = self.closest('div.row-block').attr('id');
                            var question_ids = new Array();
                            $('#' + block_id + ' div.db_question_id').each(function (index) {
                                question_ids.push(
                                    {
                                        'question_id': $(this).attr('id')
                                    }
                                );
                            });

                            $.ajax({
                                type: 'POST',
                                url: '/surveys/delete_questions/',
                                data: {
                                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                                    ids: JSON.stringify(question_ids),
                                    survey_id: $('#survey_id').val()
                                },
                                dataType: 'JSON',
                                success: function (msg) {
                                    //alert(msg);
                                    if (msg.success) {
                                        $(self).closest('div.row-block').slideUp('slow', function () {
                                            $(this).remove();
                                            enumerateQuestionBlocks();
                                            enumerateQuestions();
                                            saveSurvey();
                                        })
                                    }
                                },
                                error: function (msg) {
                                    console.log('msg no enviado')
                                }

                            });
                        }
                    }
                }
            });
        }
    });


    $('#save_block_configuration').on('click', function () {
        saveBlockConfiguration();
        enumerateQuestionBlocks();
        enumerateQuestions();
        saveSurvey();
    });


    //Funciones para relacionar momentos con bloques de preguntas
    $('#associate_questions_to_moment').submit(function (e) {
        e.preventDefault();
        var block_id = $('#current-question-block').val();
        var question_ids = new Array();
        var moment_id = $("#moment_object").val();

        $('#' + block_id + ' div.db_question_id').each(function (index) {
            question_ids.push(
                {
                    'question_id': $(this).attr('id')
                }
            );
        });

        $.ajax({
            type: 'POST',
            url: '/surveys/questions_moments/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                ids: JSON.stringify(question_ids),
                'moment_id': moment_id
            },
            dataType: 'JSON',
            success: function (msg) {
                if (msg.success) {
                    //alert('Se han asociado los momentos a las preguntas');
                }
            },
            error: function (msg) {
                console.log('msg no enviad')
            }

        });
    });


    $('a.actions_question').on('click', function () {
        if ($(this).hasClass('update_question')) {
            //alert('Edit Question');
            $('#main-configuration-panel').addClass('hidden');
            $('#add-question-option-panel').addClass('hidden');
            $('#add-new-question-configuration-panel').addClass('hidden');
            $('#questions-block-configuration-panel').addClass('hidden');
            $('#update-question-configuration-panel').removeClass('hidden');

            $('#survey-main-content div.question-content').each(function () {
                $(this).removeClass('active-question');
            });

            $(this).closest('div.question-content').addClass('active-question');

            var question_id = $(this).closest('div.question-content').find('div.db_question_id').attr('id');

            var question_survey_id = $(this).closest('div.question-content').attr('id');

            console.log(question_id)
            console.log(question_survey_id)

            $('#current-question-updated').val(question_survey_id);

            return getQuestionToUpdate(question_id);

        } else if ($(this).hasClass('remove_question')) {

            var self = $(this);

            bootbox.dialog({
                message: "¿Esta seguro de eliminar la pregunta?",
                title: "Eliminar Pregunta",
                buttons: {
                    success: {
                        label: "Cancelar",
                        className: "btn-white",
                        callback: function () {
                            return true;
                        }
                    },
                    main: {
                        label: "Eliminar",
                        className: "btn-twitter",
                        callback: function () {

                            var question_id = self.closest('div.question-content').find('div.db_question_id').attr('id');

                            var question_ids = new Array();

                            question_ids.push(
                                {
                                    'question_id': question_id
                                }
                            );

                            deleteQuestion(self, question_ids);
                        }
                    }
                }
            });
        }
    })

    //Funciones para relacionar momentos con bloques de preguntas
    $('#associate_questions_to_attribute').submit(function (e) {
        e.preventDefault();
        var question_id = $('#current-question').val();
        var attribute_id = $("#attribute_object").val();

        console.log(question_id)
        console.log(attribute_id)

        $.ajax({
            type: 'POST',
            url: '/surveys/questions_attributes/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'attribute_id': attribute_id,
                'question_id': question_id
            },
            dataType: 'JSON',
            success: function (msg) {
                if (msg.success) {
                    //alert('Se han asociado el attributo a las preguntas');
                }
            },
            error: function (msg) {
                console.log('msg no enviado')
            }

        });
    });

    $('div.question-content').hover(function () {
        $(this).find('.actions').fadeIn(100);
    }, function () {
        $(this).find('.actions').fadeOut(100);
    });


    $(document).on('keyup', '.option_added', function () {
        addQuestionOptions();
    });

    $('.multiple_choice_options_set').change(function () {
        addQuestionOptions();
    });


    //ColorPicker instance for new block text
    $('#new_block_color_picker').ColorPicker(
        {
            color: '#cecece',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#new_block_color_picker div').css('backgroundColor', '#' + hex);
                setStyleToBlock();

            }
        }
    );

    //ColorPicker instance for new border block
    $('#new_block_border_color_picker').ColorPicker(
        {
            color: '#cecece',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#new_block_border_color_picker div').css('backgroundColor', '#' + hex);
                if (!$("#new_block_has_border").is(":checked")) {
                    setStyleToBlock();
                }
            }
        }
    );

    //ColorPicker instance for new background block
    $('#new_block_background_color_picker').ColorPicker(
        {
            color: '#cecece',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#new_block_background_color_picker div').css('backgroundColor', '#' + hex);
                if (!$("#new_block_has_background").is(":checked")) {
                    setStyleToBlock();
                }
            }
        }
    );


    /*BLOCK DESIGN*/
    //button to select font family
    $('#new_block_font').change(function(){
        setStyleToBlock();
    });


})




function enumerateQuestions() {
    $('#survey-main-content div.question-content').each(function (index) {
        $(this).attr('id', 'question-' + (index + 1));
        $(this).children('div.question_id').text(index + 1 + '.- ');
    });
}

function enumerateQuestionBlocks() {
    $('#survey-main-content div.row-block').each(function (index) {
        $(this).attr('id', 'block-' + (index + 1));
    });
}

function getQuestionToUpdate(question_id) {
    $.ajax({
        type: 'GET',
        url: '/surveys/' + question_id + '/edit/',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        dataType: 'JSON',
        success: function (json_response) {

            if (json_response.question_type_name == 'Multiple Choice') {

                //alert('Multiple Choice');
                tinymce.get('tinymce-editor-update-question').setContent(json_response.question_title)

                var form = '<div id="question_type_2" class="question multiple_choice_u">'

                form += '<select name="question_type_select" id="question_type_select" disabled>'
                form += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>'
                form += '</select>'

                form += '<form class="form-horizontal padder" id="question_type_2_form">'
                form += '<div class="form-group">'
                form += '<p>'
                form += '<input class="multiple_choice_title question_title_updated" type="hidden" name="mo_title" maxlength="100" value="' + json_response.question_title + '"/>'
                form += '</p>'
                form += '<p>Options</p>'
                form += '<div class="multiple_choice_options_set_u">'

                $.each(json_response.question_options, function (index, value) {
                    form += '<div class="dynamic_inputs">'
                    form += '<i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>'
                    form += '<input type="hidden" value="' + value.option_id + '" />'
                    form += '<input type="text" maxlength="100" class="option_added_u form-control input-query" value="' + value.option_label + '"/>'
                    form += ''
                    form += '</div>'
                });

                form += '<input type="text" maxlength="100" class="dummy_option_u form-control" value="Clic para agregar otra opcion"/>'
                form += '</div>'
                form += '</div>'
                form += '<input id="edit_multiple_choice" type="submit" class="btn btn-info" value="Modificar Pregunta" />'
                form += '</form>'
                form += '</div>'

                if (json_response.question_moment_id) {
                    var moment_id = json_response.question_moment_id;
                    $('#update_moment_association option[value='+moment_id+']').prop("selected", true);
                }
                if (json_response.question_attribute_id) {
                    var attribute_id = json_response.question_attribute_id;
                    $("#update_attribute_association option[value="+attribute_id+"]").prop( "selected", true )
                }

                $('.question-conf').html(form);
            } else if (json_response.question_type_name == 'Matrix') {
                //alert('Matrix');

                tinymce.get('tinymce-editor-update-question').setContent(json_response.question_title)
                var formMatrix

                formMatrix = '<div id="question_type_1" style="display: inline;" class="question matrix_u col-lg-12">'

                formMatrix += '<select class="form-control" name="question_type_select" id="question_type_select" disabled>'
                formMatrix += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>'
                formMatrix += '</select>'

                formMatrix += '<form class="form-horizontal padder" id="question_type_1_form">'
                formMatrix += '<div class="form-group">'
                formMatrix += '<p>'
                formMatrix += '<input class="matrix_title question_title_updated" type="hidden" name="matrix_title" maxlength="100" value="' + json_response.question_title + '"/>'
                formMatrix += '</p>'
                formMatrix += '<p>Establece el n&uacute;mero de columnas</p>'
                formMatrix += '<div class="matrix_cols_u">'

                $.each(json_response.question_options, function (index, value) {
                    formMatrix += '<div class="dynamic_inputs input-close">'
                    formMatrix += '<i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>'
                    formMatrix += '<input type="hidden" value="' + value.option_id + '" />'
                    formMatrix += '<input type="text" maxlength="100" class="option_added_u form-control input-query" value="' + value.option_label + '"/>'
                    formMatrix += ''
                    formMatrix += '</div>'
                });

                formMatrix += '<input type="text" maxlength="100" class="dummy_option_u form-control" value="Clic para agregar otra columna"/>'
                formMatrix += '</div>'
                formMatrix += '</div>'

                formMatrix += '<div class="form-group">'
                formMatrix += '<p>Establece el n&uacute;mero de renglones</p>'
                formMatrix += '<div class="matrix_rows_u">'

                $.each(json_response.question_rows, function (index, value) {
                    /* New option remove dummy-option
                    var new_option_proto = '<div class="dynamic_inputs input-close"><i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>';
                    var remove_button = '<input type="text" maxlength="100" class="option_added input-query form-control"/></div>';
                    * */
                    formMatrix += '<div class="dynamic_inputs input-close">'
                    formMatrix += '<i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>'
                    formMatrix += '<input type="hidden" value="' + value.row_id + '" />'
                    formMatrix += '<input type="text" maxlength="100" class="option_added_u form-control input-query" value="' + value.row_title + '"/>'
                    formMatrix += ''
                    formMatrix += '</div>'
                });

                formMatrix += '<input type="text" maxlength="100" class="dummy_option_u form-control" value="Clic para agregar otro renglon"/>'
                formMatrix += '</div>'
                formMatrix += '</div>'

                formMatrix += '<div class="form-group">'
                formMatrix += '<input id="edit_matrix" type="submit" class="btn btn-info" value="Modificar Pregunta" />'
                formMatrix += '</form>'
                formMatrix += '</div>'
                formMatrix += '</div>'

                if (json_response.question_moment_id) {
                    var moment_id = json_response.question_moment_id;
                    $('#update_moment_association option[value='+moment_id+']').prop("selected", true);
                }
                if (json_response.question_attribute_id) {
                    var attribute_id = json_response.question_attribute_id;
                    $("#update_attribute_association option[value="+attribute_id+"]").prop( "selected", true )
                }

                $('.question-conf').html(formMatrix);
            } else if (json_response.question_type_name == 'Range') {

                //alert('Range');

                tinymce.get('tinymce-editor-update-question').setContent(json_response.question_title)
                var formRange = '<div id="question_type_4" class="question range_u">'

                formRange += '<select name="question_type_select" id="question_type_select" disabled>'
                formRange += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>'
                formRange += '</select>'

                formRange += '<form class="form-horizontal padder" id="question_type_4_form">'
                formRange += '<div class="form-group">'
                formRange += '<p>'
                formRange += '<input class="range_title question_title_updated" type="hidden" name="range_title" maxlength="100" value="' + json_response.question_title + '"/>'
                formRange += '</p>'
                formRange += '<p>Establece los siguientes datos</p>'
                formRange += '<div class="range_field_set_u">'

                formRange += '<div class="col-lg-6 col-sm-6">'
                formRange += ' <label>Valor inicial:</label>'
                formRange += '<input type="text" maxlength="100" class="start_number form-control" value="' + json_response.question_first_value + '"/>'

                formRange += '<br>'
                formRange += '<label>Etiqueta Inicial:</label>'
                formRange += '<input type="text" maxlength="100" class="start_label form-control" value="' + json_response.question_first_label + '"/>'
                formRange += '</div>'

                formRange += '</div>'
                formRange += '<div class="col-lg-6 col-sm-6">'
                formRange += '<div class="range_field_set_u">'
                formRange += '<label>Valor Final:</label>'
                formRange += '<input type="text" maxlength="100" class="end_number form-control" value="' + json_response.question_last_value + '"/>'

                formRange += '<br>'
                formRange += '<label>Etiqueta Final:</label>'
                formRange += '<input type="text" maxlength="100" class="end_label form-control" value="' + json_response.question_last_label + '"/>'

                formRange += '</div>'
                formRange += '</div>'
                formRange += '</div>'

                formRange += '<div class="form-group">'
                formRange += '<input id="edit_range_question" type="submit" class="btn btn-info" value="Modificar Pregunta" />'
                formRange += '</form>'
                formRange += '</div>'
                formRange += '</div>'

                if (json_response.question_moment_id) {
                    var moment_id = json_response.question_moment_id;
                    $('#update_moment_association option[value='+moment_id+']').prop("selected", true);
                }
                if (json_response.question_attribute_id) {
                    var attribute_id = json_response.question_attribute_id;
                    $("#update_attribute_association option[value="+attribute_id+"]").prop( "selected", true )
                }

                $('.question-conf').html(formRange);
            } else if (json_response.question_type_name == 'Open Question') {
                //alert('Open question');
                tinymce.get('tinymce-editor-update-question').setContent(json_response.question_title)
                var formOpenQuestion = '<div id="question_type_3" class="question open_question_u">'

                formOpenQuestion += '<select name="question_type_select" id="question_type_select" disabled>'
                formOpenQuestion += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>'
                formOpenQuestion += '</select>'

                formOpenQuestion += '<form id="question_type_3_form">'
                formOpenQuestion += '<p>'
                formOpenQuestion += '<input class="open_question_title question_title_updated" type="hidden" name="oq_title" maxlength="100" value="' + json_response.question_title + '"/>'
                formOpenQuestion += '</p>'

                formOpenQuestion += '</div>'
                formOpenQuestion += '<input id="edit_open_question" type="submit" class="btn btn-info" value="Modificar Pregunta" />'
                formOpenQuestion += '</form>'
                formOpenQuestion += '<div>'

                if (json_response.question_moment_id) {
                    var moment_id = json_response.question_moment_id;
                    $('#update_moment_association option[value='+moment_id+']').prop("selected", true);
                }
                if (json_response.question_attribute_id) {
                    var attribute_id = json_response.question_attribute_id;
                    $("#update_attribute_association option[value="+attribute_id+"]").prop( "selected", true )
                }

                $('.question-conf').html(formOpenQuestion);
            } else if (json_response.question_type_name == 'False and True') {
                //alert('False and True');
                tinymce.get('tinymce-editor-update-question').setContent(json_response.question_title)
                var formFandT = '<div id="question_type_5" class="question true_and_false_u">'

                formFandT += '<select name="question_type_select" id="question_type_select" disabled>'
                formFandT += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>'
                formFandT += '</select>'

                formFandT += '<form id="question_type_5_form">'
                formFandT += '<p>'
                formFandT += '<input class="true_and_false_title question_title_updated" type="hidden" name="true_and_false_title" maxlength="100" value="' + json_response.question_title + '"/>'
                formFandT += '</p>'

                formFandT += '</div>'
                formFandT += '<input id="edit_true_and_false_question" type="submit" class="btn btn-info" value="Modificar Pregunta" />'
                formFandT += '</form>'
                formFandT += '<div>'

                if (json_response.question_moment_id) {
                    var moment_id = json_response.question_moment_id;
                    $('#update_moment_association option[value='+moment_id+']').prop("selected", true);
                }
                if (json_response.question_attribute_id) {
                    var attribute_id = json_response.question_attribute_id;
                    $("#update_attribute_association option[value="+attribute_id+"]").prop( "selected", true )
                }

                $('.question-conf').html(formFandT);
            }
        },
        error: function (msg) {
            console.log(msg)
        }

    });

}


function deleteQuestion(self, question_ids) {
    $.ajax({
        type: 'POST',
        url: '/surveys/delete_questions/',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            ids: JSON.stringify(question_ids),
            survey_id: $('#survey_id').val()
        },
        dataType: 'JSON',
        success: function (msg) {
            //alert(msg);
            if (msg.success) {
                $(self).closest('div.question-content').slideUp('slow', function () {
                    $(this).remove();
                    enumerateQuestions();
                    enumerateQuestionBlocks();
                    saveSurvey();
                })
            }
        },
        error: function (msg) {
            console.log('msg no enviado')
        }

    });
}

function saveBlockConfiguration(){
    var block_id = $('#current-question-block').val();
    var question_ids = new Array();
    var moment_id = $("#moment_object").val();

    $('#' + block_id + ' div.db_question_id').each(function (index) {
        question_ids.push(
            {
                'question_id': $(this).attr('id')
            }
        );
    });

    $.ajax({
        type: 'POST',
        url: '/surveys/questions_moments/',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            ids: JSON.stringify(question_ids),
            'moment_id': moment_id
        },
        dataType: 'JSON',
        success: function (msg) {
            if (msg.success) {
                //alert('Se han asociado los momentos a las preguntas');
            }
        },
        error: function (msg) {
            console.log('msg no enviad')
        }

    });

}

function setStyleToBlock(){
    var current_question_block = $('#current-question-block').val();

    var font_family, font_color, border_color, border_style,
        border_width, background_color;



    //Determine font selected value
    switch ($('#new_block_font').val()){
        case 'times_new_roman':
            font_family = 'Times New Roman';
            break;
        case 'arial':
            font_family = 'Arial';
            break;
        case 'helvetica':
            font_family = 'Helvetica';
            break;
        case 'courier_new':
            font_family = 'Courier New';
            break;
        default:
            break;
    }

    //Determine font color
    font_color = $('#new_block_color_picker div').css('background-color');

    //Determine border properties
    if (!$("#new_block_has_border").is(":checked")) {
        border_color = $('#new_block_border_color_picker div').css('background-color');
        border_style = $('#new_block_border_style').val()+' !important';
        border_width = $('#new_block_border_width').val()+' !important';
    }

    //Determine background properties
    if (!$("#new_block_has_background").is(":checked")) {
        background_color = $('#new_block_background_color_picker div').css('background-color');
    } else {
        background_color = 'transparent';
    }

    console.log(new_block_style);

    var new_block_style = {
        'font-family': font_family,
        color: font_color,
        'border-color': border_color + '!important',
        'border-style': border_style,
        'border-width': border_width,
        'background-color': background_color
    }

    console.log(new_block_style);

    $('#' + current_question_block+' section.question-block').css(new_block_style);

}
