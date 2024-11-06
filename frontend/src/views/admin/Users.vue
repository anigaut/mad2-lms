<template>
    <AdminNavbar/>
    <table class="m-5">
        <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Action</th>
        </tr>
        <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.first_name }}</td>
            <td>{{ user.last_name }}</td>
            <td>{{ user.email }}</td>
            <td><button class="btn btn-dark" v-on:click="deleteUser(user.id)">Remove</button></td>
        </tr>
    </table>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue'
import axios from 'axios';
export default {
    components: {AdminNavbar},

    data () {
        return {
            users: []
        }
    },

    created() {
        this.getUsers();
    },

    methods: {
        getUsers() {
            axios.get("admin/get_users")
            .then((response) => {
                this.users = response.data.users;
                console.log(response.data.users);
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

        deleteUser(userID) {
            axios.delete(`admin/delete_user/${userID}`)
            .then((response) => {
                this.users = response.data.users;
                this.$toast.success(response.data.msg, {position: "top-right"});
            })
            .catch((error) => {
                this.$toast.error(error.response.data.msg, {position: "top-right"});
                console.log(error.response.data)
            })
        }
    }

}
</script>

<style scoped>
    table, th, td{
        border: 0.5px solid black;
        text-align: center;
        padding: 10px;
        width: 90vw;
    }

    .action {
        color: red;
    }
</style>