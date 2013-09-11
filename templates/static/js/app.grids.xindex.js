/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 6/09/13
 * Time: 01:07 PM
 * To change this template use File | Settings | File Templates.
 */
$(window).ready(function(){

    alert("asdasdasd");
    var data_url, table_grid;

    if($('#MyStretchGrid')[0]){
        subsidiariesDatagrid();
    } else if($('#mySTGrid')[0]){
        subsidiaryTypesDatagrid();
    } else if($('#myBUGrid')[0]){
        alert('hdkjasgfdgdsffgdsg')
        businessUnitsDatagrid();
    } else if($('#mySGrid')[0]){
        servicesDatagrid();
    } else if($('#myComGrid')[0]){
        alert('compañias')
        companiesDatagrid();
    }
})