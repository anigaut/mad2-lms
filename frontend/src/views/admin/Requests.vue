<template>
    <AdminNavbar/>
    <table class="m-5">
        <tr>
            <th>Book</th>
            <th>User ID</th>
            <th>Action</th>
        </tr>

        <tr v-for="request in requests" :key="request.id">
            <td>{{ request.book_name }}</td>
            <td>{{ request.user_id }}</td>
            <td>
                <button class="btn btn-dark mx-2" v-on:click="approveRequest(request.id)">Approve</button>
                <button class="btn btn-dark mx-2" v-on:click="rejectRequest(request.id)">Reject</button>
            </td>
        </tr>
    </table>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue'
import axios from 'axios';

export default {
    components: {AdminNavbar},
    data() {
        return {
            requests: []
        }
    },

    created() {
        this.getRequests();
    },

    methods: {
        getRequests() {
            axios.get("admin/get_requests")
            .then((response) => {
                this.requests = response.data.requests;
                console.log(response.data);
            })
            .catch((error) => {
                if (localStorage.getItem("userInfo")) {
                    console.log(error.response.data);
                    this.$router.push("/");
                    this.$toast.error("Access Denied", {position:"top-right"})
                } else {
                    console.log(error.response.data);
                    this.$router.push("/admin/login");
                    this.$toast.error("Please Login to Continue", {position: "top-right"})
                }
            })
        },

        approveRequest(requestID) {
            axios.get(`admin/approve_request/${requestID}`)
            .then((response) => {
                this.requests = response.data.requests;
                this.$toast.success(response.data.msg, {position: "top-right"})
            })
            .catch((error) => {
                console.log(error.response.data);
            })
        },

        rejectRequest(requestID) {
            axios.delete(`admin/reject_request/${requestID}`)
            .then((response) => {
                this.requests = response.data.requests;
                this.$toast.success(response.data.msg, {position: "top-right"})
            })
            .catch((error) => {
                console.log(error.response.data);
            })
        }
    }
}
</script>

<style scoped>
table, th, td {
    border: 0.5px solid black;
    width: 90vw;
    padding: 10px;
    text-align: center;
}
</style>