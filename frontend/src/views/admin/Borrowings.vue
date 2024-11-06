<template>
    <AdminNavbar/>
    <table class="m-5">
        <tr>
            <th>Book</th>
            <th>User ID</th>
            <th>Time Issued</th>
            <th>Expiry Time</th>
            <th>Access</th>
        </tr>

        <tr v-for="borrowing in borrowings" :key="borrowing.id">
            <td>{{ borrowing.book_name }}</td>
            <td>{{ borrowing.user_id }}</td>
            <td>{{ borrowing.time }}</td>
             <td>{{ borrowing.expiry }}</td>
             <td><button class="btn btn-dark" v-on:click="revokeAccess(borrowing.id)">Revoke Access</button></td>
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
            borrowings: []
        }
    },

    created() {
        this.getBorrowings();
    },

    methods: {
        getBorrowings() {
            axios.get("admin/get_borrowings")
            .then((response) => {
                this.borrowings = response.data.borrowings;
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

        revokeAccess(borrowingID) {
            axios.delete(`admin/revoke_access/${borrowingID}`)
            .then((response) => {
                this.borrowings = response.data.borrowings;
                console.log(response.data);
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
    text-align: center;
    padding: 10px;
    }
</style>