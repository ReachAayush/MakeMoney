/* ====== PORTFOLIO.JS ======

Frontend JavaScript Methods that deal with the Portfolio.html
page, which is the barebones for any Hustler (Hustle User).

- Rishabh Alaap Singh
- Torffick 'TK' Abdul
- Aayush Aggarwal

*/

/* ------------------------- HEADERS --------------------------- */

/* -- GLOBAL VARS -- 
 * all external dependencies in terms of IDs, headers, etc. 
 */

/* -- Graph -- */
var STOCK_GRAPH_USR_INPUT = "#stockTickerQueryGraphInput";
var CANDLESTICK_GRAPH = "#stockTickerQueryGraph1";
var CANDLESTICK_GRAPH_BTN = "#stockTickerQueryGraphInput1";
var AREA_GRAPH = "#stockTickerQueryGraph2";
var AREA_GRAPH_BTN = "#stockTickerQueryGraphInput2";

var GRAPH_LOADING = "#graph-loading";

/* -- Portfolio -- */
var PORTFOLIO = "#portfolioBody";
var PORTFOLIO_ROWS = PORTFOLIO + " tr";
var PORTFOLIO_ROW_HDR = "portfolio-row";
var PORTFOLIO_VALUE = "#portfolioValue";

/* -- Marketplace -- */
var MARKETPLACE = "#marketplaceBody";
var MARKETPLACE_USR_INPUT = "#stockTickerQuery";
var MARKETPLACE_NEXT_IDX = 0;
var MARKETPLACE_ROW_ID = "marketplace-row"

var CASH_ON_HAND = "#cashOnHand";

/* -- BACKEND URLs -- */
var BUY_STOCK = "buy"
var SELL_STOCK = "sell"

/* -- GLOBAL FUNCTIONS -- */

/* returns true if "Enter" key was pressed */
var ENTER_PRESSED = function(e) {return e.keyCode == 13};

/* ------------------------------------------------------------- */

/* --------- GRAPHING METHODS ----------- */

/* Writes "Loading" near the graph when the graph is loading */
function graphLoading(b) {

  console.log("woo ", b);

  if (b === true) {
    $(GRAPH_LOADING).html("Loading...");
  } else {
    $(GRAPH_LOADING).html("");
  }
}

/* Draws the stock history graph for a given user input. */
function drawStockHistGraph(tckr) {
  //show/hide diff chart divs
  $(CANDLESTICK_GRAPH).show();
  $(AREA_GRAPH).hide();
  $(CANDLESTICK_GRAPH_BTN).focus();
  
  //call interactive chart api. 7304 represents 20years of stock data in days.
  new Markit.InteractiveChartApi(tckr,7304,"stockTickerQueryGraph");
}

/* --------- PORTFOLIO METHODS ----------- */

/* Refresh Method is called to update the entire potfolio object, 
 * including - 
 * i. Current Price of Stock, Value and Net Payoff for each Buy Instance
 * ii. Current Portfolio value and cash on hand
 */
 function refresh() {
  console.log("refresh!!");
  trArray = $(PORTFOLIO_ROWS);
  trArray.each( function (i,v){
  	var currTicker = v.title.toUpperCase();
    // get the current price using the API
	new Markit.QuoteService(currTicker, function(data) {
		//Catch errors
		if (!data || data.Message){
			console.error("Error: ", data.Message);
			alert("Unfortunately, we can't process your request at this time. \
          Please try again later.");
			return;
		}
	
		//Quote data is jsonResult. Key: Name, Symbol, LastPrice,
		//Change, ChangePercent, Timestamp, MSDate, MarketCap, Volume,
		//ChangeYTD, ChangePercentYTD, High, Low, Open
        var bid = parseInt(data.LastPrice); //keeping ints for consistency

        // Update this bid value into the table
        var currentBid = $("#" + PORTFOLIO_ROW_HDR + i + "-currentBid");
        currentBid.html(bid);

        // Update value and net payoff accordingly
        updatePortfolioVal(i);

        // updates the portfolio value
        updatePortfolioNetWorth();
    });
  });
}

/* buy - Major function that implements purchase of stock into
 *  user's virtual portfolio 
 */
