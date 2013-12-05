/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 4/09/13
 * Time: 05:51 PM
 * To change this template use File | Settings | File Templates.
 */

var sucursales = [], zonas = [], types = [], businessUnits = [];

function subsidiariesDatagrid() {

    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/subsidiaries/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.subsidiaries;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }


                        $(".dropdown-menu.mainM li a").click(function () {
                            var selText = $(this).text();
                            switch (selText) {
                                case 'Tipo':
                                    $('#second-filter-subsidiary').children().remove();
                                    for (i = 0; i < types.length; i++) {
                                        $('#second-filter-subsidiary').append("<li data-value='" + types[i] + "' data-selected='true'><a href='#'>" + types[i] + "</a></li>")
                                    }
                                    break;
                                case 'Zona':
                                    $('#second-filter-subsidiary').children().remove();
                                    for (i = 0; i < zonas.length; i++) {
                                        $('#second-filter-subsidiary').append("<li data-value='" + zonas[i] + "' data-selected='true'><a href='#'>" + zonas[i] + "</a></li>")
                                    }
                                    break;
                            }

                        });

                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                for (i = 0; i < types.length; i++) {
                                    switch (options.filter.value){
                                        case types[i]:
                                            if (item.type == types[i]) return true;
                                            break;
                                    }
                                }
                                for (i = 0; i < zonas.length; i++) {
                                    switch (options.filter.value){
                                        case zonas[i]:
                                            if (item.zone == zonas[i]) return true;
                                            break;
                                    }
                                }
                            });
                        }

                        var count = data.length;

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar las sucursales, intente mas tarde!')
                    });
            }, self._delay);
        }
    };

    $('#mySubsidiaryGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'type',
                        label: 'Tipo de sucursal',
                        sortable: false
                    },
                    {
                        property: 'zone',
                        label: 'Zona',
                        sortable: false
                    },
                    {
                        property: 'location',
                        label: 'Ubicación',
                        sortable: false
                    },
                    {
                        property: 'subsidiaryId',
                        label: 'Acciones',
                        sortable: false
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.name = '<a href="/subsidiaries/details/'+ item.subsidiaryId +'">' + item.name + '</a>';
                        item.subsidiaryId = '<a href="/subsidiaries/edit/' + item.subsidiaryId + '" class="edit-subsidiary"><i class="icon-edit"></i></a>' +
                                            '<a href="/subsidiaries/remove/' + item.subsidiaryId + '" class="remove-subsidiary"><i class="icon-remove"></i></a>';
                        item.detalles = '<a href="/subsidiaries/details/' + item.detalles + '" ><i class="icon-eye-open"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';
                    });

                    $.each(items, function (index, item) {

                        if (types.length == 0) {
                            var type = item.type;
                            types.push(type);
                        }
                        var coincidencias = 0

                        for (var i = 0; i < types.length; i++) {
                            if (types[i] == item.type) {
                                coincidencias++;
                            }
                        }

                        if (coincidencias == 0) {
                            var type = item.types;
                            types.push(type)
                        }

                    });

                    $.each(items, function (index, item) {

                        if (zonas.length == 0) {
                            var zona = item.zone;
                            zonas.push(zona);
                        }
                        var coincidencias = 0

                        for (var i = 0; i < zonas.length; i++) {
                            if (zonas[i] == item.zone) {
                                coincidencias++;
                            }
                        }

                        if (coincidencias == 0) {
                            var zona = item.zone;
                            zonas.push(zona)
                        }

                    });
                }
            })
        });
    });
}




