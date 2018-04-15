//erl67
//this uses the same AJAX as before, only to GET the data
//and the response is automatically parsed to JSON
var categories = {}, transactions = {};
var catsDiv, totalCatsDiv;
var totalX, xNames;
var temp;

document.addEventListener("DOMContentLoaded", function() {
	window.onload = prepare;
});

function prepare() {
	updatePage();

	catsDiv = document.getElementById('cats');
	totalCatsDiv = document.getElementById('totalCats');
	totalX = document.getElementById('totalX');
	xNames = document.getElementById('xNames');

	setTimeout(function() {
		if (categories){
			populateCats(categories);
			totalCats(categories);
		}
		if (transactions){
			totalTransactions(transactions);
			transactionNames(transactions);
		}
		updatePage();
	}, 1000);
}

function transactionNames(arr) {
	temp = Object.keys(arr).map(function(key, index) {
		return arr[key].name;
	});
	temp = temp.sort().toString().replace(/,/g, ',  ');
	xNames.innerHTML += temp;
}

function populateCats(arr) {
	temp = Object.keys(arr).map(function(key, index) {
		return arr[key];
	});
	temp = temp.sort().toString().replace(/,/g, ',  ');
	catsDiv.innerHTML += temp;
}

function totalCats(arr) {
	temp = Object.keys(arr).reduce(function(acc, cv) {
		return parseInt(acc) + 1
	}, 0);
	totalCatsDiv.innerHTML += temp;
}

function totalTransactions(arr) {
	temp = Object.keys(arr).reduce(function(acc, cv) {
		return parseInt(acc) + 1
	}, 0);
	totalX.innerHTML += temp;
}

function getCats() {
	var httpRequest = new XMLHttpRequest();

	httpRequest.onreadystatechange = function() {
		handleGetCats(httpRequest)
	};

	httpRequest.open("GET", "/api/cats", true);
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	httpRequest.send();
}

function handleGetCats(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			categories = httpRequest.responseText ? JSON
					.parse(httpRequest.responseText) : httpRequest.responseText;
		} else if (httpRequest.status === 401) {
		} else {
			alert("There was a problem with the get request.");
		}
		logStatus(httpRequest);
	}
}

function getTransactions() {
	var httpRequest = new XMLHttpRequest();

	httpRequest.onreadystatechange = function() {
		handleGetTransactions(httpRequest)
	};

	httpRequest.open("GET", "/api/transactions", true);
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	httpRequest.send();
}

function handleGetTransactions(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			transactions = httpRequest.responseText ? JSON
					.parse(httpRequest.responseText) : httpRequest.responseText;
		} else if (httpRequest.status === 401) {
		} else {
			alert("There was a problem with the get request.");
		}
		logStatus(httpRequest);
	}
}

function logStatus(xhr) {
	if (xhr.responseText) {
		console.log("📡\t" + xhr.status + "\n"
				+ JSON.stringify(JSON.parse(xhr.responseText)));
	} else {
		console.log("📡\t" + xhr.status + "\t🛰️" + xhr.responseText);
	}
}

function updatePage() {
	getCats();
	getTransactions();
	colorize(['page']);
	colorizeText(['page'], true);
}
