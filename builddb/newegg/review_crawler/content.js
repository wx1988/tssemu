// Listen for messages
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    // If the received message has the expected format...
    if (msg.text === 'report_back') {
        // Call the specified callback, passing
        // the web-page's DOM content as argument

		/*
		var script = document.createElement('script');
		script.textContent = "stopRefreshSite()";
		(document.head||document.documentElement).appendChild(script);
		*/

		var actualCode = '// Some code example \n' + 
                 'Biz.Product.Product2010.gotoFeedBack();'+
                 '$("TopPaginationForm").Pagesize.value=100;'+
                 'Biz.Product.ProductReview.submit("TopPaginationForm");';
        document.documentElement.setAttribute('onreset', actualCode);
		document.documentElement.dispatchEvent(new CustomEvent('reset'));
		document.documentElement.removeAttribute('onreset');

		console.log("Call send response after 2 second");
        sendResponse(document.all[0].outerHTML); 
        // set timeout 2 second 
        setTimeout(
        	function(){ 

        	}, 2000);        
		/*
        console.log("document");
        console.log(document);
        console.log("document.all");
        console.log(document.all[0]);
		*/        
    }
});