function subsidiaryDetailsDatagrid(id) {

    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/subsidiaries/details/json/'+id
            var self = this;

            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.services;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }



                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                for (i = 0; i < businessUnits.length; i++) {
                                    switch (options.filter.value){
                                        case businessUnits[i]:
                                            if (item.business_name == businessUnits[i]) return true;
                                            if (options.filter.value == 'default'){
                                                data = response.services;
                                                return true;
                                            }
                                            break;
                                        //default :
                                          //  return true;
                                          //  break;

                                    }
                                }
                            });
                        }

                        var count = data.length;

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar los detalles de la sucursal, intente mas tarde!')
                    });
            }, self._delay);
        }
    };

    $('#mySubsidiaryDetailsGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'service_name',
                        label: 'Servicio',
                        sortable: true
                    },
                    {
                        property: 'business_name',
                        label: 'Unidad de servicio',
                        sortable: false
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {

                    $.each(items, function (index, item) {
                        item.business_name = item.business_name + '';
                    });

                    $.each(items, function (index, item) {

                        if (businessUnits.length == 0) {
                            var bu = item.business_name;
                            businessUnits.push(bu);
                        }
                        var coincidencias = 0;

                        for (var i = 0; i < businessUnits.length; i++) {
                            if (businessUnits[i] == item.business_name) {
                                coincidencias++;
                            }
                        }

                        if (coincidencias == 0) {
                            var bu = item.business_name;
                            businessUnits.push(bu);
                            //$('#second-filter-details').children().remove();
                            for (i = 0; i < businessUnits.length; i++) {
                                $('#second-filter-details').append("<li data-value='" + businessUnits[i] + "' data-selected='true'><a href='#'>" + businessUnits[i] + "</a></li>");


                            }

                        }

                    });
                }
            })
        });
    });
}






function subsidiaryTypesDatagrid() {
    // fuelux subsidiaries datagrid
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/subsidiary_types/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.s_types;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                switch (options.filter.value) {
                                    case 'lt5m':
                                        if (item.population < 5000000) return true;
                                        break;
                                    case 'gte5m':
                                        if (item.population >= 5000000) return true;
                                        break;
                                    default:
                                        return true;
                                        break;
                                }
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar los tipos de sucursales, intente mas tarde!')
                    });
            }, self._delay);
        }
    };

    $('#mySTGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'description',
                        label: 'Descripción',
                        sortable: false
                    },
                    {
                        property: 'st_del',
                        label: 'Acciones'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.name = '<a href="/subsidiary_types/details/' + item.st_det + '">' + item.name + '</a>';
                        item.st_del = '<a href="/subsidiary_types/update/' + item.st_up + '" class="edit-subType" data-toggle="ajaxModal"><i class="icon-edit"></i></a>' +
                            '<a href="/subsidiary_types/remove/' + item.st_del + '" class="remove-subsidiaryType"><i class="icon-remove"></i></a>';
                    });
                }
            })
        });
    });
}

