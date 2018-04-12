//erl67
var timeoutID;
var timeout = 1000;
var currentMsgs = 0;
var newMsgs = 0;
var button;
var textarea;
var select;
var categories;

document.addEventListener("DOMContentLoaded", function() {
	var buttons = document.getElementsByTagName("button");
	
	switch(buttons.length) { //just use ID jfc
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
	
	getCats();
	
});

function getCats() {
	var httpRequest = new XMLHttpRequest();

	httpRequest.onreadystatechange = function() { handleGetCats(httpRequest) };

	httpRequest.open("GET", "/c", true);
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	httpRequest.send();
}

function handleGetCats(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
	        categories = httpRequest.responseText;
		} else {
			alert("There was a problem with the get request.");
		}
		console.log(httpRequest.status + httpRequest.responseText);
	}
}

function sendCat() {
	var httpRequest = new XMLHttpRequest();

	var cat = textarea.value;

	httpRequest.onreadystatechange = function() { handleSendCat(httpRequest, cat) };

	httpRequest.open("PUT", "/c", true);
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	var data = new Object();
	data.category = cat;
	data = JSON.stringify(data);

	httpRequest.send(data);
}

function handleSendCat(httpRequest, cat) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 201) {
			textarea.value = "";
			location.reload();
		} else {
			alert("There was a problem with the put request.");
		}
		console.log(httpRequest.status + httpRequest.responseText);
	}
}

function rmCat() {
	var httpRequest = new XMLHttpRequest();

	var cat = select.value;

	httpRequest.onreadystatechange = function() { handleRmCat(httpRequest, cat) };

	httpRequest.open("DELETE", "/c", true);
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
		console.log(httpRequest.status + httpRequest.responseText);
	}
}


