/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 20/09/13
 * Time: 09:44 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {

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


    /*Funciones para insertar bloques de preguntas*/
    $('#add-block-questions').on('click', function () {

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
            /*
             '<div class="wrapper question-blocks-content">' +
             '</div>' +*/
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

        var block_selected_id = $('#survey-main-content').find('section.selected-block').closest('div.row').attr('id')

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
    });


    /*Funcion para insertar preguntas sin bloque*/
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


    /*TinyMCE*/
    tinymce.init({
        selector: "textarea#tinymce-editor",
        theme: "modern",
        width: '100%',
        height: 300,
        autoresize_min_height: 300,
        autoresize_max_height: 500,
        plugins: [
            "autoresize advlist autolink link lists charmap print preview hr anchor pagebreak spellchecker",
            "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime nonbreaking",
            "save table contextmenu directionality emoticons template paste textcolor"
        ],
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
                $('#' + current_question_block + ' div.panel-body').html('');
                $('#' + current_question_block + ' div.panel-body').html(content);
            })
            ed.on('change', function (e) {
                var content = tinymce.get('tinymce-editor').getContent();
                var current_question_block = $('#current-question-block').val();
                $('#' + current_question_block + ' div.panel-body').html('');
                $('#' + current_question_block + ' div.panel-body').html(content);

            })
        }


    });


    /*TinyMCE*/
    tinymce.init({
        selector: "textarea#tinymce-editor-new-question",
        theme: "modern",
        width: '100%',
        height: 50,
        autoresize_min_height: 50,
        autoresize_max_height: 100,
        entities: "160,nbsp,38,amp,34,quot,162,cent,8364,euro,163,pound,165,yen,169,copy,174,reg,8482,trade,8240,permil,60,lt,62,gt,8804,le,8805,ge,176,deg,8722,minus",
        entity_encoding: "raw",
        plugins: [
            "autoresize paste textcolor"
        ],
        setup: function (ed) {
            ed.on('keyup', function (e) {
                var con = ed.getContent();
                var content = con.replace(/(<([^>]+)>)/ig, "");
                var current_question = $('#current-question').val();
                $('#' + current_question + ' div.question-text').html('');
                $('#' + current_question + ' div.question-text').html(content);

                $('.question-title').val(content);

            })
            ed.on('change', function (e) {
                var con = ed.getContent();
                var content = con.replace(/(<([^>]+)>)/ig, "");
                var current_question = $('#current-question').val();
                $('#' + current_question + ' div.question-text').html('');
                $('#' + current_question + ' div.question-text').html(content);
                $('.question-title').val(content);
            })
        }
    });


    $(document).on('click', 'a.add-question-to-block', function () {
        $('#main-configuration-panel').addClass('hidden');
        $('#questions-block-configuration-panel').addClass('hidden');
        $('#add-question-option-panel').removeClass('hidden');

        $(this).closest('footer').fadeOut(400);

        var before = $(this)[0];

        var new_question_block = '';

        var parent_block = '';

        $('<div class="wrapper question-content active-question" style="display: table; min-width: 100%; min-heigth: 50px;"><div class="question_id" style="float:left;"></div><div class="question-text" style="float: left; margin-left: 5px; display: table;">Texto de la pregunta (Esta pregunta no se guardara en la configuraci&oacute;n hasta que sea guardad)</div><div class="optional-content" style="margin-top: 15px;"></div><div class="db_question_id"></div></div>').insertBefore($(this).parent());

        /*Find question id*/
        $('#survey-main-content div.question-content').each(function (index) {
            $(this).attr('id', 'question-' + (index + 1));
            $(this).children('div.question_id').text(index + 1 + '.- ');
        })
        /*end*/

    })

    $('a.btn-create-new-question').on('click', function () {
        $('#survey-main-content div.question-content').each(function (index) {
            $(this).attr('id', 'question-' + (index + 1));
            $(this).children('div.question_id').text(index + 1 + '.- ');
            if ($(this).hasClass('active-question')) {

                var question_id = $(this).attr('id');
                var current_question_text = $(this).children('div.question-text').text();

                $('#current-question').val(question_id);

                tinymce.get('tinymce-editor-new-question').setContent(current_question_text);

                $('#add-new-question-configuration-panel').removeClass('hidden');
                $('#add-question-option-panel').addClass('hidden');

            }
        })
    });

    $('#question-type a').on('click', function (e) {
        e.preventDefault();
        var question_type = $(this).attr('id');
        switch (question_type) {
            case '1':

                break;
            case '2':

                break;
            case '3':

                break;
            case '4':

                break;
            case '5':

                break;
            default:
                break;
        }
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


    $('#save-survey-question-block').on('click', function (e) {
        e.preventDefault();
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

            $('#main-configuration-panel').addClass('hidden');
            $('#add-question-option-panel').addClass('hidden');
            $('#add-new-question-configuration-panel').removeClass('hidden');
            $('#questions-block-configuration-panel').addClass('hidden');

            $('#survey-main-content div.question-content').each(function () {
                $(this).removeClass('active-question');
            });

            $(this).closest('div.question-content').addClass('active-question');

            var question_id = $(this).closest('div.question-content').find('div.db_question_id').attr('id');

            console.log(question_id)

            $('#current-question').val(question_id);
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




})

//DRAG AND DROP start>>
var holder = document.getElementById('holder'),
    tests = {
        filereader: typeof FileReader != 'undefined',
        dnd: 'draggable' in document.createElement('span'),
        formdata: !!window.FormData,
        progress: "upload" in new XMLHttpRequest
    },
    support = {
        filereader: document.getElementById('filereader'),
        formdata: document.getElementById('formdata'),
        progress: document.getElementById('progress')
    },
    acceptedTypes = {
        'image/png': true,
        'image/jpeg': true,
        'image/gif': true
    },
    progress = document.getElementById('uploadprogress'),
    fileupload = document.getElementById('upload');

"filereader formdata progress".split(' ').forEach(function (api) {
    if (tests[api] === false) {
        support[api].className = 'fail';
    } else {
        support[api].className = 'hidden';
    }
});

function previewfile(file) {
    if (tests.filereader === true && acceptedTypes[file.type] === true) {
        var reader = new FileReader();
        reader.onload = function (event) {
            var image = new Image();
            image.src = event.target.result;
            image.width = 250; // a fake resize
            holder.appendChild(image);
        };

        reader.readAsDataURL(file);
    } else {
        holder.innerHTML += '<p>Uploaded ' + file.name + ' ' + (file.size ? (file.size / 1024 | 0) + 'K' : '');
        console.log(file);
    }
}

function readfiles(files) {
    debugger;
    var formData = tests.formdata ? new FormData() : null;
    for (var i = 0; i < files.length; i++) {
        if (tests.formdata) formData.append('file', files[i]);
        previewfile(files[i]);
    }

    // now post a new XHR request
    if (tests.formdata) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/devnull.php');
        xhr.onload = function () {
            progress.value = progress.innerHTML = 100;
        };

        if (tests.progress) {
            xhr.upload.onprogress = function (event) {
                if (event.lengthComputable) {
                    var complete = (event.loaded / event.total * 100 | 0);
                    progress.value = progress.innerHTML = complete;
                }
            }
        }

        xhr.send(formData);
    }
}

if (tests.dnd) {
    holder.ondragover = function () {
        this.className = 'hover';
        return false;
    };
    holder.ondragend = function () {
        this.className = '';
        return false;
    };
    holder.ondrop = function (e) {
        this.className = '';
        e.preventDefault();
        readfiles(e.dataTransfer.files);
    }
} else {
    fileupload.className = 'hidden';
    fileupload.querySelector('input').onchange = function () {
        readfiles(this.files);
    };
}

//DRAG AND DROP <<<end


//<--------------  DRAG AND DROP QUESTION  --------->//

function drop(e) {
    e.preventDefault();
}
function dragQuestionBlock(e) {
    e.dataTransfer.setData("Text", e.target.id);
}

function dropQuestionBlock(e) {
    $('#main-configuration-panel').addClass('hidden');
    $('#questions-block-configuration-panel').removeClass('hidden');

    $('div.default-buttons').fadeOut(300);

    var n = $('#survey-main-content div.row-block').length;

    $('#survey-main-content div.row-block').each(function (index) {
        $(this).find('section.question-block').removeClass('selected-block');
    });

    var new_block_id = 'block-' + (n + 1);

    var new_questions_block_content = '<div class="row row-block animated slideDown" id="' + new_block_id + '">' +
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

    var block_selected_id = $('#survey-main-content').find('section.selected-block').closest('div.row').attr('id')

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



//---- Drag and Drop Question ----//

function dropQuestion(e) {
    /*Funcion para insertar preguntas sin bloque*/
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
}




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