/** 
 * Version 2.0
 * markitondemand / DataApis
 * https://github.com/markitondemand
 * Added some modifications like symbol lookup error checking, input symbols and ids.
 */
var Markit = {};

/**
 * Define the InteractiveChartApi.
 * First argument is symbol (string) for the quote. Examples: AAPL, MSFT, JNJ, GOOG.
 * Second argument is duration (int) for how many days of history to retrieve.
 */
Markit.InteractiveChartApi = function(symbol,duration,htmlID){
	this.symbol = symbol.toUpperCase();
	this.duration = duration;
    this.id = htmlID;
	this.PlotChart(symbol);
};

Markit.InteractiveChartApi.prototype.PlotChart = function(symbol){ 
	//handle the tickers in the user portfolio
	var trArray = $("#portfolioBody tr");
  	var portfolio = [];
  	//update portfolio global array symbols
 	 trArray.each( function (i,v){
  		var currTicker = v.title.toUpperCase();
		portfolio.push(currTicker);
	});
	portfolio.push(symbol);
	//remove duplicates
	var uniqueArray = portfolio.filter(function(elem, pos) {
		return portfolio.indexOf(elem) == pos;
	});
	
	//set up data
    var seriesOptions = [],
			yAxisOptions = [],
			seriesCounter = 0,
			colors = Highcharts.getOptions().colors;
   //Make JSON request for timeseries data
	$.each(uniqueArray, function(i, name) {
		var params = {
			parameters: JSON.stringify( Markit.InteractiveChartApi.prototype.getInputParams(name) )
		}
		console.log(params);
		$.ajax({
			data: params,
			url: "http://dev.markitondemand.com/Api/v2/InteractiveChart/jsonp",
			dataType: "jsonp",
			context: this,
			success: function(json){
				//Catch errors
				if (!json || json.Message){
					console.error("Error: ", json.Message);
					return;
				}
				seriesOptions[i] = {
					name: name,
					data: Markit.InteractiveChartApi.prototype._getOHLC(json),
					volume: Markit.InteractiveChartApi.prototype._getVolume(json)
				};
				
				// As we're loading the data asynchronously, we don't know what order it will arrive. So
				// we keep a counter and create the chart when all the data is loaded.
				seriesCounter++;
				if (seriesCounter == uniqueArray.length) {
					//createChart();
					Markit.InteractiveChartApi.prototype.render(json, seriesOptions, symbol);
				}
			},
			error: function(response,txtStatus){
				console.log(response,txtStatus)
			}
		});
	});
};

Markit.InteractiveChartApi.prototype.getInputParams = function(name){
    return {  
        Normalized: false,
        NumberOfDays: 7304,
        DataPeriod: "Day",
        Elements: [
            {
                Symbol: name || this.symbol,
                Type: "price",
                Params: ["ohlc"] //ohlc, c = close only
            },
            {
                Symbol: name || this.symbol,
                Type: "volume"
            }
        ]
        //,LabelPeriod: 'Week',
        //LabelInterval: 1
    }
};

Markit.InteractiveChartApi.prototype._fixDate = function(dateIn) {
    var dat = new Date(dateIn);
    return Date.UTC(dat.getFullYear(), dat.getMonth(), dat.getDate());
};

//returns the stock stock price data received from Markit api
Markit.InteractiveChartApi.prototype._getOHLC = function(json) {
    var dates = json.Dates || [];
    var elements = json.Elements || [];
    var chartSeries = [];

    if (elements[0]){

        for (var i = 0, datLen = dates.length; i < datLen; i++) {
            var dat = this._fixDate( dates[i] );
            var pointData = [
                dat,
                elements[0].DataSeries['open'].values[i],
                elements[0].DataSeries['high'].values[i],
                elements[0].DataSeries['low'].values[i],
                elements[0].DataSeries['close'].values[i]
            ];
            chartSeries.push( pointData );
        };
    }
    return chartSeries;
};

//returns the stock volume data received from Markit api
Markit.InteractiveChartApi.prototype._getVolume = function(json) {
    var dates = json.Dates || [];
    var elements = json.Elements || [];
    var chartSeries = [];

    if (elements[1]){

        for (var i = 0, datLen = dates.length; i < datLen; i++) {
            var dat = this._fixDate( dates[i] );
            var pointData = [
                dat,
                elements[1].DataSeries['volume'].values[i]
            ];
            chartSeries.push( pointData );
        };
    }
    return chartSeries;
};

//creates individual candlestick and area charts
Markit.InteractiveChartApi.prototype.render = function(data, seriesOptions, symbol) {
		//create comparative chart
		$("#stockTickerQueryGraph3").highcharts('StockChart', {
			chart: {
			},
			title: {
            	text: symbol + ' vs. Portfolio'
        	},
			rangeSelector: {
				selected: 4
			},
			yAxis: {
				labels: {
					formatter: function() {
						return (this.value > 0 ? '+' : '') + this.value + '%';
					}
				},
				plotLines: [{
					value: 0,
					width: 2,
					color: 'silver'
				}]
			},	    
			plotOptions: {
				series: {
					compare: 'percent'
				}
			},	    
			tooltip: {
				pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
				valueDecimals: 2
			},	    
			series: seriesOptions
		});
		
	//just in case of asyncronous ajax response
	var currIndex = 0;
	for(var i=0; i < seriesOptions.length; i++) {
		if (seriesOptions[i]['name'] == symbol) {
			currIndex = i;
		}
	}
	
    // set the allowed units for data grouping
    var groupingUnits = [[
        'week',                         // unit name
        [1]                             // allowed multiples
    ], [
        'month',
        [1, 2, 3, 4, 6]
    ]];

    // create candlestick chart
    $("#stockTickerQueryGraph1").highcharts('StockChart', {      
        rangeSelector: {
            selected: 1
            //enabled: false
        },

        title: {
            text: symbol + ' Historical Price'
        },

        yAxis: [{
            title: {
                text: 'OHLC'
            },
            height: 200,
            lineWidth: 2
        }, {
            title: {
                text: 'Volume'
            },
            top: 300,
            height: 100,
            offset: 0,
            lineWidth: 2
        }],
        
        series: [{
            type: 'candlestick',
            name: symbol,
            data: seriesOptions[currIndex]['data'],
            dataGrouping: {
                units: groupingUnits
            }
        }, {
            type: 'column',
            name: 'Volume',
            data: seriesOptions[currIndex]['volume'],
            yAxis: 1,
            dataGrouping: {
                units: groupingUnits
            }
        }],
        credits: {
            enabled:false
        }
    });
    
    //Create Area chart
     $("#stockTickerQueryGraph2").highcharts('StockChart', {  
        rangeSelector: {
            selected: 1
            //enabled: false
        },

        title: {
            text: symbol + ' Historical Price'
        },

        yAxis: [{
            title: {
                text: 'OHLC'
            },
            height: 200,
            lineWidth: 2
        }, {
            title: {
                text: 'Volume'
            },
            top: 300,
            height: 100,
            offset: 0,
            lineWidth: 2
        }],
        
        series: [{
            type: 'area',
            name: symbol,
            data: 	seriesOptions[currIndex]['data'],
            threshold : null,
            tooltip : {
            	valueDecimals : 2
			},
			fillColor : {
					linearGradient : {
						x1: 0, 
						y1: 0, 
						x2: 0, 
						y2: 1
					},
					stops : [[0, Highcharts.getOptions().colors[0]], [1, 'rgba(0,0,0,0)']]
			}
		}]
    });    
};