function businessUnitsDatagrid() {
    // fuelux subsidiaries datagrid
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };


    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {

            var url = '/business_units/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.business_u;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        $(".dropdown-menu.mainM li a").click(function () {
                            var selText = $(this).text();
                            switch (selText) {
                                case 'Sucursal':
                                    $('#second-filter').children().remove();
                                    for (i = 0; i < sucursales.length; i++) {
                                        $('#second-filter').append("<li data-value='" + sucursales[i] + "' data-selected='true'><a href='#'>" + sucursales[i] + "</a></li>")
                                    }
                                    break;
                                case 'Zona':
                                    $('#second-filter').children().remove();
                                    for (i = 0; i < zonas.length; i++) {
                                        $('#second-filter').append("<li data-value='" + zonas[i] + "' data-selected='true'><a href='#'>" + zonas[i] + "</a></li>")
                                    }
                                    break;
                            }

                        });

                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                for (i = 0; i < sucursales.length; i++) {
                                    switch (options.filter.value){
                                        case sucursales[i]:
                                            if (item.subsidiary == sucursales[i]) return true;
                                            break;
                                    }
                                }
                                for (i = 0; i < zonas.length; i++) {
                                    switch (options.filter.value){
                                        case zonas[i]:
                                            if (item.zone == zonas[i]) return true;
                                            break;
                                    }
                                }

                                /*
                                switch (options.filter.value) {

                                    case 'Sucursal':
                                        if (item.subsidiary == 'Sucursal 1') return true;
                                        break;
                                    case 'Zona':
                                        if (item.subsidiary == 'Subsidiaria 2') return true;
                                        break;
                                    default:
                                        return true;
                                        break;
                                }*/
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar las unidades de servicio!')
                    });
            }, self._delay);
        }
    };

    $('#myBUGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'subsidiary',
                        label: 'Sucursales',
                        sortable: false
                    },
                    {
                        property: 'business_unit_id',
                        label: 'Opciones',
                        sortable: false
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        var buid = item.business_unit_id;
                        var subid = item.subsidiary_id;
                        item.name = '<a href="/services/' + buid + '">' + item.name + '</a>';
                        item.business_unit_id =
                            '<a href="/business_units/update/' + item.business_unit_id + '" class="update_bu" data-toggle="ajaxModal"><i class="icon-edit"></i></a>'
                                +
                                '<label>|</label>'
                                +
                            '<a href="/business_units/' + item.business_unit_id + '/remove" class="remove-business-unit"><i class="icon-remove"></i></a>';
                        //c = (item.active == true) ? "checked" : ""    ARRIBA + item.subsidiary_id + '/'
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';

                    });

                    $.each(items, function (index, item) {

                        if (sucursales.length == 0) {
                            var sucursal = item.subsidiary;
                            sucursales.push(sucursal);
                        }
                        var coincidencias = 0

                        for (var i = 0; i < sucursales.length; i++) {
                            if (sucursales[i] == item.subsidiary) {
                                coincidencias++;
                            }
                        }

                        if (coincidencias == 0) {
                            var sucursal = item.subsidiary;
                            sucursales.push(sucursal)
                        }

                    });

                    $.each(items, function (index, item) {

                        if (zonas.length == 0) {
                            var zona = item.zone;
                            zonas.push(zona);
                        }
                        var coincidencias = 0

                        for (var i = 0; i < zonas.length; i++) {
                            if (zonas[i] == item.zone) {
                                coincidencias++;
                            }
                        }

                        if (coincidencias == 0) {
                            var zona = item.zone;
                            zonas.push(zona)
                        }

                    });

                }

                //Crear filtros


            })
        });
    });
}


function servicesDatagrid() {
    // fuelux subsidiaries datagrid
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {

            if($('#business_unit_id')[0]){
                var business_unit_id = $('#business_unit_id').val();
                var url = '/services/json/'+business_unit_id
            } else {
                var url = '/services/json/'
            }
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.services;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                switch (options.filter.value) {
                                    case 'lt5m':
                                        if (item.population < 5000000) return true;
                                        break;
                                    case 'gte5m':
                                        if (item.population >= 5000000) return true;
                                        break;
                                    default:
                                        return true;
                                        break;
                                }
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar los servicios!')
                    });
            }, self._delay);
        }
    };

    $('#mySGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'business_unit',
                        label: 'Unidad de servicio',
                        sortable: false
                    },
                    {
                        property: 'subsidiary',
                        label: 'Sucursal',
                        sortable: false
                    },
                    {
                        property: 'zone',
                        label: 'Ubicación',
                        sortable: false
                    },
                    {
                        property: 'delete',
                        label: 'Acciones'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.name = '<a href="/services/details/' + item.details + '/'+ item.business_unit_id + ' ">' + item.name + '</a>';
                        //item.detail = '<a href="/services/details/' + item.detail + '"><i class="icon-eye-open"></i></a>';
                        item.delete =
                            '<a href="/services/update/' + item.edit + '/' + item.business_unit_id + '" class="update_service" data-toggle="ajaxModal"><i class="icon-edit text-warning"></i></a>'
                                +
                                '<label>|</label>'
                                +
                            '<a href="/services/remove/' + item.delete + '/' + item.business_unit_id  + '"><i class="icon-remove text-danger"></i></a>';
                    });
                }
            })
        });
    });
}

