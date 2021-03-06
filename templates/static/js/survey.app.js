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

    /** ELEMENTS TO HIDE WHEN THE DOM IS READY **/
    $('.question_actions .actions').hide();
    $('.intro_block_actions').hide();
    //current block editing icon
    $('div.icon_current_edited').hide();


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

        var type_of_operation = 'questions-block';

        if(parent.hasClass('text-block')){
            var style =($(this).closest('div.row-block').find('section.question-block').attr('style')).split(';');

            setDefaultTextBlockStyleInDesign(style);

            /*
            if($('#survey_has_blocks_style').val() == 'True'){
                $('#apply_design_to_all_blocks').prop('disabled', true);
            }
            */
            $('#main-configuration-panel').addClass('hidden');
            $('#questions-block-configuration-panel').addClass('hidden');
            $('#add-question-option-panel').addClass('hidden');
            $('#add-new-question-configuration-panel').addClass('hidden');
            $('#update-question-configuration-panel').addClass('hidden');
            $('#update-survey-block').removeClass('hidden');

            $('#survey-main-content div.row-block').each(function () {
                $(this).find('section.question-block').removeClass('selected-block');
                $(this).find('div.question-content').removeClass('active-question');
            });

            parent.find('section.question-block').addClass('selected-block');

            var block_description = parent.find('div.panel-body').html();
            $('#current-text-block-updated').val(parent.attr('id'));
            tinymce.get('tinymce-editor-update-block').setContent(block_description);
        } else if(parent.hasClass('question-block')){

        } else {
            var style =($(this).closest('div.row-block').find('section.question-block').attr('style')).split(';');

            setDefaultStyleInDesign(style);

            if($('#survey_has_blocks_style').val() == 'True'){
                $('#apply_design_to_all_blocks').prop('disabled', true);
            }

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
        }

        if (parent.hasClass('row-no-block')) {
            parent.find('section.question-block').removeClass('selected-block');
            parent.find('div.question-content').addClass('active-question');
            $('#questions-block-configuration-panel').removeClass('hidden');
        }

    });


    $(document).on('click', 'a.actions_block', function (e) {
        e.preventDefault();
        var action = $(this).attr('id')
        if ($(this).hasClass("remove_block")) {
            var title = '',
                message = '',
                operation = '';
            if($(this).closest('div.row-block').hasClass('text-block')){
                title = 'Eliminar Bloque de Texto';
                message = '¿Esta seguro que desea eliminar el bloque de texto?';
                operation = 'del_text_block';
            } else if($(this).closest('div.row-block').hasClass('question-block')){
                title = 'Eliminar Pregunta';
                message = '¿Esta seguro que desea eliminar la pregunta?';
                operation = 'del_question_block';
            } else if($(this).closest('div.row-block').hasClass('questions-block')){
                title = 'Eliminar bloque de preguntas';
                message = '¿Esta seguro que desea eliminar el bloque de preguntas?';
                operation = 'del_questions_block';
            }
            var self = $(this);

            bootbox.dialog({
                message: message,
                title: title,
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
                            switch (operation){
                                case 'del_text_block':
                                    $(self).closest('li.list-group-item').slideUp('slow', function () {
                                        $(this).remove();
                                        enumerateQuestionBlocks();
                                        enumerateQuestions();
                                        saveSurvey();
                                    })
                                    break;
                                case 'del_questions_block':
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
                                                $(self).closest('li.list-group-item').slideUp('slow', function () {
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
                                    break;
                                case 'del_question_bock':
                                    break;
                            }
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


    $(document).on('click', 'a.actions_question', function () {
        if ($(this).hasClass('update_question')) {
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

            $('#current-question-updated').val(question_survey_id);

            var style = $(this).closest('div.question-content').attr('style');

            setDefaultStyleInQuestionDesignUpdate((style).split(';'));

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
                            if(question_id == undefined){
                                self.closest('li.list-group-item').slideUp('slow', function(){
                                    $(this).remove();
                                    enumerateQuestionBlocks();
                                    enumerateQuestions();
                                    saveSurvey();
                                })
                            } else {
                                deleteQuestion(self, question_ids);
                            }
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
                //$('#new_block_color_picker div').css('backgroundColor', '#' + hex);
                $('#new_block_color_picker div').attr('style', 'background-color: #' + hex + ';');
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
                //$('#new_block_border_color_picker div').css('backgroundColor', '#' + hex);
                $('#new_block_border_color_picker div').attr('style', 'background-color: #' + hex + ';');
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
                //$('#new_block_border_color_picker div').css('backgroundColor', '#' + hex);
                $('#new_block_background_color_picker div').attr('style', 'background-color: #' + hex + ';');
                if (!$("#new_block_has_background").is(":checked")) {
                    setStyleToBlock();
                }
            }
        }
    );

    //ColorPicker instance for new font color question
    $('#new_question_font_color_picker').ColorPicker(
        {
            color: '#717171',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#new_question_font_color_picker div').attr('style', 'background-color: #' + hex + ';');
                setStyleToQuestion();
                if($('#apply_design_to_all_questions').is(':checked')){
                    var global_question_style = setStyleToQuestion();
                    $('#survey_question_style').val(global_question_style);
                }
            }
        }
    );

    //ColorPicker instance for border color survey
    $('#survey_border_color_picker').ColorPicker(
        {
            color: '#FFFFFF',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#survey_border_color_picker div').attr('style', 'background-color: #' + hex + ';');
                buildSurveyStyle();
            }
        }
    );

    //ColorPicker instance for background color survey
    $('#survey_background_color_picker').ColorPicker(
        {
            color: '#FFFFFF',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#survey_background_color_picker div').attr('style', 'background-color: #' + hex + ';');
                buildSurveyStyle();
            }
        }
    );

    //ColorPicker instance for font color when question is updated
    $('#update_question_font_color_picker').ColorPicker(
        {
            color: '#FFFFFF',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#update_question_font_color_picker div').attr('style', 'background-color: #' + hex + ';');
                updateStyleToBlock();
            }
        }
    );

    //ColorPicker instance for font color when text block is updated
    $('#update_text_block_color_picker').ColorPicker(
        {
            color: '#FFFFFF',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#update_text_block_color_picker div').attr('style', 'background-color: #' + hex + ';');
                setStyleToTextBlock();
            }
        }
    );

    $('#update_text_block_border_color_picker').ColorPicker(
        {
            color: '#FFFFFF',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#update_text_block_border_color_picker div').attr('style', 'background-color: #' + hex + ';');
                setStyleToTextBlock();
            }
        }
    );

    $('#update_text_block_background_color_picker').ColorPicker(
        {
            color: '#FFFFFF',
            onShow: function (colpkr) {
                $(colpkr).fadeIn(500);
                return false;
            },
            onHide: function (colpkr) {
                $(colpkr).fadeOut(500);
                return false;
            },
            onChange: function (hsb, hex, rgb) {
                $('#update_text_block_background_color_picker div').attr('style', 'background-color: #' + hex + ';');
                setStyleToTextBlock();
            }
        }
    )

    //control to add style to question
    $('#new_question_font_style').change(function(){
        setStyleToQuestion()
        if($('#apply_design_to_all_questions').is(':checked')){
            var global_question_style = setStyleToQuestion();
            $('#survey_question_style').val(global_question_style);
        }
    });

    //control to add style to question
    $('#new_question_font').change(function(){
        setStyleToQuestion()
        if($('#apply_design_to_all_questions').is(':checked')){
            var global_question_style = setStyleToQuestion();
            $('#survey_question_style').val(global_question_style);
        }
    });

    $('#apply_design_to_all_questions').change(function(){
        if($(this).is(':checked')){
            var global_question_style = setStyleToQuestion();
            $('#survey_has_question_style').val('True');
            $('#survey_question_style').val(global_question_style);
        } else {
            $('#survey_has_question_style').val('False');
            $('#survey_question_style').val('');
        }
    });

    //control to update question style in the preview
    $('#update_question_font, #update_question_font_style').change(function(){
        updateStyleToBlock();
    });


    /*BLOCK DESIGN*/
    //button to select font family
    $('#new_block_font').change(function(){
        setStyleToBlock();
    });

    //input to select if the block has or has not a border
    $('#new_block_has_border').change(function(){
        if($(this).is(':checked')) {
            $('#border_block_configuration_section').slideUp(200);
        } else {
            $('#border_block_configuration_section').slideDown(200);
        }
        setStyleToBlock();
    });

    //input to check if the block has or has not a background
    $('#new_block_has_background').change(function(){
        if($(this).is(':checked')) {
            $('#new_block_background_configuration_section').slideUp(200);
        } else {
            $('#new_block_background_configuration_section').slideDown(200);
        }
        setStyleToBlock();
    });

    //
    $('#update_text_block_has_border').change(function(){
        if($(this).is(':checked')) {
            $('#border_update_text_block_configuration_section').slideUp(200);
        } else {
            $('#border_update_text_block_configuration_section').slideDown(200);
        }
        setStyleToTextBlock();
    });

    //
    $('#update_text_block_has_background').change(function(){
        if($(this).is(':checked')) {
            $('#update_text_block_background_configuration_section').slideUp(200);
        } else {
            $('#update_text_block_background_configuration_section').slideDown(200);
        }
        setStyleToTextBlock();
    });

    //control to select the new block border style
    $('#new_block_border_style').change(function(){
        setStyleToBlock();
    });

    //control to select the new block border size
    $('#new_block_border_width').change(function(){
        setStyleToBlock();
    });

    //control to put a general style to blocks in this survey
    $('#apply_design_to_all_blocks').change(function(){
        if($(this).is(':checked')){
            $('#survey_has_blocks_style').val('True');
            $('#survey_blocks_style').val(setStyleToBlock());
        } else {
            $('#survey_has_blocks_style').val('False');
            $('#survey_blocks_style').val('');
        }
    });

    //control to verify if checkbox is checked and change the value of the input about moment associated
    $('#associate_moment_to_block').change(function(){
        var block_id = $('#current-question-block').val();
        var moment_id = $("#moment_object").val();
        if($(this).is(':checked')){
            $('#'+block_id+' input.block_moment_associated_id').removeClass('false');
            $('#'+block_id+' input.block_moment_associated_id').addClass('true');
            $('#'+block_id+' input.block_moment_associated_id').val(moment_id);
        } else {
            $('#'+block_id+' input.block_moment_associated_id').removeClass('true');
            $('#'+block_id+' input.block_moment_associated_id').addClass('false');
            $('#'+block_id+' input.block_moment_associated_id').val('');
        }
    });

    //control to change the value of the moment associated inside the block
    $('#moment_object').change(function(){
        var block_id = $('current-question-block').val();
        if($('#associate_moment_to_block').is(':checked')){
            $('#'+block_id+' input.block_moment_associated_id').removeClass('false');
            $('#'+block_id+' input.block_moment_associated_id').addClass('true');
            $('#'+block_id+' input.block_moment_associated_id').val($(this).val());
        }
    });


    //control to check if survey has border
    $('#survey_has_border').change(function(){
        if($(this).is(':checked')){
            $('#border_survey_configuration_section').slideUp(200);
        } else {
            $('#border_survey_configuration_section').slideDown(200);
        }
        buildSurveyStyle();
    });

    //control to check if survey has background
    $('#survey_has_background').change(function(){
        if($(this).is(':checked')){
            $('#survey_background_configuration_section').slideUp(200);
        } else {
            $('#survey_background_configuration_section').slideDown(200);
        }
        buildSurveyStyle();
    });

    $('#survey_border_style, #survey_border_width, #survey_has_shadow').change(function(){
        buildSurveyStyle();
    });

    $('#btn-save-text-block').on('click', function(){
       saveSurvey();
    });

    //
    $('#update_text_block_font').change(function(){
        setStyleToTextBlock();
    });

    $('#update_text_block_has_border, #update_text_block_has_background').change(function(){
        setStyleToTextBlock();
    });

    $('#update_text_block_border_style, #update_text_block_border_width').change(function(){
        setStyleToTextBlock();
    });



    getSurveyStyle();
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
            console.log(json_response);
            if (json_response.question_type_name == 'Multiple Choice') {

                $('#update-question-title').val(json_response.question_title);

                var form = '<div id="question_type_2" class="question multiple_choice_u">';

                form += '<select name="question_type_select" id="question_type_select" disabled>';
                form += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>';
                form += '</select>';

                form += '<form class="form-horizontal padder" id="question_type_2_form">';
                form += '<div class="form-group">';
                form += '<p>';
                form += '<input class="multiple_choice_title question_title_updated" type="hidden" name="mo_title" maxlength="100" value="' + json_response.question_title + '"/>';
                form += '</p>';
                form += '<p>Options</p>';
                form += '<div class="multiple_choice_options_set_u">';

                $.each(json_response.question_options, function (index, value) {
                    form += '<div class="dynamic_inputs">';
                    form += '<i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>';
                    form += '<input type="hidden" value="' + value.option_id + '" />';
                    form += '<input type="text" maxlength="100" class="option_added_u form-control input-query" value="' + value.option_label + '"/>';
                    form += '';
                    form += '</div>';
                });

                form += '<input type="text" maxlength="100" class="dummy_option_u form-control" value="Clic para agregar otra opcion"/>';
                form += '</div>';
                form += '</div>';
                form += '</form>';
                form += '</div>';

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
                $('#update-question-title').val(json_response.question_title);
                var formMatrix;

                formMatrix = '<div id="question_type_1" style="display: inline;" class="question matrix_u col-lg-12">';

                formMatrix += '<select class="form-control" name="question_type_select" id="question_type_select" disabled>';
                formMatrix += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>';
                formMatrix += '</select>';

                formMatrix += '<form class="form-horizontal padder" id="question_type_1_form">';
                formMatrix += '<div class="form-group">';
                formMatrix += '<p>';
                formMatrix += '<input class="matrix_title question_title_updated" type="hidden" name="matrix_title" maxlength="100" value="' + json_response.question_title + '"/>';
                formMatrix += '</p>';
                formMatrix += '<p>Establece el n&uacute;mero de columnas</p>';
                formMatrix += '<div class="matrix_cols_u">';

                $.each(json_response.question_options, function (index, value) {
                    formMatrix += '<div class="dynamic_inputs input-close">';
                    formMatrix += '<i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>';
                    formMatrix += '<input type="hidden" value="' + value.option_id + '" />';
                    formMatrix += '<input type="text" maxlength="100" class="option_added_u form-control input-query" value="' + value.option_label + '"/>';
                    formMatrix += '';
                    formMatrix += '</div>';
                });

                formMatrix += '<input type="text" maxlength="100" class="dummy_option_u form-control" value="Clic para agregar otra columna"/>';
                formMatrix += '</div>';
                formMatrix += '</div>';

                formMatrix += '<div class="form-group">';
                formMatrix += '<p>Establece el n&uacute;mero de renglones</p>';
                formMatrix += '<div class="matrix_rows_u">';

                $.each(json_response.question_rows, function (index, value) {
                    /* New option remove dummy-option
                    var new_option_proto = '<div class="dynamic_inputs input-close"><i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>';
                    var remove_button = '<input type="text" maxlength="100" class="option_added input-query form-control"/></div>';
                    * */
                    formMatrix += '<div class="dynamic_inputs input-close">';
                    formMatrix += '<i class="icon-remove remove-dummy" onclick="deleteOption(event);" ></i>';
                    formMatrix += '<input type="hidden" value="' + value.row_id + '" />';
                    formMatrix += '<input type="text" maxlength="100" class="option_added_u form-control input-query" value="' + value.row_title + '"/>';
                    formMatrix += '';
                    formMatrix += '</div>';
                });

                formMatrix += '<input type="text" maxlength="100" class="dummy_option_u form-control" value="Clic para agregar otro renglon"/>';
                formMatrix += '</div>';
                formMatrix += '</div>';

                formMatrix += '<div class="form-group">';
                formMatrix += '</form>';
                formMatrix += '</div>';
                formMatrix += '</div>';

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
                $('#update-question-title').val(json_response.question_title);
                var formRange = '<div id="question_type_4" class="question range_u">';

                formRange += '<select name="question_type_select" id="question_type_select" disabled>';
                formRange += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>';
                formRange += '</select>';

                formRange += '<form class="form-horizontal padder" id="question_type_4_form">';
                formRange += '<div class="form-group">';
                formRange += '<p>';
                formRange += '<input class="range_title question_title_updated" type="hidden" name="range_title" maxlength="100" value="' + json_response.question_title + '"/>';
                formRange += '</p>';
                formRange += '<p>Establece los siguientes datos</p>';
                formRange += '<div class="range_field_set_u">';

                formRange += '<div class="col-lg-6 col-sm-6">';
                formRange += ' <label>Valor inicial:</label>';
                formRange += '<input type="text" maxlength="100" class="start_number form-control" value="' + json_response.question_first_value + '"/>';

                formRange += '<br>';
                formRange += '<label>Etiqueta Inicial:</label>';
                formRange += '<input type="text" maxlength="100" class="start_label form-control" value="' + json_response.question_first_label + '"/>';
                formRange += '</div>';

                formRange += '</div>';
                formRange += '<div class="col-lg-6 col-sm-6">';
                formRange += '<div class="range_field_set_u">';
                formRange += '<label>Valor Final:</label>';
                formRange += '<input type="text" maxlength="100" class="end_number form-control" value="' + json_response.question_last_value + '"/>';

                formRange += '<br>';
                formRange += '<label>Etiqueta Final:</label>';
                formRange += '<input type="text" maxlength="100" class="end_label form-control" value="' + json_response.question_last_label + '"/>';

                formRange += '</div>';
                formRange += '</div>';
                formRange += '</div>';

                formRange += '<div class="form-group">';
                formRange += '</form>';
                formRange += '</div>';
                formRange += '</div>';

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
                $('#update-question-title').val(json_response.question_title);
                var formOpenQuestion = '<div id="question_type_3" class="question open_question_u">';

                formOpenQuestion += '<select name="question_type_select" id="question_type_select" disabled>';
                formOpenQuestion += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>';
                formOpenQuestion += '</select>';

                formOpenQuestion += '<form id="question_type_3_form">';
                formOpenQuestion += '<p>';
                formOpenQuestion += '<input class="open_question_title question_title_updated" type="hidden" name="oq_title" maxlength="100" value="' + json_response.question_title + '"/>';
                formOpenQuestion += '</p>';

                formOpenQuestion += '</div>';
                formOpenQuestion += '</form>';
                formOpenQuestion += '<div>';

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
                $('#update-question-title').val(json_response.question_title);
                var formFandT = '<div id="question_type_5" class="question true_and_false_u">';

                formFandT += '<select name="question_type_select" id="question_type_select" disabled>';
                formFandT += '<option value="' + json_response.question_type_id + '" selected>' + json_response.question_type_name + '</option>';
                formFandT += '</select>';

                formFandT += '<form id="question_type_5_form">';
                formFandT += '<p>';
                formFandT += '<input class="true_and_false_title question_title_updated" type="hidden" name="true_and_false_title" maxlength="100" value="' + json_response.question_title + '"/>';
                formFandT += '</p>';

                formFandT += '</div>';
                formFandT += '</form>';
                formFandT += '<div>';

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
                $(self).closest('li.list-group-item').slideUp('slow', function () {
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

    if($('#associate_moment_to_block').is(':checked')){
        $('#'+block_id+' input.block_moment_associated_id').removeClass('false');
        $('#'+block_id+' input.block_moment_associated_id').addClass('true');
        $('#'+block_id+' input.block_moment_associated_id').val(moment_id);

        var questions_in_block = $('#'+block_id+' div.question-content').length;

        if(questions_in_block == 0){
            return true;
        } else {
            console.log(moment_id);

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
                    'moment_id': moment_id,
                    'survey_id': $('#survey_id').val()
                },
                dataType: 'JSON',
                success: function (msg) {
                    if (msg.success) {
                        //alert('Se han asociado los momentos a las preguntas');
                        return true;
                    } else {
                        return false;
                        console.log(msg);
                    }
                },
                error: function (msg) {
                    console.log('msg no enviad')
                }

            });
        }

    }
}


