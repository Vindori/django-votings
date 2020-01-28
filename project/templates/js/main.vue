var app = new Vue({
	delimiters: ["[[", "]]"],
	el: "#app",
	data: {
			polls: null,
			poll: {},
			selected: null,
			timer: null,
			login_form: {},
			signup_form: {},
			token: null,
	},
	methods: {
			logIn: function () {
				let data = this.login_form;
				console.log(data);
				axios
				.post({% url "api_auth" %}, data)
				.then((response) =>{
					this.token = response.data.token;
				});
			},
			signUp: function () {
				let data = this.signup_form;
				console.log(data);
				axios
				.put({% url "api_auth" %}, data)
				.then((response) =>{
					console.log(response.data);
				});
			},
			showPoll: function (desc) {
				axios
				.get(`{% url "votings:questions-list" %}${desc}/`)
				.then(response => (this.poll = response.data),
					  error => (this.errors.push(error))
				);
			},
			updatePolls: function () {
				axios
				.get("{% url "votings:questions-list" %}")
				.then(response => (this.polls = response.data),
					  error => (this.errors.push(error))
				);
			},
			timeSince: function (cr_date) {
				date = new Date(cr_date);
				var seconds = Math.floor((new Date() - date) / 1000 + 3600 * 3);

				var interval = Math.floor(seconds / 31536000);

				if (interval > 1) {
					return interval + " years ago";
				}
				interval = Math.floor(seconds / 2592000);
				if (interval > 1) {
					return interval + " months ago";
				}
				interval = Math.floor(seconds / 86400);
				if (interval > 1) {
					return interval + " days ago";
				}
				interval = Math.floor(seconds / 3600);
				if (interval > 1) {
					return interval + " hours ago";
				}
				interval = Math.floor(seconds / 60);
				if (interval > 1) {
					return interval + " minutes ago";
				}
				if (seconds > 0) {
					return Math.floor(seconds) + " seconds ago";
				}
				return "in the far future";
			}
	},
	watch: {
		token: function() {
			localStorage.setItem("token", this.token);
			axios.defaults.headers.common["Authorization"] = `Token ${this.token}`;
			if (!this.token) {
				axios.defaults.headers.common["Authorization"] = "";
			}
			this.updatePolls();
		}
	},
	mounted: function() {
		this.token = localStorage.getItem("token");
		if (this.token) {
			axios.defaults.headers.common["Authorization"] = `Token ${this.token}`;
		}
		this.timer = setInterval(this.updatePolls, 30 * 1000);
	},
});