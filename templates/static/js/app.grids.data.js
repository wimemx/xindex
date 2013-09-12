/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 4/09/13
 * Time: 05:51 PM
 * To change this template use File | Settings | File Templates.
 */

function subsidiariesDatagrid() {
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
            //var url = '/static/js/data/datagrid.json';
            //Inician pruebas
            var url = '/subsidiaries/json'
            //terminan pruebas
            var self = this;


            setTimeout(function () {

                var data = $.extend(true, [], self._data);

                $.ajax(url, {
                    dataType: 'json',
                    async: false,
                    type: 'GET'
                }).done(function (response) {
                        data = response.subsidiarias;
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
                        alert('¡No se pueden consultar las sucursales, intente mas tarde!')
                    });
            }, self._delay);
        }
    };

    $('#MyStretchGrid').each(function () {
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
                        property: 'detalles',
                        label: 'Detalles',
                        sortable: false
                    },
                    /*
                     {
                     property: 'active',
                     label: '¿Activa?',
                     sortable: true
                     },
                     */
                    {
                        property: 'subsidiaryId',
                        label: 'Editar',
                        sortable: false
                    },
                    {
                        property: 'subsidiaryIds',
                        label: 'Eliminar',
                        sortable: false
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.subsidiaryId = '<a href="/subsidiaries/edit/' + item.subsidiaryId + '"><i class="icon-edit-sign"></i></a>';
                        item.subsidiaryIds = '<a href="/subsidiaries/remove/' + item.subsidiaryIds + '"><i class="icon-remove-sign"></i></a>';
                        item.detalles = '<a href="/subsidiaries/details/' + item.detalles + '"><i class="icon-eye-open"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';
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
                    /*
                     {
                     property: 'active',
                     label: '¿Activa?',
                     sortable: true
                     },
                     */
                    {
                        property: 'st_det',
                        label: 'Detalles',
                        sortable: false
                    },
                    {
                        property: 'st_up',
                        label: 'Editar',
                        sortable: false
                    },
                    {
                        property: 'st_del',
                        label: 'Eliminar'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.st_det = '<a href="/subsidiary_types/details/' + item.st_det + '"><i class="icon-eye-open"></i></a>';
                        item.st_up = '<a href="/subsidiary_types/update/' + item.st_up + '"><i class="icon-edit-sign"></i></a>';
                        item.st_del = '<a href="/subsidiary_types/remove/' + item.st_del + '"><i class="icon-remove-sign"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';
                    });
                }
            })
        });
    });
}

var sucursales = [], zonas = [];

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
                        label: 'Sucursal',
                        sortable: false
                    },
                    /*
                     {
                     property: 'active',
                     label: '¿Activa?',
                     sortable: true
                     },
                     */
                    {
                        property: 'zone',
                        label: 'Zona',
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
                        item.name = '<a href="/business_units/details/' + buid + '">' + item.name + '</a>';
                        item.business_unit_id = '<a href="/business_units/details/' + item.business_unit_id + '"><i class="icon-eye-open"></i></a>' + ' | ' +
                            '<a href="/business_units/update/' + item.business_unit_id + '"><i class="icon-edit-sign"></i></a>' + ' | ' +
                            '<a href="/business_units/remove/' + item.business_unit_id + '"><i class="icon-remove-sign"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
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
            var url = '/services/json'
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
                        item.name = '<a href="/services/details/' + item.details + ' ">' + item.name + '</a>';
                        //item.detail = '<a href="/services/details/' + item.detail + '"><i class="icon-eye-open"></i></a>';
                        item.delete =
                            '<a href="/services/update/' + item.edit + '"><i class="icon-edit text-warning"></i></a>'
                                +
                                '<label>|</label>'
                                +
                            '<a href="/services/remove/' + item.delete + '"><i class="icon-remove text-danger"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';
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


//funcion para agregar una unidad de servicio
$('#addBusinessUnit').click(function () {

    $('.modal-body').load('/render/62805', function (result) {
        $('#myModal').modal({show: true});
    });


});