function buy(rowID) {
  var row = $("#" + rowID);
  var elts = row.find('td');

  // Create JSONObject of keys required for backend.
  var backendObj = {};

  // map backendObj to it's correct formatting
  $.each(elts, function(i,obj) {
    if (obj.title == "quant") {
     backendObj[obj.title] = $($(obj).children()[0]).val();
   } else {
    backendObj[obj.title] = obj.textContent;
  }
  });

  // send this JSON object to the backend for db mgmt
  $.ajax({
    url: BUY_STOCK,

    data:backendObj, 

    success: function(data) {
      // add to portfolio
      var b = $(PORTFOLIO);
      var portSize = $(PORTFOLIO_ROWS).size();
      
      var port_row_id_hdr = PORTFOLIO_ROW_HDR + portSize;

      var row = $("<tr title=" + backendObj["ticker"] + " id='" + 
        port_row_id_hdr + "'></tr>");
      
      //Create Objects
      var tckr = $("<td class='text-center'>" + backendObj['ticker'] + "</td>");
      var name = $("<td class='text-center'>" + backendObj['name'] + "</td>");
      var date = $("<td class='text-center'>" +
       data['date'] + "</td>"); // Date of Purchase

      var boughtAt = $("<td class='text-center' id='" + 
       port_row_id_hdr + "-boughtAt'>" + backendObj['ask'] + "</td>");

      var quant = $("<td class='text-center' id='" + 
        port_row_id_hdr + "-quantity'>" + backendObj['quant'] + "</td>");

      var currBid = $("<td class='text-center' id='" + 
        port_row_id_hdr + "-currentBid'>" +
         backendObj['ask'] + "</td>"); // current Price

      var valPerStock = $("<td class='text-center' id='" + 
        port_row_id_hdr + "-value'>0</td>");

      var netPayoff = $("<td class='text-center' id='" + 
        port_row_id_hdr + "-netPayoff'>0</td>");
      
      //button
      var sellBtn = $("<td class='text-center'><button class='btn btn-default' \
        onclick=\"sell(" + portSize + ")\">Sell</button></td>");

      //append
      row.append(tckr);
      row.append(name);
      row.append(date);
      row.append(boughtAt);
      row.append(quant);
      row.append(currBid);
      row.append(valPerStock);
      row.append(netPayoff);
      row.append(sellBtn);

      b.append(row);

      // update the cash on hand for this user
      $(CASH_ON_HAND).text("$" + data['cashOnHand']);

      refresh();
    },

    error: function(data) {
      console.log("--- ERR LOG (trying to access backend) ---");
      console.log(e);
      alert("Unfortunately, we can't process your request at this time. \
        Please try again later.");
    }
  });
}

// Sell Implementation
function sell(idx) {

  var portfolio_row_id_hdr = "#" + PORTFOLIO_ROW_HDR

  var soldAt = $(portfolio_row_id_hdr + idx + "-currentBid").html();
  var quant = $(portfolio_row_id_hdr + idx + "-quantity").html();
  var cashOnHand = $(CASH_ON_HAND).html()

  var backendObj = {}
  backendObj['index'] = idx;
  backendObj['soldAt'] = soldAt;


  //send the index of the row selected to the backend for removal
  $.ajax({
    url: SELL_STOCK,
    data:backendObj,
    success: function(data) {
      // update cashOnHand
      $(CASH_ON_HAND).text("$" + data['cashOnHand']);

      // remove that row from the table
      // TODO maybe we could add like a fade out?

      $("#" + PORTFOLIO_ROW_HDR + idx).remove();

      // update all rows in the table
      reorderPortfolioRows();      
    },

    error: function(data) {
      alert("Something went wrong while implementing your sell. \
        Please call a technician.");
      console.log("--- ERR LOG (trying to complete backend AJAX call \
        to save sell in db) ---");
      console.log(e);
    }
  });
}

/* Updates the value, and net Payoff of the given index */
function updatePortfolioVal(idx){
  var portfolio_row_id_hdr = "#" + PORTFOLIO_ROW_HDR

  var boughtAt = $(portfolio_row_id_hdr + idx + "-boughtAt");
  var curr = $(portfolio_row_id_hdr + idx + "-currentBid");
  var quant = $(portfolio_row_id_hdr + idx + "-quantity");

  var value = Math.round(curr.html() - boughtAt.html());
  var netPayoff = value * quant.html();

  $(portfolio_row_id_hdr + idx + "-value").html(value);
  $(portfolio_row_id_hdr + idx + "-netPayoff").html(netPayoff);
}

/* Reorders ID values of the porfolio table for all current objects
 * when called.
 */
function reorderPortfolioRows(){
  var rows = $(PORTFOLIO_ROWS);

  $.each(rows, function(i, row) {

    var new_row_id = PORTFOLIO_ROW_HDR + i;

    // Change the row ID
    $(row).attr("id", new_row_id);

    // Change the ID for all their children
    var children = $(row).children();

    $(children[3]).attr("id", new_row_id + "-boughtAt");
    $(children[4]).attr("id", new_row_id + "-quantity");
    $(children[5]).attr("id", new_row_id + "-currentBid");
    $(children[6]).attr("id", new_row_id + "-value");
    $(children[7]).attr("id", new_row_id + "-netPayoff");

    var sellbtn = $(children[8]).children()[0];
    console.log("btn = ", sellbtn);
    $(sellbtn).attr("onclick", "sell('" + i + "')");
  });
}

/* Looks into the portfolio table and returns the sum of 
 * all the current bid price * quant
 */
