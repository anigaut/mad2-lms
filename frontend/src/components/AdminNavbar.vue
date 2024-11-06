<template>
    <div>
        <nav>
            <div class="logo">
                <a href="/admin">
                    OPUS BOOKS (Admin)
                </a>
            </div>

            <div class="nav-links">
                <a href="/admin/books" class="nav-link">Books</a>
                <a href="/admin/genres" class="nav-link">Genres</a>
                <a href="/admin/borrowings" class="nav-link">Borrowings</a>
                <a href="/admin/requests" class="nav-link">Requests</a>
                <a href="/admin/users" class="nav-link">Users</a>
                <button class="btn btn-dark me-5" v-on:click="adminLogout">Logout</button>
            </div>
        </nav>    
    </div>
</template>

<script>
import { isLoggedIn } from '@/auth';
import axios from 'axios';

export default {
  data () {
    return {
        errorMessage: "",
        isLoggedIn: isLoggedIn()
    }
  },

  methods: {
    adminLogout() {
      if (localStorage.getItem("adminInfo")) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('adminInfo');
        this.$router.push("/admin/login");
        this.$toast.success("Logged out Successfully", {position: "top-right"});
      }
    }
  }
}
</script>

<style scoped>
.logo a {
    margin-left: 40px;
    text-decoration: none;
    color: black;
    font-weight: bold;
    font-size: 25px;
}
nav {
    background: lightblue;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 10vh;
}

.nav-links a {
    display: inline-block;
    margin: 20px;
    font-size: 17px;
}

.nav-links a:hover {
    text-decoration: underline;
}
</style>