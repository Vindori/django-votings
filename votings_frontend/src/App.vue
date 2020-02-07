<template>
    <div>
        <fixed-header>
            <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
                <div class="container d-flex justify-content-between">
                    <a class="navbar-brand" href="#">
                        <img width="40px" height="40px" src="{% static 'images/logo.png' %}">
                        Polls
                    </a>
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
                    aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarCollapse">
                        <ul class="navbar-nav mr-auto">
                            <li class="btn btn-danger btn-block">Add poll</li>
                        </ul>
                        <li class="navbar-nav mr-right btn btn-info" @click="show_modal('hello-world')">LogIn</li>
                        <li class="navbar-nav mr-right nav-item dropdown dropdown-menu-right">
                            <a class="btn btn-outline-primary my-2 my-sm-0 dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Log In</a>
                            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                                <form class="w-100 px-4 py-3">
                                    <div class="form-group form-inline">
                                        <input v-model="login_form['username']" type="text" class="form-control" placeholder="Username" required="required" name="login_username">
                                        <input v-model="login_form['password']" type="password" class="form-control" placeholder="Password" required="required" name="login_password">
                                    </div>
                                    <li @click="logIn()" class="btn btn-primary btn-block">Go for it!</li>
                                </form>
                            </div>
                        </li>
                        <li class="navbar-nav mr-right nav-item dropdown dropdown-menu-right">
                            <a class="btn btn-outline-primary my-2 my-sm-0 dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Sign Up</a>
                            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                                <form class="w-100 px-4 py-3">
                                    <div class="form-group form-inline">
                                        <input v-model="signup_form['username']" type="text" class="form-control" placeholder="Username" required="required" name="singup_username">
                                        <input v-model="signup_form['email']" type="text" class="form-control" placeholder="Email" required="required" name="singup_email">
                                        <input v-model="signup_form['password']" type="password" class="form-control" placeholder="Password" required="required" name="singup_password">
                                    </div>
                                    <li @click="signUp()" class="btn btn-primary btn-block">Go for it!</li>
                                </form>
                            </div>
                        </li>
                    </div>
                </div>
            </nav>
        </fixed-header>
        <div class="main wrapper">
            <ul class="list-group">
                <li
                v-for="poll in polls"
                class="list-group-item list-group-item-action"
                :class="{ active: poll.access_token == selected }"
                @click="showPoll(poll.access_token); selected = poll.access_token">
                    <a>{{ poll.topic }}</a>
                </li>
            </ul>
        </div>
        <h1>{{ poll.topic }}</h1>
        <h2>{{ poll.description }}</h2>
        <li class="btn btn-primary btn-block" @click="vote(index)" v-for="(choice, index) in poll.choices">{{ choice.label }}: {{ choice.votes }}</li>
        <div id="chart">
            <apexchart type="pie" width="380" :options="chartOptions" :series="series"></apexchart>
        </div>
        <flash-message></flash-message>
        <modal name="hello-world">
            <div class="form-group">
                <input v-model="login_form['username']" type="text" class="form-control" placeholder="Username" required="required" name="login_username">
                <input v-model="login_form['password']" type="password" class="form-control" placeholder="Password" required="required" name="login_password">
            </div>
            <li @click="logIn()" class="btn btn-primary btn-block">Go for it!</li>
        </modal>
    </div>
</template>

<script>
    export default {
        name: 'Main',
        data: function() {
            return {
                series: [],
                polls: [],
                poll: {},
                selected: null,
                timer: null,
                login_form: {},
                signup_form: {},
                token: null,
                chartOptions: {
                    chart: {
                        width: 380,
                        type: 'pie',
                    },
                    labels: [],
                    responsive: [{
                        breakpoint: 480,
                        options: {
                            chart: {
                                width: 200
                            },
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }],
                },
            }
        },
        methods: {
            show_modal: function(modal) {
                this.$modal.show(modal);
            },
            vote: function(index) {
                let data = {id: this.poll.choices[index].id, question: this.poll.access_token};
                this.$http
                .post("/vote/", data)
                .then((response) => {
                    this.showPoll(this.poll.access_token);
                    this.flashSuccess(response.data.success, {timeout: 3000});
                    },
                    (error) => {
                    this.flashError(error.response.data.error, {timeout: 3000});
                });
            },
            logIn: function () {
                let data = this.login_form;
                console.log(data);
                this.$http
                .post("/auth/", data)
                .then(
                    (response) => {
                        this.token = response.data.token;
                        this.flashSuccess("You have logged in successfully.", {timeout: 3000})
                    },
                    (error) => {
                        this.flashError(error.response.data.error, {timeout: 3000});
                });
            },
            signUp: function () {
                let data = this.signup_form;
                console.log(data);
                this.$http
                .put("/auth/", data)
                .then(
                    (response) => {
                        this.flashSuccess(response.data.success, {timeout: 3000});
                    },
                    (error) => {
                        this.flashError(error.response.data.error, {timeout: 3000});
                });
            },
            showPoll: function (desc) {
                this.$http
                .get(`/questions/${desc}/`)
                .then(
                    (response) => {
                        this.poll = response.data
                    },
                    (error) => {
                        this.flashError('Backend is DOWN.', {timeout: 3000});
                });
            },
            updatePolls: function () {
                this.$http
                .get("/questions/")
                .then(
                    (response) => {
                        this.polls = response.data
                    },
                    (error) => {
                        this.flashError('Backend is DOWN.', {timeout: 3000});
                });
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
                this.$http.defaults.headers.common["Authorization"] = `Token ${this.token}`;
                if (!this.token) {
                    this.$http.defaults.headers.common["Authorization"] = "";
                }
                this.updatePolls();
            },
            poll: function() {
                let s = [];
                let labels = [];
                for (let p of this.poll.choices)
                {
                    s.push(p.votes);
                    labels.push(p.label);
                }
                this.series = s;
                this.chartOptions = {
                    ...this.chartOptions,
                    ...{
                        labels: labels
                    }
                };
            },
        },
        mounted: function() {
            this.token = localStorage.getItem("token");
            if (this.token) {
                this.$http.defaults.headers.common["Authorization"] = `Token ${this.token}`;
            }
            this.timer = setInterval(this.updatePolls, 30 * 1000);
        },
    }
</script>

<style>
    div.main{
        align-items: center;
        margin: auto;
        margin-left: 0px;
        margin-top: 50px;
    }
    .wrapper {
        display: flex;
        width: 100%;
        align-items: stretch;
    }
</style>
