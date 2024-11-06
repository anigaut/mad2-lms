<template>
    <AdminNavbar/>
    <div class="container-lg">
        <div class="row">
            <div class="card-container">
                <div class="card">
                    <div class="card-content">
                        <h4>Ongoing Borrowings</h4>
                        <p>View the books currently borrowed by users and revoke access if the user has been had the book for more than 7 days</p>
                        <a href="/admin/borrowings" class="btn btn-primary">GO</a>
                    </div>
                </div>
        
                <div class="card">
                    <div class="card-content">
                        <h4>Pending Requests</h4>
                        <p>Requests for Borrowings that have not been approved yet</p>
                        <a href="/admin/requests" class="btn btn-primary">GO</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="card-container">
                <div class="card">
                    <div class="card-content">
                        <h4>Manage Books</h4>
                        <p>Add, Remove and Edit the Existing Books in the Library</p>
                        <a href="/admin/books" class="btn btn-primary">GO</a>
                    </div>
                </div>
        
                <div class="card">
                    <div class="card-content">
                        <h4>Manage Genres</h4>
                        <p>Add, Remove and Edit the Existing Genres in the Library and edit the books in each genre</p>
                        <a href="/admin/genres" class="btn btn-primary">GO</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="card-container">    
                <div class="card">
                    <div class="card-content">
                        <h4>Users</h4>
                        <p>View and Manage the Users Registered to the app</p>
                        <a href="/admin/users" class="btn btn-primary">GO</a>
                    </div>
                </div>

                <div class="card">
                    <div class="card-content">
                        <h4>Generate User Activity Report</h4>
                        <p>Download a report in CSV format that contains all borrowing data</p>
                        <div v-if="downloadTriggered">
                            <button v-on:click="downloadCSV(this.taskID)" class="btn btn-primary mt-2">Download</button>
                        </div>

                        <div v-else>
                            <button v-on:click="generateCSV" class="btn btn-primary">GO</button> <br>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue'
import axios from 'axios';
export default {
    components: {AdminNavbar},

    data() {
        return {
            downloadTriggered: false,
            taskID: ""
        }
    },

    created() {
        this.authCheck();
    },

    methods: {
        authCheck() {
            if (localStorage.getItem("accessToken")) {
                if (localStorage.getItem("userInfo")) {
                    this.$router.push("/");
                    this.$toast.error("Users Cannot Access This Page", {position: "top-right"});
                }
            } else {
                this.$router.push("/admin/login");
                this.$toast.error("Please Login to Access This Page", {position: "top-right"});
            }
        },

        generateCSV() {
            axios.get("admin/generate_report")
            .then(response => {
                this.$toast.success(response.data.msg, {position: "top-right"});
                this.taskID = response.data.taskID;
                this.downloadTriggered = !this.downloadTriggered;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },

        downloadCSV(taskID) {
            axios.get(`admin/download_report/${taskID}`)
            .then(response => {
                this.$toast.success("Report Downloaded Successfully", {position: "top-right"});
                window.location.href = `http://127.0.0.1:5000/api/admin/download_report/${taskID}`
            })
            .catch(error => {
                this.$toast.error(error.response.data.msg, {position: "top-right"})
            })
        }
    }
}
</script>

<style scoped>
.card-container {
    display: flex;
    justify-content: center;
}

.card {
    width: 50vw;
    margin: 20px;
}

.card-content {
    padding: 15px;
}
</style>