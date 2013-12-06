$(document).ready(function(){
    var i= 0; //use this to uniquely identify html id tags

     $("#searchTickerBtn").click(function(){
      var tckr = $("#searchTickerTxt").val();
      $.ajax({
      type: "GET",
      url: "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20%28%22" + tckr + "%22%29&env=store://datatables.org/alltableswithkeys&format=json",
      success:function(data){
        if (data.query.results.quote.ErrorIndicationreturnedforsymbolchangedinvalid) {
          alert("No such ticker symbol.");
        } else { 
          var result = data.query.results.quote;
          console.log(result);

          var row = $("<tr class='text-center' id='marketplace-table"+i+"'></tr>");
          var name = $("<td>" + result.symbol + "</td>");
          var company = $("<td>" + result.Name + "</td>")
          var stockExchange = $("<td>" + result.StockExchange + "</td>");
          var bid = $("<td>" + result.Bid + "</td>");
          var ask = $("<td>" + result.Ask + "</td>");
          var shares = $("<td><input id='shares' type='text' name='shares'></td>");
          var buttons = $("<td class='text-center'><div class='btn-group'><button class='longStockBtn btn btn-success'>Long</button><button class='shortStockBtn btn btn-danger'>Short</button></div></td>");
          var hidden = $("<input type='hidden' id='hidden' name='stockData' value='"+result.symbol+","+result.Name+","+result.StockExchange+","+result.Bid+","+result.Ask+"'>")

          row.append(name);
          row.append(company);
          row.append(stockExchange);
          row.append(bid);
          row.append(ask);
          row.append(shares);
          row.append(buttons);
          row.append(hidden);

          $("#marketplaceBody").append(row);
          i=i+1;
        }
        
      },
      error:function(e){
        console.log("GOT AN AJAX ERROR WHEN REFERENCING YAHOO API");
      },
      dataType: "json"
      });
    });
/*
    User presses enter key
    $("#searchTickerBtn").click(searchTicker());
    $("#searchTickerBtn").keyup(function(event) {
      if(event.keyCode == 13) {
        searchTicker();
      }
    });
*/

  //function to handle ajax request of orders
  function handleOrder(param, action) {
    var id = $(param).closest("tr").attr("id");
    //check if user input shares
    var shares = $("#"+id).find("#shares");
    if(shares.val() && shares.val() > 0) {
      console.log(id);
      var hidden = $("#"+id).find("#hidden");
      //add instruction to buy
      var dataArray = hidden.val().split(",");

      //submit ajax request
      $.post("/buy", 
            {'symbol':dataArray[0], 'name':dataArray[1], 'exchange':dataArray[2], 'bid':dataArray[3], 'ask':dataArray[4], 'shares':shares.val(), 'action':action, csrfmiddlewaretoken:'{{csrf_token}}'},
            function(data) { //alert("Data Loaded: " + data)
          });
    }
    else {
      console.log("no shares");
      return false;
    }
  }

  //handle long order
  $(document).on("click", ".buyStockBtn", function() {
    alert("long");
    handleOrder(this, 'long');
  });

  //handle shorting
  $(document).on("click", ".shortStockBtn", function() {
    alert("short");
    handleOrder(this, 'short');
  });

  function addMktTableElt(code){}
});