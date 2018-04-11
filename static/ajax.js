var timeoutID;
var timeout = 1000;
var currentMsgs = 0;
var newMsgs = 0;
var button;
var textarea;
var select;

document.addEventListener("DOMContentLoaded", function() {
	var buttons = document.getElementsByTagName("button");
	
	switch(buttons.length) { 
	    case 1:
	    	buttons[0].addEventListener("click", sendCat, true);
	        break;
	    case 2:
	    	buttons[0].addEventListener("click", sendCat, true);
	    	buttons[1].addEventListener("click", rmCat, true);
	        break;
	    default:
	    	alert("What did you do");
	}

	textarea = document.getElementsByTagName("input")[0];
	select = document.getElementsByTagName("select")[0];

});

function sendCat() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	var cat = textarea.value;

	httpRequest.onreadystatechange = function() { handleSendCat(httpRequest, cat) };

	httpRequest.open("PUT", "/c");
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	var data = new Object();
	data.category = cat;
	data = JSON.stringify(data);

	httpRequest.send(data);
}

function handleSendCat(httpRequest, cat) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 204) {
			textarea.value = "";
			location.reload();
		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function rmCat() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	var cat = select.value;

	httpRequest.onreadystatechange = function() { handleRmCat(httpRequest, cat) };

	httpRequest.open("DELETE", "/c");
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	var data = new Object();
	data.category = cat;
	data = JSON.stringify(data);

	httpRequest.send(data);
}

function handleRmCat(httpRequest, cat) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 204) {
			location.reload();
		} else {
			alert("There was a problem with the delete request.");
		}
	}
}


