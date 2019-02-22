const myDiv = document.getElementById("dataapi");

var request = new XMLHttpRequest();

request.open('GET', 'https://api.oehu.org/devices', true);
request.onload = function () {
  var data = JSON.parse(this.response);

   if (request.status >= 200 && request.status < 400) {
    data.forEach(device => {
        var checkBox = document.createElement("input");
        var label = document.createElement("label");
        checkBox.type = "checkbox";
		checkBox.id = "ankush";
        checkBox.value = device.deviceId;
		var br = document.createElement("br");
        myDiv.appendChild(br);
        myDiv.appendChild(checkBox);
        myDiv.appendChild(label);
        label.appendChild(document.createTextNode(device.deviceId));
    });
  } else {
    console.log('error');
  }
}
request.send();
function myFunction() {
  	document.getElementById("source").value = "Hey"
}
