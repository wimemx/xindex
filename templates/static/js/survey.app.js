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


    /*Funciones para insertar bloques de preguntas*/
    $('#add-block-questions').on('click', function () {

        $('#main-configuration-panel').addClass('hidden');
        $('#questions-block-configuration-panel').removeClass('hidden');

        $('div.default-buttons').fadeOut(300);

        var new_questions_block_content = '<div class="row animated rollIn" id="block-1">' +
            '<div class="col-lg-12">' +
            '<section class="padder padder-v question-block selected-block">' +
            '<div class="panel-body">' +
            '<div>' +
            '<header class="">' +
            'Este es el nombre del bloque de preguntas' +
            '</header>' +
            '<small class="">' +
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

        $('#current-question-block').val('block-1');

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
        plugins: [
            "autoresize paste textcolor"
        ],
        setup: function (ed) {
            ed.on('keyup', function (e) {
                var content = tinymce.get('tinymce-editor-new-question').getContent();
                var current_question = $('#current-question').val();
                $('#' + current_question + ' div.question-text').html('');
                $('#' + current_question + ' div.question-text').html(content);
            })
            ed.on('change', function (e) {
                var content = tinymce.get('tinymce-editor-new-question').getContent();
                var current_question = $('#current-question').val();
                $('#' + current_question + ' div.question-text').html('');
                $('#' + current_question + ' div.question-text').html(content);

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

        $('<div class="wrapper question-content active-question" style="display: table; min-width: 100%; min-heigth: 50px;"><div class="question_id" style="float:left;"></div><div class="question-text" style="float: left; margin-left: 5px; display: table;">Texto de la pregunta</div><div class="optional-content" style="margin-top: 15px;"></div></div>').insertBefore($(this).parent());

        /*Find question id*/
        $('#survey-main-content div.question-content').each(function (index) {
            $(this).attr('id', 'question-' + (index + 1));
            $(this).children('div.question_id').text(index + 1+'.- ');
        })
        /*end*/

    })

    $('a.btn-create-new-question').on('click', function () {
        $('#survey-main-content div.question-content').each(function (index) {
            $(this).attr('id', 'question-' + (index + 1));
            $(this).children('div.question_id').text(index + 1+'.- ');
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
    holder.innerHTML += '<p>Uploaded ' + file.name + ' ' + (file.size ? (file.size/1024|0) + 'K' : '');
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
      xhr.onload = function() {
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
  holder.ondragover = function () { this.className = 'hover'; return false; };
  holder.ondragend = function () { this.className = ''; return false; };
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
