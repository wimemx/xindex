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
    } else if ($('#myZonesGrid')[0]) {
        zonesDatagrid();
    } else if ($('#myULGrid')[0]) {
        userListDatagrid();
    } else if ($('#myCGrid')[0]) {
        clientListDatagrid();
    } else if ($('#mySubsidiaryGrid')[0]) {
        subsidiariesDatagrid();
    } else if ($('#mySubsidiaryDetailsGrid')[0]) {
        var id = $('#id-subsidiary-grid').val();
        subsidiaryDetailsDatagrid(id);
    } else if ($('#myClientActivityGrid')[0]) {
        var client = $('#client-id').val();
        clientActivityDatagrid(client);
    }
});