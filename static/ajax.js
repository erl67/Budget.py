//erl67
var buttons, addBtn, delBtn, addXBtn, delXBtn;
var delCatDiv, addCat, selectCat;
var delXDiv, xSelectCat, xName, xDate, xTotal;
var categories, transactions;

document.addEventListener("DOMContentLoaded", function() {
	window.onload = prepare;
});

function prepare() {
	buttons = document.getElementsByTagName("button");
	
	delBtn = document.getElementById("delCatBtn");
	delBtn.addEventListener("click", rmCat, true);
	addBtn = document.getElementById("addCatBtn");
	addBtn.addEventListener("click", sendCat, true);
	
	addXBtn = document.getElementById("addXBtn");
	addXBtn.addEventListener("click", sendTransaction, true);

	addCat = document.getElementById("addCat");
	selectCat = document.getElementById("delCat");
	xSelectCat = document.getElementById("xSelectCat");
	
	delCatDiv = document.getElementById("delCatDiv");
	delXDiv = document.getElementById("delXDiv");
	
	xName = document.getElementById("xName");
	xDate = document.getElementById("xDate");
	xTotal = document.getElementById("xTotal");
	
	updatePage();
}

function getCats() {
	var httpRequest = new XMLHttpRequest();

	httpRequest.onreadystatechange = function() { handleGetCats(httpRequest) };

	httpRequest.open("GET", "/api/cats", true);
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	httpRequest.send();
}

function handleGetCats(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
	        categories = httpRequest.responseText;
	        if (categories.length > 5)
	        	delCatDiv.classList.remove("d-none");
	        else delCatDiv.classList.add("d-none");
		} else {
			alert("There was a problem with the get request.");
		}
		logStatus(httpRequest);
	}
}

function sendCat() {
	var httpRequest = new XMLHttpRequest();

	var cat = addCat.value;

	httpRequest.onreadystatechange = function() { handleSendCat(httpRequest, cat) };

	httpRequest.open("POST", "/api/cats", true);
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	var data = new Object();
	data.category = cat;
	data = JSON.stringify(data);

	httpRequest.send(data);
}

function handleSendCat(httpRequest, cat) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 201) {
			addCat.value = "";
			
			var option = document.createElement("option");
			var option2 = document.createElement("option");
			option.text = cat;
			option2.text = cat;
			option.value = selectCat.length;
			option2.value = xSelectCat.length;
			
			selectCat.add(option);
			xSelectCat.add(option2);
			updatePage();
		} else {
			alert("There was a problem with the post request.");
		}
		logStatus(httpRequest);
	}
}

function rmCat() {
	var httpRequest = new XMLHttpRequest();

	var cat = selectCat.value;
	
	if (cat) {
		httpRequest.onreadystatechange = function() { handleRmCat(httpRequest, cat) };
	
		httpRequest.open("DELETE", "/api/cats", true);
		httpRequest.setRequestHeader('Content-Type', 'application/json');
	
		var data = new Object();
		data.category = cat;
		data = JSON.stringify(data);
	
		httpRequest.send(data);
	}
}

function handleRmCat(httpRequest, cat) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 204) {
			selectCat.remove(selectCat.selectedIndex);
			xSelectCat.remove(selectCat.selectedIndex);
			updatePage();
		} else {
			alert("There was a problem with the delete request.");
		}
		logStatus(httpRequest);
	}
}

function sendTransaction() {
	var httpRequest = new XMLHttpRequest();

	var name = xName.value;
	var date = xDate.value;
	var total = xTotal.value;
	var cat = xSelectCat.options[xSelectCat.selectedIndex].text;

	httpRequest.onreadystatechange = function() { handleSendTransaction(httpRequest) };

	httpRequest.open("PUT", "/api/transactions", true);
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	var data = new Object();
	data.name = name;
	data.date = date;
	data.total = total;
	data.category = cat;
	data = JSON.stringify(data);

	httpRequest.send(data);
}

function handleSendTransaction(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 201) {	
			xName.value = "";
			xDate.value = "";
			xTotal.value = "";
			xSelectCat.selectedIndex = 0;
			updatePage();
		} else {
			alert("There was a problem with the put request.");
		}
		logStatus(httpRequest);
	}
}

function logStatus(xhr) {
	console.log("📡\t" + xhr.status + "\t" + xhr.responseText);
}

function updatePage() {
	getCats();

	colorize(['page']);
	colorizeText(['page'], true);
}
