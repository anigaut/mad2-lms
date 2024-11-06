<template>
    <div>
        <div v-if="isLoggedIn">
          <nav>
            <div class="logo">
                <a href="/">
                  <img src="/src/assets/logo.png" style="width: 45px; height: 45px;">
                    OPUS BOOKS
                </a>
            </div>

            <form action="user/search" class="d-flex" role="search" method="POST" v-on:submit.prevent="search">
                <input class="form-control me-2" type="search" placeholder="Search by Book, Genre or Author" aria-label="Search" v-model="searchQuery">
                <button class="btn btn-outline-dark" type="submit" v-on:click="search(this.searchQuery)">Search</button>
            </form>

            <div class="nav-links">
              <a href="/browse-genres" class="nav-link">Browse</a>
              <button class="btn btn-dark mx-4" v-on:click="userLogout">Logout</button>
            </div>
          </nav>
        </div>

        <div v-else>
          <nav>
            <div class="logo">
                <a href="/">
                  <img src="/src/assets/logo.png" style="width: 45px; height: 45px;">
                    OPUS BOOKS
                </a>
            </div>

            <form action="user/search" class="d-flex" role="search" method="POST" v-on:submit.prevent="search">
                <input class="form-control me-2" type="search" placeholder="Search by Book, Genre or Author" aria-label="Search" v-model="searchQuery">
                <button class="btn btn-outline-dark" type="submit" v-on:click="search(this.searchQuery)">Search</button>
            </form>

            <div class="nav-links">
                <a href="/browse-genres" class="nav-link">Browse</a>
                <router-link to="/login" class="btn btn-dark">Login</router-link>
                <router-link to="/register" class="btn btn-dark">Register</router-link>
            </div>
          </nav>
        </div>      
    </div>
</template>

<script>
import { isLoggedIn } from '@/auth';
import axios from 'axios';
export default {
  data () {
    return {
        errorMessage: "",
        isLoggedIn: isLoggedIn(),
        showLogin: false,
        searchQuery: "",
    }
  },

  methods: {
    userLogout () {
      axios.post("user/logout", {headers: {Authorization: `Bearer ${localStorage.getItem("accessToken")}`}})
      .then((response) => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("userInfo");
        this.$router.push("/login");
        this.$toast.success(response.data.msg, {position: "top-right"});
      })
      .catch((error) => {
        console.log(error.response.data);
      })
    },

    search(query) {
      this.$router.push(`/search/${this.searchQuery}`);
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
    background: lightgreen;
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

form {
    width: 40vw;
}
</style>