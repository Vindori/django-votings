<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-default nav_header">
            <div class="container">
                <a class="navbar-brand nav_logo mr-lg-auto" @click="showIndex()">POLLS</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar-default" aria-controls="navbar-default" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <button v-if="Boolean(user)" type="button" class="btn btn-secondary btn-sm btn-outline-success" style="margin-left: 2%;" @click="poll=null; edit_mode=true;">Add</button>
                <div class="collapse navbar-collapse" id="navbar-default">
                    <div class="navbar-collapse-header">
                        <div class="row">
                            <div class="col-6 collapse-close">
                                <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbar-default" aria-controls="navbar-default" aria-expanded="false" aria-label="Toggle navigation">
                                    <span></span>
                                    <span></span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <ul class="navbar-nav ml-lg-auto ml-5 nav_text">
                        <div v-if="!Boolean(user)">
                            <li class="dropdown nav-item">
                                <a class="nav-link nav-link-icon" data-toggle="dropdown" aria-expanded="true">
                                    Login
                                </a>
                                <div class="dropdown-menu">
                                    <form class="w-100 px-4 py-3">
                                        <div class="form-group form-inline">
                                            <input v-model="login_form['username']" type="text" class="form-control" placeholder="Username" required="required" name="login_username">
                                        </div>
                                        <div class="form-group form-inline">
                                            <input v-model="login_form['password']" type="password" class="form-control" placeholder="Password" required="required" name="login_password">
                                        </div>
                                        <li @click="logIn()" class="btn btn-primary btn-block">LogIn</li>
                                    </form>
                                </div>
                            </li>
                            <li class="dropdown nav-item">
                                <a class="nav-link nav-link-icon" data-toggle="dropdown" aria-expanded="true">
                                    Register
                                </a>
                                <div class="dropdown-menu">
                                    <form class="w-100 px-4 py-3">
                                        <div class="form-group form-inline">
                                            <input v-model="signup_form['username']" type="text" class="form-control" placeholder="Username" required="required" name="singup_username">
                                        </div>
                                        <div class="form-group form-inline">
                                            <input v-model="signup_form['email']" type="text" class="form-control" placeholder="Email" required="required" name="singup_email">
                                        </div>
                                        <div class="form-group form-inline">
                                            <input v-model="signup_form['password']" type="password" class="form-control" placeholder="Password" required="required" name="singup_password">
                                        </div>
                                        <li @click="signUp()" class="btn btn-primary btn-block">SignUp</li>
                                    </form>
                                </div>
                            </li>
                        </div>
                        <div v-else>
                            <li class="dropdown nav-item">
                                <a class="nav-link nav-link-icon" data-toggle="dropdown" aria-expanded="true">
                                    {{ user }}
                                </a>
                                <div class="dropdown-menu">
                                    <form class="w-100 px-4 py-3">
                                        <li @click="logout()" class="btn btn-primary btn-block">Logout</li>
                                    </form>
                                </div>
                            </li>
                        </div>
                    </ul>

                </div>
            </div>
        </nav>
        <!--sidebar!-->
        <div class="wrapper d-flex align-items-stretch">
            <nav id="sidebar">
                <div class="custom-menu">
                    <button type="button" id="sidebarCollapse" class="btn btn-primary">
                      <i class="fa fa-bars"></i>
                      <span class="sr-only">Toggle Menu</span>
                  </button>
                </div>
                <div class="p-4 pt-5">
                    <h1><a class="logo">List</a></h1>
                    <ul class="list-unstyled components mb-5">
                        <li class="active">
                            <a href="#homeSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">Public polls</a>
                            <ul class="collapse list-unstyled" id="homeSubmenu">
                                <li
                                v-for="poll in polls"
                                :class="{ active: poll.access_token == selected }"
                                @click="showPoll(poll.access_token); selected = poll.access_token">
                                    <a>{{ poll.topic }}</a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                    <ul class="list-unstyled components mb-5" v-if="user">
                        <li class="active">
                            <a href="#homeSubmenu2" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">My polls</a>
                            <ul class="collapse list-unstyled" id="homeSubmenu2">
                                <li
                                v-for="poll in my_polls"
                                :class="{ active: poll.access_token == selected }"
                                @click="showPoll(poll.access_token); selected = poll.access_token">
                                    <a>{{ poll.topic }}</a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
        <div class="poll" v-if="Boolean(poll)">
            <div v-if="!edit_mode">
                <h1 class="poll_label">{{ poll.topic }}</h1>  
                <p class="poll_desc">{{ poll.description }}</p>
                <div class="poll-btn-cont" v-for="(choice, index) in poll.choices">
                    <button type="button" class="btn btn-vote btn-outline-default btn-lg btn-block" @click="vote(index)">{{ choice.label }}: {{ choice.votes }}</button>
                </div>
                <div class="poll-chg poll-btn-cont" v-if="user == poll.author">
                    <button type="button" class="btn btn-secondary btn-sm btn-outline-default" @click="edit_mode=true">Change</button>
                    <button type="button" class="btn btn-secondary btn-sm btn-outline-danger" @click="deletePoll(poll.access_token)">Delete</button>
                </div>
            </div>
            <div v-else>
                <input style="width: 60%; margin: auto;" v-model="poll['topic']" type="text" class="form-control" placeholder="Topic" required="required">
                <input style="width: 60%; margin: auto;" v-model="poll['description']" type="text" class="form-control" placeholder="Description" required="required">
                <h2>Choices:</h2>
                <div class="poll-btn-cont" v-for="(choice, index) in poll['choices']">
                    <input style="width: 57%; margin: auto;" class="d-inline form-control" required="required" v-model="poll['choices'][index].label" placeholder="Vote"><button class="d-inline btn btn-secondary btn-sm btn-outline-warning" @click="poll['choices'].splice(index, 1)">Del</button>
                </div>
                <div class="custom-control custom-checkbox mb-3">
                    <input class="custom-control-input" id="public" type="checkbox" v-model="poll['public']">
                    <label class="custom-control-label" for="public">Public</label>
                </div>
                <div class="poll-chg poll-btn-cont">
                    <button class="btn btn-secondary btn-sm btn-outline-info" @click="poll['choices'].push({label: ''})">Add</button>
                    <button type="button" @click="editPoll()" class="btn btn-secondary btn-sm btn-outline-default">Save</button>
                </div>
            </div>
        </div>
        <div class="poll" v-else-if="edit_mode">
            <input style="width: 60%; margin: auto;" v-model="create_poll['topic']" type="text" class="form-control" placeholder="Topic" required="required">
            <input style="width: 60%; margin: auto;" v-model="create_poll['description']" type="text" class="form-control" placeholder="Description" required="required">
            <h2>Choices:</h2>
            <div class="poll-btn-cont" v-for="(choice, index) in create_poll['choices']">
                <input style="width: 57%; margin: auto;" class="d-inline form-control" required="required" v-model="create_poll['choices'][index].label" placeholder="Vote"><button class="d-inline btn btn-secondary btn-sm btn-outline-warning" @click="create_poll['choices'].splice(index, 1)">Del</button>
            </div>
            <div class="custom-control custom-checkbox mb-3">
                <input class="custom-control-input" id="public" type="checkbox" v-model="create_poll['public']">
                <label class="custom-control-label" for="public">Public</label>
            </div>
            <div class="poll-chg poll-btn-cont">
                <button class="btn btn-secondary btn-sm btn-outline-info" @click="create_poll['choices'].push({label: ''})">Add</button>
                <button type="button" @click="savePoll()" class="btn btn-secondary btn-sm btn-outline-default">Save</button>
            </div>
        </div>
        <div class="poll" v-else>
            <div class="poll_parag">
                <h1>The best service to create your own public or private polls!</h1>
                <p class="poll_desc">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit</p>
            </div>
        </div>
        <div style="width: 21%; margin: auto; margin-top: 5%" v-if="Boolean(poll) && !edit_mode">
            <apexchart type="pie" width="400" :options="chartOptions" :series="series"></apexchart>
        </div>
        <div style="width: 40%; margin: auto; margin-top: 1%">
            <flash-message></flash-message>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Main',
        data: function() {
            return {
                edit_mode: false,
                series: [],
                polls: [],
                poll: null,
                selected: null,
                timer: null,
                login_form: {},
                signup_form: {},
                token: null,
                user: null,
                my_polls: [],
                create_poll: {choices: [{label:''}, {label:''}], topic: '', description: '', author: '', public: true},
                chartOptions: {
                    dataLabels: {
                        style: {
                            colors: ['#FFFFFF']
                        }
                    },
                    theme: {
                        palette: 'palette10'
                    },
                    legend: {show: false},
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
                            }
                        }
                    }],
                },
            }
        },
        methods: {
            showIndex: function() {
                this.edit_mode = false;
                this.poll = null;
                this.selected = null;
            },
            savePoll: function() {
                let data = this.create_poll;
                this.create_poll = {choices: [{label:''}, {label:''}], topic: '', description: '', author: '', public: true};
                this.$http
                .post(`/questions/`, data)
                .then((response) => {
                    this.showIndex();
                    this.updatePolls();
                    this.getUser();
                });
            },
            editPoll: function() {
                let data = this.poll;
                this.$http
                .patch(`/questions/${this.poll.access_token}/`, data)
                .then((response) => {
                    this.edit_mode = false;
                    this.showPoll(data.access_token);
                });
            },
            deletePoll: function(token) {
                this.$http
                .delete(`/questions/${token}/`)
                .then((response) => {
                    this.flashSuccess('asd', {timeout: 3000});
                    this.showIndex();
                    this.updatePolls();
                    this.getUser();
                });
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
                this.$http
                .post("/auth/", data)
                .then(
                    (response) => {
                        this.token = response.data.token;
                        this.$http.defaults.headers.common["Authorization"] = `Token ${this.token}`;
                        this.flashSuccess("You have logged in successfully.", {timeout: 3000});
                        this.getUser();
                    },
                    (error) => {
                        this.flashError(error.response.data.error, {timeout: 3000});
                });
            },
            signUp: function () {
                let data = this.signup_form;
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
                this.edit_mode = false;
                this.$http
                .get(`/questions/${desc}/`)
                .then(
                    (response) => {
                        this.poll = response.data
                    },
                    (error) => {
                        this.flashError("No such poll.", {timeout: 3000});
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
                        console.log(error.response.data);
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
            },
            getUser: function() {
                this.$http
                .get("/auth/")
                .then(
                    (response) => {
                        this.user = response.data.username;
                        this.my_polls = response.data.questions;
                    },
                    (error) => {
                        console.log(error.response.data);
                });
            },
            logout: function() {
                this.token = "";
                this.user = null;
                this.my_polls = [];
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
            this.token = localStorage.token;
            if (this.token) {
                this.$http.defaults.headers.common["Authorization"] = `Token ${this.token}`;
                this.getUser();
            }
            this.timer = setInterval(this.updatePolls, 30 * 1000);
            if (this.$route.name === "ShowPoll")
            {
                this.showPoll(this.$route.params.id);
            }
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
