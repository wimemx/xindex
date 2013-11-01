/**
 * Created with PyCharm.
 * User: osvaldo
 * Date: 29/10/13
 * Time: 01:26 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){
	var buildMorris = function($re){
		if($re){
			$('.graph').html('');
		}
		var tax_data = [
	       {"period": "2011 Q3", "licensed": 3407, "sorned": 660},
	       {"period": "2011 Q2", "licensed": 3351, "sorned": 629},
	       {"period": "2011 Q1", "licensed": 3269, "sorned": 618},
	       {"period": "2005 Q4", "licensed": 3289, "sorned": null}
		];
        var report_data = [
            {"month": "Jul", "xindex": 4},
            {"month": "Agosto", "xindex": 5},
            {"month": "Septiembre", "xindex": 6},
            {"month": "Octubre", "xindex": 7}
        ];
		Morris.Line({
			element: 'hero-graph',
			data: report_data,
			xkey: 'month',
			ykeys: ['xindex'],
			labels: ['Valor']
		});
	}
    /*
    new Morris.Line({
        // ID of the element in which to draw the chart.
        element: 'historical-graph',
        // Chart data records -- each entry in this array corresponds to a point on
        // the chart.
        data: [
            { month: '2013-07', value: 4 },
            { month: '2013-08', value: 5 },
            { month: '2013-09', value: 4.5 },
            { month: '2013-10', value: 6 },
            { month: '2013-11', value: 8 }
        ],
        // The name of the data record attribute that contains x-values.
        xkey: 'month',
        // A list of names of data record attributes that contain y-values.
        ykeys: ['value'],
        // Labels for the ykeys -- will be displayed when you hover over the
        // chart.
        labels: ['Value'],
        xLabels: 'month'
    });
    */
    //buildMorris(true);

});
