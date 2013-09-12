/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 12/09/13
 * Time: 01:10 PM
 * To change this template use File | Settings | File Templates.
 */

function addBusinessUnit(){
    $.ajax({

    })
}

$(document).ready(function(){
    $('#business_unit_form').on('submit', function(e){
      e.preventDefault();
      $.post('/business_unit/add',
         $('#business_unit_form').serialize(),
         function(data, status, xhr){
           alert('Yeh!')
         });

    });
})