function updatePortfolioNetWorth() {
  var rows = $(PORTFOLIO_ROWS);
  var portNetWorth = 0;

  portfolio_row_id_hdr = "#" + PORTFOLIO_ROW_HDR;

  $.each(rows, function (i, row) {

    var id_quant = portfolio_row_id_hdr + i + "-quantity";
    var id_cBid = portfolio_row_id_hdr + i + "-currentBid";

    var quant = $(id_quant).html();
    var cBid = $(id_cBid).html();

    portNetWorth += (parseInt(quant) * parseInt(cBid));
  });

  var portNetWorthText = "$" + portNetWorth;

  $(PORTFOLIO_VALUE).html(portNetWorthText);
}


/* --------- MARKETPLACE METHODS ----------- */

/* AJAX success method - 
 * Given a search result in Data making an API call, 
 * adds it to the marketplace table.
 */
function addSearchResultToMarketplaceTable(data) {
    var i = MARKETPLACE_NEXT_IDX;
    var exchange;
    new Markit.LookUpService(data.Symbol, function(lookupData) {
    	exchange = lookupData[0].Exchange;
    	console.log(exchange);
    });
    //Create our own bid/ask spread of 
    var dataBid = parseInt(data.LastPrice) - 0.50;
    var dataAsk = parseInt(data.LastPrice);

    var id = MARKETPLACE_ROW_ID + i

    var row = $("<tr class='text-center' id='" + id + "'></tr>");
    var name = $("<td title='ticker'>" + data.Symbol + "</td>");
    var company = $("<td title='name'>" + data.Name + "</td>")
    var stockExchange = $("<td title='exchange'>" + exchange + "</td>");
    var bid = $("<td title='bid'>" + dataBid + "</td>");
    var ask = $("<td title='ask'>" + dataAsk + "</td>");
    var shares = $("<td title='quant'><input type='text' name='quant', value='10'></td>");
    var buttons = $("<td class='text-center'><button class='btn btn-success' \
      onclick='buy(\"" + id + "\")'>Buy</button></td>");

    row.append(name);
    row.append(company);
    row.append(stockExchange);
    row.append(bid);
    row.append(ask);
    row.append(shares);
    row.append(buttons);

    $(MARKETPLACE).append(row);   

    //increment global next_idx value
    MARKETPLACE_NEXT_IDX++;
} 

/* AJAX Err Method Call - 
 * Run this method if performing the API Call resulted in an error.
 */
function addSearchInstanceToMarketplaceErrHandler(e) {
  console.log("--- ERR LOG (trying to access YAHOO API) ---");
  console.log(e);
  alert("Unfortunately, we can't process your request at this time. Please try again later.");
}

/* API CALL - 
 * Performs a Markit Lookup Query to receive stock data
 */
function makeStockQuoteCall(tckr, ajax_success, ajax_err) {

	new Markit.QuoteService(tckr, function(data) {
		//Catch errors
		if (!data || data.Message){
			console.error("Error: ", data.Message);
			alert("No such ticker symbol.");
			alert(ajax_err);
			return;
		}
	
		//Quote data is jsonResult. Key: Name, Symbol, LastPrice,
		//Change, ChangePercent, Timestamp, MSDate, MarketCap, Volume,
		//ChangeYTD, ChangePercentYTD, High, Low, Open
		ajax_success(data);
  });
}




/* ------------ TOP-LEVEL METHODS --------------- */

/* ------ CLICK HANDLERS ------ */

/* --- GRAPH --- */
$(STOCK_GRAPH_USR_INPUT).keyup(function(e){
  if(ENTER_PRESSED(e)) {  
    // Get the user input
    var tckr = $(STOCK_GRAPH_USR_INPUT).val().toUpperCase();
    graphLoading(true);
    drawStockHistGraph(tckr); 
    graphLoading(false);
  }
});

$(STOCK_GRAPH_USR_INPUT).blur(function() {
  //delete text input when user clicks out
  $(this).val('');
});

//handle button toggles for charts
$(CANDLESTICK_GRAPH_BTN).on("click", function() {
  $(AREA_GRAPH).hide();
  $(CANDLESTICK_GRAPH).show();
  $(CANDLESTICK_GRAPH_BTN).focus();
});

$(AREA_GRAPH_BTN).on("click", function() {
  $(CANDLESTICK_GRAPH).hide();
  $(AREA_GRAPH).show();
  $(AREA_GRAPH_BTN).focus();
});

/* --- MARKETPLACE --- */
$(MARKETPLACE_USR_INPUT).keyup(function(e){
  if (ENTER_PRESSED(e)) {
    var tckr = $(MARKETPLACE_USR_INPUT).val().toUpperCase();
    makeStockQuoteCall(tckr, addSearchResultToMarketplaceTable,
      addSearchInstanceToMarketplaceErrHandler);
  }
});

$(MARKETPLACE_USR_INPUT).blur(function() { $(this).val(''); });

/* ------ DOCUMENT.READY ------ */
$(document).ready(function(){

    // Calls refresh method on page load and every 5 seconds.
    refresh();
    setInterval(refresh, 5000);  
});

