function companiesDatagrid() {
    // fuelux subsidiaries datagrid
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {

            var url = '/companies/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.companies;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                switch (options.filter.value) {
                                    case 'lt5m':
                                        if (item.population < 5000000) return true;
                                        break;
                                    case 'gte5m':
                                        if (item.population >= 5000000) return true;
                                        break;
                                    default:
                                        return true;
                                        break;
                                }
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar las compañias!')
                    });
            }, self._delay);
        }
    };

    $('#myComGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'address',
                        label: 'Direccion',
                        sortable: false
                    },
                    {
                        property: 'rfc',
                        label: 'RFC',
                        sortable: true
                    },
                    /*
                     {
                     property: 'active',
                     label: '¿Activa?',
                     sortable: true
                     },
                     */
                    {
                        property: 'c_det',
                        label: 'Detalles',
                        sortable: false
                    },
                    {
                        property: 'c_up',
                        label: 'Editar',
                        sortable: false
                    },
                    {
                        property: 'c_del',
                        label: 'Eliminar'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.c_det = '<a href="/companies/' + item.c_det + '/details/"><i class="icon-eye-open"></i></a>';
                        item.c_up = '<a href="/companies/' + item.c_up + '/edit/"><i class="icon-edit-sign"></i></a>';
                        item.c_del = '<a href="/companies/' + item.c_del + '/remove/"><i class="icon-remove-sign"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';
                    });
                }
            })
        });
    });
}

/*
* Tabla de indicadores/atributos
* */
function attributesDatagrid() {
    // fuelux subsidiaries datagrid
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/indicators/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.attributes;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        // FILTERING == FILTRADO DEL CONTENIDO
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                switch (options.filter.value) {
                                    case 'lt5m':
                                        if (item.population < 5000000) return true;
                                        break;
                                    case 'gte5m':
                                        if (item.population >= 5000000) return true;
                                        break;
                                    default:
                                        return true;
                                        break;
                                }
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar los atributos!')
                    });
            }, self._delay);
        }
    };

    $('#myAttributesGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'questions',
                        label: 'Preguntas Asociadas',
                        sortable: false
                    },
                    {
                        property: 'attribute_id',
                        label: 'Acciones',
                        sortable: false
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.name = '<a href="/indicators/details/' + item.attribute_id + ' ">' + item.name + '</a>';
                        item.attribute_id =
                            '<a class="update-attribute" href="/indicators/update/' + item.attribute_id + '"><i class="icon-edit text-warning"></i></a>'
                                +
                                '<label>|</label>'
                                +
                            '<a class="delete-attribute" href="/indicators/remove/' + item.attribute_id + '"><i class="icon-remove text-danger"></i></a>';
                    });
                }
            })
        });
    });
}


/* 373 x 210 div momentos
* Tabla de encuestas
*
function surveysDatagrid() {
    // fuelux subsidiaries datagrid
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/surveys/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.surveys;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                switch (options.filter.value) {
                                    case 'lt5m':
                                        if (item.population < 5000000) return true;
                                        break;
                                    case 'gte5m':
                                        if (item.population >= 5000000) return true;
                                        break;
                                    default:
                                        return true;
                                        break;
                                }
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar las encuestas!')
                    });
            }, self._delay);
        }
    };

    $('#mySurveysGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'x property',
                        label: 'X columna',
                        sortable: false
                    },
                    {
                        property: 'questions',
                        label: 'Preguntas Asociadas',
                        sortable: false
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {

                    });
                }
            })
        });
    });
}


//funcion para agregar una unidad de servicio
$('#addBusinessUnit').click(function () {

    $('.modal-body').load('/render/62805', function (result) {
        $('#myModal').modal({show: true});
    });


});*/


