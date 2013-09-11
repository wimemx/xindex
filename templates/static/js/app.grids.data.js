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
                        property: 'bu_det',
                        label: 'Detalles',
                        sortable: false
                    },
                    {
                        property: 'bu_up',
                        label: 'Editar',
                        sortable: false
                    },
                    {
                        property: 'bu_del',
                        label: 'Eliminar'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.bu_det = '<a href="/business_units/details/' + item.bu_det + '"><i class="icon-eye-open"></i></a>';
                        item.bu_up = '<a href="/business_units/update/' + item.bu_up + '"><i class="icon-edit-sign"></i></a>';
                        item.bu_del = '<a href="/business_units/remove/' + item.bu_del + '"><i class="icon-remove-sign"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';
                    });
                }
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
                        property: 's_det',
                        label: 'Detalles',
                        sortable: false
                    },
                    {
                        property: 's_up',
                        label: 'Editar',
                        sortable: false
                    },
                    {
                        property: 's_del',
                        label: 'Eliminar'
                    }
                ],

                // Create IMG tag for each returned image
                formatter: function (items) {
                    $.each(items, function (index, item) {
                        item.s_det = '<a href="/services/details/' + item.s_det + '"><i class="icon-eye-open"></i></a>';
                        item.s_up = '<a href="/services/update/' + item.s_up + '"><i class="icon-edit-sign"></i></a>';
                        item.s_del = '<a href="/services/remove/' + item.s_del + '"><i class="icon-remove-sign"></i></a>';
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
                        item.c_det = '<a href="/companies/'+ item.c_det +'/details/"><i class="icon-eye-open"></i></a>';
                        item.c_up = '<a href="/companies/'+ item.c_up +'/edit/"><i class="icon-edit-sign"></i></a>';
                        item.c_del = '<a href="/companies/'+ item.c_del +'/remove/"><i class="icon-remove-sign"></i></a>';
                        //c = (item.active == true) ? "checked" : ""
                        //item.active = '<input type="checkbox" disabled="disabled" '+ c + '>';
                    });
                }
            })
        });
    });
}