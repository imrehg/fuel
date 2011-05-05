/* Fuel price plotting */
var chart;
jQuery.noConflict();
jQuery(document).ready(function() {
    var options = {
	chart: {
	    renderTo: 'fueleconomy',
	    defaultSeriesType: 'scatter',
	    zoomType: 'xy'
	},
	title: {
	    text: 'Global petrol price vs. economy'
	},
	tooltip: {
	    formatter: function() {
		return '<b>'+this.point.name+'</b><br/>'+
		    'GDP: $'+Math.floor(Math.exp(this.x))+'<br/>'+
		    'Gasoline: ¢'+this.y;
	    }
	},
	xAxis: {
	    title: {
		text: 'GDP / capita ($)'
	    },
	    labels: {
		formatter: function() {
                return Math.floor(Math.exp(this.value));
		}
            }
	},
	yAxis: {
	    min : 0,
	    title: {
		text: 'Gasoline price / liter (¢)'
	    },
	},
	plotOptions: {
            scatter: {
		marker: {
		    radius: 5,
		    states: {
			hover: {
			    enabled: true,
			    lineColor: 'rgb(100,100,100)'
			}
		    }
		},
		states: {
		    hover: {
			marker: {
			    enabled: false
			}
		    }
		}
            }
	},
	symbols: [
	    'circle', 
	    'triangle', 
	],
	legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 30,
            floating: true,
            backgroundColor: '#FFFFFF',
            borderWidth: 1
	},
	series: []
        
    };

    var rankOptions = {
	chart: {
            renderTo: 'fuelrank',
            defaultSeriesType: 'column',
	    zoomType: 'xy'
	},
	title: {
            text: 'Gasoline price ranking'
	},
	tooltip: {
	    formatter: function() {

		return '<b>'+this.point.name+'</b><br/>'+
		    'Rank: '+this.x+'<br/>'+
		    'Gasoline: ¢'+this.y;
	    }
	},
	xAxis: {
	    min: 0,
	    max: 161,
            title: {
		text: 'Country rank in gasoline price'
            }
	},
	yAxis: {
            min: 0,
            title: {
		text: 'Gasoline price / liter (¢)'
            }
	},
	legend: {
            enabled: false
	},
	plotOptions: {
            column: {
		groupPadding: 0,
		pointPadding: 0,
		borderWidth: 0,
            }
	},
	series : []
    }
	
    jQuery.get('/static/fuel/data.csv', function(data) {
  	var lines = data.split('\n');
	// Fuel price vs. GDP plot
        var seriesout = { 
	    name: "Net oil exporter",
	    color: 'rgba(243, 83, 83, .7)',
	    data: []
	};
        var seriesin = { 
	    name: "Net oil importer",
	    color: 'rgba(109, 112, 241, .7)',
	    data: []
	};
        var ranks = {
	    data: []
	}
	jQuery.each(lines, function(lineNo, line) {
	    // Skip header and assemble data
	    if (lineNo > 0) {
 		var items = line.split(',');
		var gdp = parseFloat(items[2]);
		var oilout = parseFloat(items[4]);
		var oilin = parseFloat(items[5]);
		var price = parseFloat(items[6]);
		var rank = parseInt(items[7])
		
		if (price > 0 & gdp > 0) {
                    var point = { name: items[1], x: Math.log(gdp), y: price }
                    if (oilout > oilin) {
			seriesout.data.push(point);
                    } else {
			seriesin.data.push(point);
                    };
		}
		if (price > 0) {
                    if (oilout > oilin) {
			ranks.data.push( {name: items[1], x: rank, y: price, color: 'rgba(243, 83, 83, .7)'})
		    } else {
		    	ranks.data.push( {name: items[1], x: rank, y: price, color: 'rgba(109, 112, 241, .7)'})
		    }
		}
	    }
	});
        options.series.push(seriesin);
        options.series.push(seriesout);
        var chart = new Highcharts.Chart(options);

        rankOptions.series.push(ranks);
        var chart = new Highcharts.Chart(rankOptions);


    });
});