function zonesDatagrid() {
    // fuelux subsidiaries datagrid
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };


    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {

            var url = '/zones/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.zones;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }
                        /*
                        $(".dropdown-menu.mainM li a").click(function () {
                            var selText = $(this).text();
                            switch (selText) {
                                case 'Sucursal':
                                    $('#second-filter').children().remove();
                                    for (i = 0; i < sucursales.length; i++) {
                                        $('#second-filter').append("<li data-value='" + sucursales[i] + "' data-selected='true'><a href='#'>" + sucursales[i] + "</a></li>")
                                    }
                                    break;
                                case 'Zona':
                                    $('#second-filter').children().remove();
                                    for (i = 0; i < zonas.length; i++) {
                                        $('#second-filter').append("<li data-value='" + zonas[i] + "' data-selected='true'><a href='#'>" + zonas[i] + "</a></li>")
                                    }
                                    break;
                            }

                        });

                        // FILTERING
                        if (options.filter) {
                            data = _.filter(data, function (item) {
                                for (i = 0; i < sucursales.length; i++) {
                                    switch (options.filter.value){
                                        case sucursales[i]:
                                            if (item.subsidiary == sucursales[i]) return true;
                                            break;
                                    }
                                }
                                for (i = 0; i < zonas.length; i++) {
                                    switch (options.filter.value){
                                        case zonas[i]:
                                            if (item.zone == zonas[i]) return true;
                                            break;
                                    }
                                }

                                switch (options.filter.value) {

                                    case 'Sucursal':
                                        if (item.subsidiary == 'Sucursal 1') return true;
                                        break;
                                    case 'Zona':
                                        if (item.subsidiary == 'Subsidiaria 2') return true;
                                        break;
                                    default:
                                        return true;
                                        break;
                                }
                            });
                        }
                        */

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar las zonas!')
                    });
            }, self._delay);
        }
    };

    $('#myZonesGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                // Column definitions for Datagrid
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'someAttr',
                        label: 'someAttr',
                        sortable: false
                    },
                    {
                        property: 'zone_id',
                        label: 'Opciones',
                        sortable: false
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        var subid = item.subsidiary_id;
                        item.name = '<a href="/zones/' + item.zone_id + '">' + item.name + '</a>';
                        item.zone_id =
                            '<a href="/zones/'+ item.zone_id + '/edit/" class="update_zone" data-toggle="ajaxModal"><i class="icon-edit"></i></a>'
                                +
                                '<label>|</label>'
                                +
                            '<a href="/zones/'+ item.zone_id + '/remove/" class="remove_zone" data-toggle="ajaxModal"><i class="icon-remove"></i></a>';
                    });

                    $.each(items, function (index, item) {

                        if (zonas.length == 0) {
                            var zona = item.zone;
                            zonas.push(zona);
                        }
                        var coincidencias = 0

                        for (var i = 0; i < zonas.length; i++) {
                            if (zonas[i] == item.zone) {
                                coincidencias++;
                            }
                        }

                        if (coincidencias == 0) {
                            var zona = item.zone;
                            zonas.push(zona)
                        }

                    });

                }

            })
        });
    });
}


function userListDatagrid() {
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/user_list/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.users;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar los usuarios, intente mas tarde!')
                    });
            }, self._delay);
        }
    };

    $('#myULGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                columns: [
                    {
                        property: 'name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'surname',
                        label: 'Apellido',
                        sortable: false
                    },
                    {
                        property: 'email',
                        label: 'Email',
                        sortable: false
                    },
                    {
                        property: 'role',
                        label: 'Rol',
                        sortable: false
                    },
                    {
                        property: 'actions',
                        label: 'Acciones'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.name = '<a href="#">' + item.name + '</a>';
                        item.actions = '<a href="/user/edit/'+ item.actions +'" class="edit-user" data-toggle="ajaxModal"><i class="icon-edit"></i></a>' +
                            '<a href="/user/delete/'+ item.actions +'"  class="remove-user"><i class="icon-remove"></i></a>';
                    });
                }
            })
        });
    });
}


