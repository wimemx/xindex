/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 18/12/13
 * Time: 11:31 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){
    //tiny mce instance to edit privacy notice
    tinymce.init({
        selector: "textarea#id_text-area-field",
        theme: "modern",
        width: '80%',
        height: 200,
        autoresize_min_height: 200,
        autoresize_max_height: 500,
        language : 'es',
        language_url : '/langs/es.js',
        plugins: [
            "autolink lists charmap preview hr anchor pagebreak spellchecker",
            "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime nonbreaking",
            "save table contextmenu directionality template paste textcolor"
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
            ed.on('keyup change', function (e) {
                var content = tinymce.get('id_text-area-field').getContent();
                $('#field-content').html(content);
            });
        }


    });

    $('#btn-send-form').on('click', function(){

        var privacy_content = tinymce.get('id_text-area-field').getContent();
        $('#id_text-area-field').val(privacy_content);
        var serialize = $('#module-form').serializeArray();
        $('#module-form').submit();
        //serialize.push({name: "id_privacy_notice", value: privacy_content});
        /*
        $.ajax({
            url: $('#privacy-notice-form').attr('action'),
            type: 'POST',
            data: serialize,
            dataType: 'Json',
            success: function (msg) {
                alert(msg);
            },
            error: function (msg_error) {
                alert(msg_error.error);
            }
        });
        */
    });



})