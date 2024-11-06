<template>
    <UserNavbar/>
    <div class="container-lg">
        <h1 class="mt-5 text-center">{{ book.name }}</h1>
        <p class="mb-5 text-center">{{ book.author }}</p>
        
        <iframe v-bind:src="book.pdf_file + '#toolbar=0'" width="100%" height="600px" style="border: none; margin-bottom: 100px;"></iframe>
    </div>
</template>

<script>
import UserNavbar from '@/components/UserNavbar.vue'
import axios from 'axios';

export default {
    components: {UserNavbar},
    data() {
        return {
            book: {}
        }
    },

    created() {
        this.readBook(this.$route.fullPath.split("/").pop())
    },

    methods: {
        readBook(bookID) {
            axios.get(`user/read_book/${bookID}`, {headers: {Authorization: `Bearer ${localStorage.getItem("accessToken")}`}})
            .then((response) => {
                this.book = response.data.book;
            }) 
            .catch((error) => {
                console.log(error.response.data);
                if (localStorage.getItem("adminInfo")) {
                    this.$router.push("/admin");
                    this.$toast.error("Access Denied", {position:"top-right"});
                } else if (!localStorage.getItem("accessToken")) {
                    this.$router.push("/login");
                    this.$toast.error("Please Login to Continue", {position: "top-right"});
                } else {
                    this.$router.push("/");
                    this.$toast.error(error.response.data.msg, {position: "top-right"});
                }
            })
        }
    }
}
</script>