/**
 * FUNCTIONS TO MANAGE THE BLOCK DESIGN
 */


function setStyleToBlock(){
    var current_question_block = $('#current-question-block').val();

    var font_family, font_color, border_color, border_style,
        border_width, background_color;



    //Determine font selected value
    switch ($('#new_block_font').val()){
        case 'times_new_roman':
            font_family = 'Times New Roman';
            break;
        case 'lato':
            font_family = 'Lato';
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
    font_color = rgb2hex($('#new_block_color_picker div').css('background-color'));

    //Determine border properties
    if (!$("#new_block_has_border").is(":checked")) {
        border_color = rgb2hex($('#new_block_border_color_picker div').css('background-color'));
        border_style = $('#new_block_border_style').val();
        border_width = $('#new_block_border_width').val();
    } else {
        border_color = 'rgba(255, 255, 255, 0)';
        border_style = 'solid';
        border_width = '0px';
    }

    //Determine background properties
    if (!$("#new_block_has_background").is(":checked")) {
        background_color = rgb2hex($('#new_block_background_color_picker div').css('background-color'));
    } else {
        background_color = 'rgba(255, 255, 255, 0)';
    }

    var attr_style = 'border: '+border_width+' '+border_style+' '+border_color+' !important; font-family: '+font_family+'; color: '+font_color+'; background-color: '+background_color+';';

    $('#' + current_question_block+' section.question-block').attr('style', attr_style);

    return attr_style;

}


function setStyleToQuestion(){
    var current_question = $('#current-question').val();

    var font_family, font_color, font_style;

    //Determine font selected value
    switch ($('#new_question_font').val()){
        case 'times_new_roman':
            font_family = 'Times New Roman';
            break;
        case 'lato':
            font_family = 'Lato';
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

    //Determine font style
    font_style = $('#new_question_font_style').val();

    console.log(font_style);

    //Determine font color
    font_color = rgb2hex($('#new_question_font_color_picker div').css('background-color'));

    var attr_style = 'display: table; min-width: 100%; min-height: 50px; font-family: '+font_family+'; font-style: '+font_style+'; color: '+font_color+';';

    $('#' + current_question).attr('style', attr_style);

    return attr_style;
}

function setStyleToTextBlock(){
    var current_text_block = $('#current-text-block-updated').val();

    var font_family, font_color, border_color, border_style,
        border_width, background_color;



    //Determine font selected value
    switch ($('#update_text_block_font').val()){
        case 'times_new_roman':
            font_family = 'Times New Roman';
            break;
        case 'lato':
            font_family = 'Lato';
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
    font_color = rgb2hex($('#update_text_block_color_picker div').css('background-color'));

    //Determine border properties
    if (!$("#update_text_block_has_border").is(":checked")) {
        border_color = rgb2hex($('#update_text_block_border_color_picker div').css('background-color'));
        border_style = $('#update_text_block_border_style').val();
        border_width = $('#update_text_block_border_width').val();
    } else {
        border_color = '#FFFFFF';
        border_style = 'solid';
        border_width = '0px';
    }

    //Determine background properties
    if (!$("#update_text_block_has_background").is(":checked")) {
        background_color = rgb2hex($('#update_text_block_background_color_picker div').css('background-color'));
    } else {
        background_color = 'rgba(255, 255, 255, 0)';
    }

    var attr_style = 'border: '+border_width+' '+border_style+' '+border_color+' !important; font-family: '+font_family+'; color: '+font_color+'; background-color: '+background_color+';';

    $('#' + current_text_block+' section.question-block').attr('style', attr_style);

    return attr_style;

}

function updateStyleToBlock(){
    var current_question = $('#current-question-updated').val();

    var font_family, font_color, font_style;

    //Determine font selected value
    switch ($('#update_question_font').val()){
        case 'times_new_roman':
            font_family = 'Times New Roman';
            break;
        case 'lato':
            font_family = 'Lato';
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

    //Determine font style
    font_style = $('#update_question_font_style').val();

    console.log(font_style);

    //Determine font color
    font_color = rgb2hex($('#update_question_font_color_picker div').css('background-color'));

    var attr_style = 'display: table; min-width: 100%; min-height: 50px; font-family: '+font_family+'; font-style: '+font_style+'; color: '+font_color+';';

    $('#' + current_question).attr('style', attr_style);
    console.log(current_question);
    console.log(attr_style);
}


function checkIfSurveyHasBlocksStyle(){
    var answer = $('#survey_has_blocks_style').val();
    if(answer == 'True'){
        return true;
    } else if(answer == 'False'){
        return false;
    }
}


function getSurveyBlocksStyle(){
    var survey_id = $('#survey_id').val();
    $.ajax({
        type: 'POST',
        url: '/surveys/getSurveyBlocksStyle/',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'survey_id': survey_id
        },
        dataType: 'JSON',
        async: false,
        success: function (msg) {
            if (msg.answer === true) {
                console.log(msg.blocks_style);
                return msg.blocks_style;
            } else {
                return '';
            }
        },
        complete: function(msg){
            if (msg.answer === true) {
                console.log(msg.blocks_style);
                return msg.blocks_style;
            } else {
                return '';
            }
        },
        error: function (msg) {
            return '';
        }

    });
}

function checkIfSurveyHasQuestionsStyle(){
    var answer = $('#survey_has_question_style').val();
    if(answer == 'True'){
        return true;
    } else if(answer == 'False'){
        return false;
    }
}


function getSurveyQuestionsStyle(){
    var questions_style = $('#survey_question_style').val();
    return questions_style;
}

function setDefaultStyle(){
    var default_style = ($('#survey_blocks_style').val()).split(';');
    setDefaultStyleInDesign(default_style);
}

function setStyleInUpdateQuestion(){
    var default_style = ($('#survey_question_style').val()).split(';');
    setDefaultStyleInQuestionDesignUpdate(default_style);
}

function setDefaultStyleInDesign(default_style){
    var border = (default_style[0]).split(' '); // border: 1px solid #cecece !important
    var border_width = $.trim(border[1]),
        border_style = $.trim(border[2]),
        border_color = $.trim(border[3]);

    var font = (default_style[1]).split(':'); // font-family: Times New Roman
    var font_family = $.trim(font[1]);

    var font_color = (default_style[2]).split(':'); // color: #cec4fe

    var color = $.trim(font_color[1]);

    var background_color = (default_style[3]).split(':'); // background-color: #cec6d7

    var background_c = $.trim(background_color[1]);




    switch(font_family){
        case 'Lato':
            font_family = 'lato';
            break;
        case 'Times New Roman':
            font_family = 'time_new_roman';
            break;
        case 'Arial':
            font_family = 'arial';
            break;
        case 'Helvetica':
            font_family = 'helvetica';
            break;
        case 'Courier New':
            font_family = 'courier_new';
            break;
    }

    $('#new_block_font option[value='+font_family+']').prop("selected", true);


    $('#new_block_color_picker div').attr('style', 'background-color: '+color)

    if(border_width == '0px' & border_style == 'solid' & border_color == 'transparent'){
        $('#new_block_has_border').prop('checked', true);
        $('#new_block_has_border_icon').addClass('checked');
        $('#border_block_configuration_section').slideUp(200);
    }

    $('#new_block_border_color_picker div').attr('style', 'background-color: '+border_color);

    $('#new_block_border_style option[value='+border_style+']').prop("selected", true);

    $('#new_block_border_width option[value='+border_width+']').prop('selected', true);

    if(background_c == 'rgba(255, 255, 255, 0)'){
        $('#new_block_has_background').attr('checked', true);
        $('#new_block_has_background_icon').addClass('checked');
        $('#new_block_background_configuration_section').slideUp(200);
    }

    $('#new_block_background_color_picker div').attr('style', 'background-color: '+background_c);

}


function setDefaultStyleInQuestionDesign(default_question_style){
    console.log(default_question_style);
    var font = (default_question_style[3]).split(':'); // font-family: Times New Roman
    var font_family = $.trim(font[1]);

    var font_sty = (default_question_style[4]).split(':'); // color: #cec4fe
    var font_style = $.trim(font_sty[1]);

    var font_color = (default_question_style[5]).split(':'); // color: #cec4fe
    var color = $.trim(font_color[1]);

    switch(font_family){
        case 'Lato':
            font_family = 'lato';
            break;
        case 'Times New Roman':
            font_family = 'time_new_roman';
            break;
        case 'Arial':
            font_family = 'arial';
            break;
        case 'Helvetica':
            font_family = 'helvetica';
            break;
        case 'Courier New':
            font_family = 'courier_new';
            break;
    }

    switch(font_style){
        case 'Normal':
            font_style = 'normal';
            break;
        case 'Italica':
            font_style = 'italic';
            break;
        case 'Oblicua':
            font_style = 'oblique';
            break;
    }

    $('#new_question_font option[value='+font_family+']').prop("selected", true);

    $('#new_question_font_style option[value='+font_style+']').prop("selected", true);

    $('#new_question_font_color_picker div').attr('style', 'background-color: '+color);

}

function setDefaultStyleInQuestionDesignUpdate(default_question_style){
    console.log(default_question_style);
    var font = (default_question_style[3]).split(':'); // font-family: Times New Roman
    var font_family = $.trim(font[1]);

    var font_sty = (default_question_style[4]).split(':'); // color: #cec4fe
    var font_style = $.trim(font_sty[1]);

    var font_color = (default_question_style[5]).split(':'); // color: #cec4fe
    var color = $.trim(font_color[1]);

    switch(font_family){
        case 'Lato':
            font_family = 'lato';
            break;
        case 'Times New Roman':
            font_family = 'time_new_roman';
            break;
        case 'Arial':
            font_family = 'arial';
            break;
        case 'Helvetica':
            font_family = 'helvetica';
            break;
        case 'Courier New':
            font_family = 'courier_new';
            break;
    }

    switch(font_style){
        case 'Normal':
            font_style = 'normal';
            break;
        case 'Italica':
            font_style = 'italic';
            break;
        case 'Oblicua':
            font_style = 'oblique';
            break;
    }

    $('#update_question_font option[value='+font_family+']').prop("selected", true);

    $('#update_question_font_style option[value='+font_style+']').prop("selected", true);

    $('#update_question_font_color_picker div').attr('style', 'background-color: '+color);

    var survey_has_question_style = checkIfSurveyHasQuestionsStyle();

    if(survey_has_question_style){
        $('#apply_design_to_all_questions_update').prop('disabled', true);
    }

}




function rgb2hex(rgb){
 rgb = rgb.match(/^rgba?[\s+]?\([\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?/i);
 return (rgb && rgb.length === 4) ? "#" +
  ("0" + parseInt(rgb[1],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[2],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[3],10).toString(16)).slice(-2) : '';
}


function set_current_operation_active(){
    $('#current_element_active').val('True');
}

function set_current_operation_inactive(){
    $('#current_element_active').val('False');
    $('#main-configuration-panel').removeClass('hidden');
    $('#question-questions-block-configuration-panel').addClass('hidden');
    $('#add-question-option-panel').addClass('hidden');
    $('#add-new-question-configuration-panel').addClass('hidden');
    $('#update-question-configuration-panel').addClass('hidden');
    $('#update-survey-block').addClass('hidden');
}

function checkIfExistsCurrentOperation(){
    var current_operation = $('#current_element_active').val();
    if(current_operation == 'True'){
        bootbox.dialog({
            message: "Actualmente esta editando otro elemento, ¿Desea cancelar el proceso y continuar?",
            title: "Ayuda de Xindex",
            buttons: {
                success: {
                    label: "Volver",
                    className: "btn-white",
                    callback: function () {
                        return false;
                    }
                },
                main: {
                    label: "Aceptar",
                    className: "btn-twitter",
                    callback: function () {
                        return true;
                    }
                }
            }
        });
    }
}

function buildSurveyStyle(){
    var survey_style,
        border_color,
        border_style,
        border_width,
        background_color,
        box_shadow = '0px 0px 5px #cecece';

    if($('#survey_has_border').is(':checked')){
        border_color = 'rgba(255, 255, 255, 0)';
        border_style = 'solid';
        border_width = '0px';
    } else{
        border_color = rgb2hex($('#survey_border_color_picker div').css('background-color'));
        border_style = $('#survey_border_style').val();
        border_width = $('#survey_border_width').val();
    }

    if($('#survey_has_background').is(':checked')){
        background_color = 'rgba(255, 255, 255, 0)';
    } else {
        background_color = rgb2hex($('#survey_background_color_picker div').css('background-color'));
    }

    if($('#survey_has_shadow').is(':checked')){
        box_shadow = '0px 0px 0px #FFFFFF';
    }

    survey_style = 'border-color: '+border_color+'; border-style: '+border_style+'; border-width: '+border_width+'; background-color: '+background_color+'; box-shadow: '+box_shadow+';';

    $('#survey_global_content').attr('style', survey_style);

}

function getSurveyStyle(){
    var border_color = $('#configured_survey_border_color').val(),
        border_style = $('#configured_survey_border_style').val(),
        border_width = $('#configured_survey_border_width').val(),
        background_color = $('#configured_survey_background_color').val(),
        box_shadow = $('#configured_survey_box_shadow').val();

    if(border_color == 'rgba(255, 255, 255, 0)' & border_style == 'solid' & border_width == '0px'){
        $('#survey_has_border').attr('checked', true);
        $('#survey_has_border_icon').addClass('checked');
    } else {
        $('#survey_border_color_picker div').css('background-color', border_color);
        $('#survey_border_style option[value="'+border_style+'"]').prop('selected', true);
        $('#survey_border_width option[value="'+border_width+'"]').prop('selected', true);
    }

    if(background_color == 'rgba(255, 255, 255, 0)'){
        $('#survey_has_background').attr('checked', true);
        $('#survey_has_background_icon').addClass('checked');
    } else {
        $('#survey_background_color_picker div').css('background-color', background_color);
    }

    if(box_shadow == 'rgb(255, 255, 255) 0px 0px 0px 0px'){
        $('#survey_has_shadow').attr('checked', true);
        $('#survey_has_shadow_icon').addClass('checked');
    }

    var survey_style = 'border-color: '+border_color+'; border-style: '+border_style+'; border-width: '+border_width+'; background-color: '+background_color+'; box-shadow: '+box_shadow+';';

    $('#survey_global_content').attr('style', survey_style);

}

function setDefaultTextBlockStyleInDesign(default_style){
    var border = (default_style[0]).split(' '); // border: 1px solid #cecece !important
    var border_width = $.trim(border[1]),
        border_style = $.trim(border[2]),
        border_color = $.trim(border[3]);

    var font = (default_style[1]).split(':'); // font-family: Times New Roman
    var font_family = $.trim(font[1]);

    var font_color = (default_style[2]).split(':'); // color: #cec4fe

    var color = $.trim(font_color[1]);

    var background_color = (default_style[3]).split(':'); // background-color: #cec6d7

    var background_c = $.trim(background_color[1]);




    switch(font_family){
        case 'Lato':
            font_family = 'lato';
            break;
        case 'Times New Roman':
            font_family = 'time_new_roman';
            break;
        case 'Arial':
            font_family = 'arial';
            break;
        case 'Helvetica':
            font_family = 'helvetica';
            break;
        case 'Courier New':
            font_family = 'courier_new';
            break;
    }

    $('#update_text_block_font option[value='+font_family+']').prop("selected", true);


    $('#update_text_block_color_picker div').attr('style', 'background-color: '+color);
    if(border_width == '0px' & border_style == 'solid' & border_color == '#FFFFFF'){
        $('#update_text_block_has_border').prop('checked', true);
        $('#update_text_block_has_border_icon').addClass('checked');
        $('#border_update_text_block_configuration_section').slideUp(200);
    }

    $('#update_text_block_border_color_picker div').attr('style', 'background-color: '+border_color);

    $('#update_text_block_border_style option[value='+border_style+']').prop("selected", true);

    $('#update_text_block_border_width option[value='+border_width+']').prop('selected', true);

    if(background_c == 'rgba(255, 255, 255, 0)'){
        $('#update_text_block_has_background').attr('checked', true);
        $('#update_text_block_has_background_icon').addClass('checked');
        $('#update_text_block_background_configuration_section').slideUp(200);
    }

    $('#update_text_block_background_color_picker div').attr('style', 'background-color: '+background_c);
}

function showDefaultButtons(){
    $('div.default-buttons').slideDown(300);
    $('#survey-main-content a.add-question-to-block').each(function () {
        $(this).closest('footer').slideDown(300);
    });
}

function hideDefaultButtons(){
    $('div.default-buttons').slideUp(300);
    $('#survey-main-content a.add-question-to-block').each(function () {
        $(this).closest('footer').slideUp(300);
    });
}

function get_questions_block_structure(){
    //check if survey has blocks style by default
    var hasBlocksStyle = checkIfSurveyHasBlocksStyle();
    var blocks_style;
    if(hasBlocksStyle){
        //TO DO: fix this, recover the style from db with this function
        //blocks_style = getSurveyBlocksStyle();
        blocks_style = $('#survey_blocks_style').val();
        setDefaultStyle();
        //disable check box to apply style to all blocks
        $('#apply_design_to_all_blocks').prop('disabled', true);
    } else {
        blocks_style = 'border: 1px solid #cecece !important; font-family: Lato; color: #717171; background-color: rgba(255, 255, 255, 0);';

        setDefaultStyleInDesign((blocks_style).split(';'));
    }

    var new_questions_block_content = '<div class="row row-block questions-block animated fadeInDown" id="">' +
        '<div class="col-lg-12">' +
        '<section class="padder padder-v question-block selected-block" data-toggle="tooltip" data-placement="right" title="" data-original-title="Arrastre para cambiar la pocisión del bloque" style="'+blocks_style+'">' +
        '<input type="hidden" class="block_moment_associated_id false">'+
        '<div class="block_actions_content" style="height: 25px; min-height: 25px;">'+
            '<div class="block_actions">'+
                '<a class="actions_block remove_block" id="remove_block">'+
                    '<i class="icon-trash icon-large pull-right"></i>'+
                '</a>'+
                '<a class="actions_block update_block" id="update_block">'+
                    '<i class="icon-edit icon-large pull-right"></i>'+
                '</a>'+
            '</div>'+
        '</div>'+
        '<div class="panel-body">' +
        '<div>' +
        '<header class="block-title">' +
        'Titulo' +
        '</header>' +
        '<small class="block-description">' +
        '<p>' +
        'Este contenido es editable' +
        '</p>' +
        '</small>' +
        '</div>' +
        '</div>' +
        '<ul class="list-group no-bg gutter list-group-lg list-group-sp sortable" id="sortable_question_list">'+
        '</ul>'+
        '<footer class="wrapper text-center" style="display: none;">' +
        '<a class="btn btn-info wrapper add-question-to-block">' +
        '<i class="icon-plus-sign-alt"></i>' +
        'Da click aquí para añadir una pregunta' +
        '</a>' +
        '</footer>' +
        '</section>' +
        '</div>' +
        '</div>';

    return new_questions_block_content;
}

function get_question_block_structure(){
    var survey_has_question_style = checkIfSurveyHasQuestionsStyle();

    var questions_style = 'display: table; min-width: 100%; min-height: 50px; font-family: Lato; font-style: normal; color: #717171;';

    if(survey_has_question_style){
        questions_style = getSurveyQuestionsStyle();
        setDefaultStyleInQuestionDesign((questions_style).split(';'));

        $('#apply_design_to_all_questions').prop('disabled', true);
    }

    var new_questions_block_content =
        '<div class="row row-block row-no-block question-block animated" id="">' +
            '<div class="col-lg-12">' +
                '<section class="padder padder-v question-block selected-block" data-toggle="tooltip" data-placement="right" title="" data-original-title="Arrastre para cambiar la pocisión del bloque" style="border: 0px solid #FFFFFF !important; font-family: Lato; color: #717171; background-color: rgba(255, 255, 255, 0);">' +
                    '<input type="hidden" class="block_moment_associated_id false">'+
                    /*
                     '<div class="wrapper question-blocks-content">' +
                     '</div>' +*/
                    '<div class="wrapper question-content block-question active-question" style="'+questions_style+'">'+
                        '<div class="question_actions_content wrapper b-b bg-gradient" style="height: 30px; min-height: 30px;">'+
                            '<div class="question_actions">'+
                                '<strong class="actions pull-left">'+
                                    '<a class="actions_question remove_question" id="remove_block">'+
                                        '<i class="icon-trash icon-sm pull-left"></i>'+
                                    '</a>'+
                                    '<a class="actions_question update_question" id="update_block">'+
                                        '<i class="icon-edit icon-sm pull-left"></i>'+
                                    '</a>'+
                                '</strong>'+
                                '<small class="pull-right padder text-dark attribute_info"><strong class="text-black">Atributo: </strong>" Sin asignar " </small>'+
                                '<small class="pull-right text-dark moment_info"><strong class="text-black"> Momento: </strong>" Sin asignar "</small>'+
                            '</div>'+
                        '</div>'+
                        '<div class="question_id" style="float:left;"></div>'+
                        '<div class="question-text" style="float: left; margin-left: 5px; display: table;">Texto de la pregunta</div>'+
                        '<div class="optional-content" style="margin-top: 15px;"></div>'+
                        '<div class="db_question_id"></div>'+
                    '</div>' +
                '</section>' +
            '</div>' +
        '</div>';

    return new_questions_block_content;
}