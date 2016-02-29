console.log("in background javascript");

chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    console.log(tabs[0].url);
});

chrome.tabs.getCurrent(function (tab) {
  //Your code below...
  //var tabUrl = encodeURIComponent(tab.url);
  //var tabTitle = encodeURIComponent(tab.title);

  /*
  var theurl = "http://www.newegg.com/Product/Product.aspx?Item=N82E16820233173";
  chrome.tabs.update(
    tab.id, {
      url: theurl});
  */
  console.log("get current tab");
  console.log(tab);
});

chrome.browserAction.onClicked.addListener(function(tab) {
  console.log("browserAction"); 
  /*
  chrome.tabs.executeScript({
    code: 'document.body.style.backgroundColor="red"'
  });*/
  chrome.tabs.executeScript({
    //code: 'Biz.Product.Product2010.gotoFeedBack();'
  });

});


chrome.browserAction.onClicked.addListener(function(tab) {
  // No tabs or host permissions needed!
  console.log('Turning ' + tab.url + ' red!');
  chrome.tabs.executeScript({
      code: 'document.body.style.backgroundColor="red"'
    });

});


//

// When the browser-action button is clicked...
chrome.browserAction.onClicked.addListener(function (tab) {
  // A function to use as callback

  //////// communicate with content
  // with in this scope to be able to get the tab.id
  function doStuffWithDom(domContent) {
      console.log('I received the following DOM content:\n' + domContent);
      // TODO, use an ajax to send back the crawled content. 

      // current test page
      //http://www.newegg.com/Product/Product.aspx?Item=N82E16820231018
      $.post(
        "http://rtds9.cse.tamu.edu:8080/receivedoc", 
        {
          "url":tab.url,
          "data":domContent
      });

      $.get("http://rtds9.cse.tamu.edu:8080/getnextid", function(data){
        // TODO, get one from the server that is not cralwed
        var theurl = "http://www.newegg.com/Product/Product.aspx?Item="+data.newegg_id; 
        chrome.tabs.update(tab.id, {url: theurl});
      });
      
  }


  // TODO, automatch the url and trigger the event

  // ...check the URL of the active tab against our pattern and...
  //if (urlRegex.test(tab.url)) {
        // ...if it matches, send a message specifying a callback too
  chrome.tabs.sendMessage(tab.id, {text: 'report_back'}, doStuffWithDom);
    //}
});


chrome.webNavigation["onCompleted"].addListener(function(data){
  var e = "onCompleted";
  if (typeof data)
        console.log(chrome.i18n.getMessage('inHandler'), e, data);
      else
        console.error(chrome.i18n.getMessage('inHandlerError'), e);



//*
  //if(data.url.startsWith("http://www.newegg.com/Product/Product.aspx?Item=")){}    
  //chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    //var tab_url = tabs[0].url;
  var prefix = "http://www.newegg.com/Product/Product.aspx?Item=";
  if( data.url.startsWith(prefix)){
    // TODO
    function newdoStuffWithDom(domContent) {
      // set timeout 2 second 
        setTimeout(function(){ 
            //console.log('I received the following DOM content:\n' + domContent);
            // TODO, use an ajax to send back the crawled content. 

            // current test page
            //http://www.newegg.com/Product/Product.aspx?Item=N82E16820231018
            $.post(
              "http://rtds9.cse.tamu.edu:8080/receivedoc", 
              {
                "url":data.url,
                "data":domContent
            });

            setTimeout(function(){ 

              $.get("http://rtds9.cse.tamu.edu:8080/getnextid", function(nextdata){
                // TODO, get one from the server that is not cralwed
                console.log("next to retrieval nextdata");
                console.log(nextdata);

                var theurl = "http://www.newegg.com/Product/Product.aspx?Item="+nextdata.newegg_id; 
                console.log(theurl);

                chrome.tabs.update(data.tabId, {url: theurl});
              }, "json");   
            },4000);

          }, 2000);        
    }

    console.log("trigger get content");
    chrome.tabs.sendMessage(data.tabId, {text: 'report_back'}, newdoStuffWithDom);
  }
  //});
  //*/

  /*

  chrome.tabs.getCurrent(function (tab) {
    if( data.url == tab.url){
      console.log("trigger get content");
      chrome.tabs.sendMessage(tab.id, {text: 'report_back'}, doStuffWithDom);
    }
  });
  //*/

});