$(window).ready(function(){

    alert(".ready");
    var data_url, table_grid;

    if($('#MyStretchGrid')[0]){
        alert('subsidiaries');
        subsidiariesDatagrid();
    } else if($('#mySTGrid')[0]){
        alert('subsidiarytypes');
        subsidiaryTypesDatagrid();
    } else if($('#myBUGrid')[0]){
        alert('bussinesunits')
        businessUnitsDatagrid();
    } else if($('#mySGrid')[0]){
        alert('services');
        servicesDatagrid();
    } else if($('#myComGrid')[0]){
        alert('companies')
        companiesDatagrid();
    }
})