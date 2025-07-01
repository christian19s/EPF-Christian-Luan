document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('btnLogin').addEventListener('click', function() {
		window.location.href = "/login";
	});
	document.getElementById('btnCreate').addEventListener('click', function () {
		window.location.href = "/home/create";
	});
});


