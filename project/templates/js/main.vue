var app = new Vue({
	delimiters: ['[[', ']]'],
	el: '#app',
	data: {
			polls: null,
			description: null,
			selected: null,
			hovered: null,
			timer: null,
	},
	methods: {
			timeSince2: function (cr_date) {
				alert(timeSince(cr_date));
			},
			showDesc: function (desc) {
				this.description = desc;
				this.selected = null;
			},
			updatePolls: function () {
				axios
				.get("{% url 'votings:questions-list' %}")
				.then(response => (this.polls = response.data));
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
	beforeMount: function() {
				this.updatePolls();
				this.timer = setInterval(this.updatePolls, 30 * 1000)
			},
});