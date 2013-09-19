$(document).ready(function () {

    var data_url, table_grid;

    if ($('#MyStretchGrid')[0]) {
        subsidiariesDatagrid();
    } else if ($('#mySTGrid')[0]) {
        subsidiaryTypesDatagrid();
    } else if ($('#myBUGrid')[0]) {
        businessUnitsDatagrid();
    } else if ($('#mySGrid')[0]) {
        servicesDatagrid();
    } else if ($('#myComGrid')[0]) {
        companiesDatagrid();
    } else if ($('#myAttributesGrid')[0]) {
        attributesDatagrid();
    } else if ($('#mySurveysGrid')[0]) {
        surveysDatagrid();
    }
});