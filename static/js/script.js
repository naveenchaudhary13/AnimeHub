function filterGenre(slug, btn) {
	// Hide all groups
	document
		.querySelectorAll(".anime-group")
		.forEach((g) => g.classList.add("hidden"));

	// Show selected group
	if (slug === "all") {
		document.querySelector(".genre-all").classList.remove("hidden");
	} else {
		document.querySelector(`.genre-${slug}`).classList.remove("hidden");
	}

	// Active button logic
	document.querySelectorAll(".genre-btn").forEach((b) => {
		b.classList.remove("active-genre", "bg-purple-700", "text-white");
		b.classList.add("bg-gray-200", "text-gray-800");
	});

	btn.classList.remove("bg-gray-200", "text-gray-800");
	btn.classList.add("active-genre", "bg-purple-700", "text-white");
}
