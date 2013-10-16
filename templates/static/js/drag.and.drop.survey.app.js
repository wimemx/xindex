/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 14/10/13
 * Time: 10:53 AM
 * To change this template use File | Settings | File Templates.
 */

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
        //support[api].className = 'hidden';
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


//<--------------  DRAG AND DROP QUESTION  BLOCK--------->//

function drop(e) {
    e.preventDefault();
}
function dragQuestionBlock(e) {
    e.dataTransfer.setData("Text", e.target.attr("id"));
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

    //var id = $(e.target).attr("id");
    //alert(id);
    /*Funcion para insertar preguntas sin bloque*/
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
}

function revertDraggable($selector) {
    $selector.each(function() {
        var $this = $(this),
            position = $this.data("originalPosition");

        if (position) {
            $this.animate({
                left: position.left,
                top: position.top
            }, 500, function() {
                $this.data("originalPosition", null);
            });
        }
    });
}
