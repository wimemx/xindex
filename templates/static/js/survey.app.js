/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 20/09/13
 * Time: 09:44 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {




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


    /*Funciones para insertar bloques de preguntas*/
    $('#add-block-questions').on('click', function () {

        $('div.default-buttons').fadeOut(300);

        var new_questions_block_content = '<div class="row animated rollIn" id="block-1">' +
                '<div class="col-lg-12">' +
                    '<section class="question-block selected-block">' +
                        '<div class="panel-body">' +
                            '<div>'+
                            '<header class="">' +
                                'Este es el nombre del bloque de preguntas' +
                            '</header>' +
                            '<small class="">' +
                                '<p>' +
                                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.' +
                                '</p>' +
                            '</small>' +
                            '</div>'+
                        '</div>' +
                        '<footer class="wrapper text-center">'+
                            '<a class="btn btn-info wrapper add-question-to-block">' +
                                'Da click aquí para añadir una pregunta' +
                            '</a>'+
                        '</footer>'+
                    '</section>' +
                '</div>' +
            '</div>';

        $('#survey-main-content').append(new_questions_block_content);

        $('#current-question-block').val('block-1');

        tinymce.get('tinymce-editor').setContent(
            '<div>'+
            '<header class="">' +
            'Este es el nombre del bloque de preguntas' +
            '</header>' +
            '<small class="">' +
            '<p>' +
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.' +
            '</p>' +
            '</small>'+
            '</div>'
        );
    });


    /*TinyMCE*/
    tinymce.init({
        selector: "textarea#tinymce-editor",
        theme: "modern",
        width: '100%',
        height: 300,
        autoresize_min_height: 300,
        autoresize_max_height: 500,
        init_instance_callback: function (inst) {
            inst.execCommand('mceAutoResize');
        },
        plugins: [
            "autoresize advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
            "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
            "save table contextmenu directionality emoticons template paste textcolor"
        ],
        content_css: "css/content.css",
        toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | l      ink image | print preview media fullpage | forecolor backcolor emoticons",
        style_formats: [
            {title: 'Bold text', inline: 'b'},
            {title: 'Red text', inline: 'span', styles: {color: '#ff0000'}},
            {title: 'Red header', block: 'h1', styles: {color: '#ff0000'}},
            {title: 'Example 1', inline: 'span', classes: 'example1'},
            {title: 'Example 2', inline: 'span', classes: 'example2'},
            {title: 'Table styles'},
            {title: 'Table row 1', selector: 'tr', classes: 'tablerow1'}
        ],
        setup: function (ed) {
            ed.on('keyup', function (e) {
                var content = tinymce.get('tinymce-editor').getContent();
                var current_question_block = $('#current-question-block').val();
                $('#'+current_question_block+' div.panel-body').html('');
                $('#'+current_question_block+' div.panel-body').html(content);
            })
            ed.on('change', function (e) {
                var content = tinymce.get('tinymce-editor').getContent();
                var current_question_block = $('#current-question-block').val();
                $('#'+current_question_block+' div.panel-body').html('');
                $('#'+current_question_block+' div.panel-body').html(content);

            })
        }


    });

    $(document).on('click', 'a.add-question-to-block', function(){
        //$(this).closest('.col-lg-12').
    });



})