function clientListDatagrid() {
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/clients/json'
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.clients;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar los clientes, intente mas tarde!')
                    });
            }, self._delay);
        }
    };

    $('#myCGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                columns: [
                    {
                        property: 'first_name',
                        label: 'Nombre',
                        sortable: true
                    },
                    {
                        property: 'last_name',
                        label: 'Apellido',
                        sortable: false
                    },
                    {
                        property: 'email',
                        label: 'Email',
                        sortable: false
                    },
                    {
                        property: 'company',
                        label: 'Compañia',
                        sortable: false
                    },
                    {
                        property: 'state',
                        label: 'Estado',
                        sortable: false
                    },
                    {
                        property: 'city',
                        label: 'Ciudad',
                        sortable: false
                    },
                    {
                        property: 'rating',
                        label: 'Rating',
                        sortable: false
                    },
                    {
                        property: 'actions',
                        label: 'Acciones'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {

                        var stars = '';

                        if (item.rating == null){
                            for (var j = 1; j <= 5; j++){
                                stars += '<i class="icon-star-empty" id="star' + j + '">';
                            }
                        } else {
                            for (var i = 1; i <= 5; i++){
                                if (i <= item.rating){
                                    stars += '<i class="icon-star" id="star' + i + '">';
                                } else {
                                    stars += '<i class="icon-star-empty" id="star' + i + '">';
                                }
                            }
                        }

                        item.first_name = '<a href="/clients/details/'+ item.actions +'">' + item.first_name + '</a>';
                        item.rating = '<input type="hidden" value="'+ item.rating +'">' + stars;
                        item.actions = '<a href="/clients/edit/'+ item.actions +'" class="edit-client" data-toggle="ajaxModal"><i class="icon-edit"></i></a>' +
                            '<a href="/clients/remove/'+ item.actions +'"  class="remove-client"><i class="icon-remove"></i></a>';
                    });
                }
            })
        });
    });
}

function clientActivityDatagrid(client) {
    var DataGridDataSource = function (options) {
        this._formatter = options.formatter;
        this._columns = options.columns;
        this._delay = options.delay;
    };

    DataGridDataSource.prototype = {

        columns: function () {
            return this._columns;
        },

        data: function (options, callback) {
            var url = '/clients/activity/' + client
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.activity;
                        // SEARCHING
                        if (options.search) {
                            data = _.filter(data, function (item) {
                                var match = false;

                                _.each(item, function (prop) {
                                    if (_.isString(prop) || _.isFinite(prop)) {
                                        if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
                                    }
                                });

                                return match;
                            });
                        }

                        var count = data.length;

                        // SORTING
                        if (options.sortProperty) {
                            data = _.sortBy(data, options.sortProperty);
                            if (options.sortDirection === 'desc') data.reverse();
                        }

                        // PAGING
                        var startIndex = options.pageIndex * options.pageSize;
                        var endIndex = startIndex + options.pageSize;
                        var end = (endIndex > count) ? count : endIndex;
                        var pages = Math.ceil(count / options.pageSize);
                        var page = options.pageIndex + 1;
                        var start = startIndex + 1;

                        data = data.slice(startIndex, endIndex);

                        if (self._formatter) self._formatter(data);

                        callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });
                    }).fail(function (e) {
                        alert('¡No se pueden consultar la actividad del cliente, intente mas tarde!')
                    });
            }, self._delay);
        }
    };

    $('#myClientActivityGrid').each(function () {
        $(this).datagrid({
            dataSource: new DataGridDataSource({
                columns: [
                    {
                        property: 'date',
                        label: 'Fecha',
                        sortable: true
                    },
                    {
                        property: 'subsidiary',
                        label: 'Sucursal',
                        sortable: false
                    },
                    {
                        property: 'rating',
                        label: 'Rating',
                        sortable: false
                    },
                    {
                        property: 'status',
                        label: 'Status'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.status = '<a href="#">' + item.status + '</a>';
                        item.actions = '<a href="/clients/edit/'+ item.actions +'" class="edit-client" data-toggle="ajaxModal"><i class="icon-edit"></i></a>' +
                            '<a href="/clients/remove/'+ item.actions +'"  class="remove-client"><i class="icon-remove"></i></a>';
                    });
                }
            })
        });
    });
}