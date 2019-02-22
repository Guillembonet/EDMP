function sell() {
	var json = new URLSearchParams({

			first_asset_amount: $('#price').val(),

			first_asset_type: $('#currency').val(),

			second_asset_amount: '1',

			second_asset_type: 'EW' + $('#hash').val()

		});

	var xhr = new XMLHttpRequest();
	xhr.open("PUT", 'http://localhost:8080/market/asks', true);
	xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
	xhr.onload = function () {
		var data = JSON.parse(xhr.responseText);
		console.log(data)
		if (xhr.status == 200) alert('ask created successfully')
	}
	xhr.send(json);

}

function buy(hash, price, currency) {
	var json = new URLSearchParams({

			first_asset_amount: price,

			first_asset_type: currency,

			second_asset_amount: '1',

			second_asset_type: hash

		});

	var xhr = new XMLHttpRequest();
	xhr.open("PUT", 'http://localhost:8080/market/bids', true);
	xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
	xhr.onload = function () {
		var data = JSON.parse(xhr.responseText);
		console.log(data)
		if (xhr.status == 200) {
			alert('bid created successfully')
			alert('You can copy the hash: ' + hash.replace(/^EW/, ""))
			location.reload();
		}
	}
	console.log(json)
	xhr.send(json);
}



function getAsks() {

	var xhr = new XMLHttpRequest();
	xhr.open("GET", 'http://localhost:8080/market/asks', true);
	xhr.onload = function () {
		var data = JSON.parse(xhr.responseText);
		data.asks.forEach(function(element) {
			console.log(element);
			if (element.ticks.length == 1) {
				var b = document.createElement("button");
				b.className = "list-group-item list-group-item-action";
				b.appendChild(document.createTextNode(element.asset2));
				document.getElementById("myList").appendChild(b);
				var span = document.createElement("span");
				span.className = "badge badge-primary badge-pill";
				span.appendChild(document.createTextNode(element.ticks[0].assets.first.amount + ' ' + element.asset1));
				b.appendChild(span)
				b.addEventListener('click', function() {
				    buy(element.asset2, element.ticks[0].assets.first.amount, element.asset1);
				}, false);
			}
		});

	}
	xhr.send();
}
