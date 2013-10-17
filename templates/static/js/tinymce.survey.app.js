/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 14/10/13
 * Time: 09:54 AM
 * functions to create tiny mce instances
 */

$(document).ready(function () {

    //tiny mce instance to create block description
    tinymce.init({
        selector: "textarea#tinymce-editor",
        theme: "modern",
        width: '100%',
        height: 300,
        autoresize_min_height: 300,
        autoresize_max_height: 500,
        language : 'es',
        language_url : '/langs/es.js',
        plugins: [
            "autoresize advlist autolink link lists charmap print preview hr anchor pagebreak spellchecker",
            "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime nonbreaking",
            "save table contextmenu directionality emoticons template paste textcolor"
        ],
        toolbar: "insertfile undo redo | styleselect | bold italic| Red header | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor emoticons",
        style_formats: [
            {title: 'Bold text', inline: 'b'},
            {title: 'Red text', inline: 'span', styles: {color: '#ff0000'}},
            {title: 'Red header', block: 'h1', styles: {color: '#ff0000'}},
            {title: 'Titulo 1', block: 'h1', styles: {color: '#cecece'}},
            {title: 'Titulo 2', block: 'h2', styles: {color: '#cecece'}},
            {title: 'Titulo 3', block: 'h3', styles: {color: '#cecece'}},
            {title: 'Titulo 4', block: 'h4', styles: {color: '#cecece'}},
            {title: 'Titulo 5', block: 'h5', styles: {color: '#cecece'}},
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


    //tiny mce instance to update block description
    tinymce.init({
        selector: "textarea#tinymce-editor-update-block",
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
            ed.on('keyup change', function (e) {
                var content = ed.getContent();
                var current_text_block_id = $('#current-text-block-updated').val();
                $('#' + current_text_block_id + ' div.panel-body').html('');
                $('#' + current_text_block_id + ' div.panel-body').html(content);
            });
        }
    });

    //TODO: Delete this, now its implemented with text area
    //tiny mce instance to update question text
    tinymce.init({
        selector: "textarea#tinymce-editor-update-question",
        theme: "modern",
        width: '100%',
        height: 50,
        autoresize_min_height: 50,
        autoresize_max_height: 50,
        entities: "160,nbsp,38,amp,34,quot,162,cent,8364,euro,163,pound,165,yen,169,copy,174,reg,8482,trade,8240,permil,60,lt,62,gt,8804,le,8805,ge,176,deg,8722,minus",
        entity_encoding: "raw",
        plugins: [
            "autoresize paste textcolor"
        ],
        setup: function (ed) {
            ed.on('keyup', function (e) {
                var con = ed.getContent();
                var content = con.replace(/(<([^>]+)>)/ig, "");
                var current_question = $('#current-question-updated').val();
                $('#' + current_question + ' div.question-text').html('');
                $('#' + current_question + ' div.question-text').html(content);

                $('.question_title_updated').val(content);
            })
            ed.on('change', function (e) {
                var con = ed.getContent();
                var content = con.replace(/(<([^>]+)>)/ig, "");
                var current_question = $('#current-question-updated').val();
                $('#' + current_question + ' div.question-text').html('');
                $('#' + current_question + ' div.question-text').html(content);

                $('.question_title_updated').val(content);
            })
        }
    });

})
