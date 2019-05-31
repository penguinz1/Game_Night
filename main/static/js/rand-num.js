var start = document.getElementById("start-num") // starting index
var end = document.getElementById("end-num") // ending index
var output = document.getElementById("rand-output") // output message
var warning = document.getElementById("rand-warn") // warning message
var submit = document.getElementById("pick-rand") // submit button

// creates a random number in the range [start, end]
submit.addEventListener("click", () => {
	output.style.display = "none";
	warning.style.display = "none";
	let start_ind = parseInt(start.getAttribute('value'));
	let end_ind = parseInt(end.getAttribute('value'));
	let r_ind = parseInt(focus.value);
	if (end_ind < start_ind) {
		warning.innerHTML = "Error: Start > End";
		warning.style.display = "block";
		return;
	}

	let dist = end_ind - start_ind;
	let rand_selection = make_random(dist, r_ind)
	let pick = rand_selection[0] + start_ind;

	output.innerHTML = "Random number generated: " + pick;
	output.style.display = "block";
	focus.value = rand_selection[1]; // updates random index
})
