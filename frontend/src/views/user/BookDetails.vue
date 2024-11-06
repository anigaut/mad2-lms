<template>
    <UserNavbar/>
    <div class="container-lg">
        <div class="page-container">
            <div class="book-cover">
                <img v-bind:src="book.cover_pic">
                <br>
                
                <div v-if="currentlyBorrowed">
                    <button class="btn btn-dark mt-4" v-on:click="openBook(book.id)">Read</button>
                    <button class="btn btn-dark mt-4" v-on:click="returnBook(book.id)">Return</button>
                </div>

                <div v-else-if="purchased">
                    <button class="btn btn-dark mt-4" v-on:click="openBook(book.id)">Read</button>
                </div>

                <div v-else>
                    <button class="btn btn-dark mt-4" v-on:click="requestBook(book.id)">Request to Borrow</button> 
                    <button class="btn btn-dark mt-4" v-on:click="purchaseBook(book.id)">Buy for ₹{{ book.price }}</button> 
                </div>

            </div>

            <div class="book-desc">
                <h1>{{ book.name }}</h1>
                <h5>{{ book.author }}</h5>
                <p>{{ book.genre }}</p>
                <hr>
                <p>{{ book.description }}</p>
            </div>
        </div>

        <div class="review">
            <h2>Reviews</h2><hr>
            <h4>What are your thoughts on this book?</h4>
            <form action="users/add_review" method="POST" v-on:submit.prevent="addReview">
                <textarea class="form-control my-4" v-model="content"></textarea>
                <button type="submit" v-bind:disabled="!this.content" class="btn btn-dark">Submit</button>
            </form>

            <div v-if="this.reviews.length > 0">
                <h4 class="mt-5">Community Reviews</h4><hr>
                <div v-for="review in reviews" :key="review.id">
                    <img src="/src/assets/profile.png" class="me-2">
                    <h6>{{ review.user_first_name }} {{ review.user_last_name }}</h6>
                    <p class="mt-3">{{ review.content }}</p>
                    <br>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserNavbar from "@/components/UserNavbar.vue";
import axios from "axios";
export default {
    components: {UserNavbar},
    data() {
        return {
            book: "",
            reviews: [],
            content: "", 
            currentlyBorrowed: false,
            purchased: false,
            userID: JSON.parse(localStorage.getItem("userInfo"))
        }
    },

    created() {
        this.getBookDetails(this.$route.fullPath.split("/").pop());
    },

    methods: {
        getBookDetails(bookID) {
            axios.get(`user/book_details/${bookID}`, {headers: {Authorization: `Bearer ${localStorage.getItem("accessToken")}`}})
            .then((response) => {
                console.log(response.data);
                this.currentlyBorrowed = response.data.currently_borrowed;
                this.purchased = response.data.purchased;
                this.book = response.data.book;
                this.reviews = response.data.reviews;
            })
            .catch((error) => {
                console.log(error.response.data);
                if (localStorage.getItem("adminInfo")) {
                    this.$router.push("/admin");
                    this.$toast.error("Access Denied", {position:"top-right"});
                } else {
                    this.$router.push("/login");
                    this.$toast.error("Please Login to Continue", {position: "top-right"});
                }
            })
        },

        requestBook(bookID) {
            axios.get(`user/request_book/${bookID}`, {headers: {Authorization:  `Bearer ${localStorage.getItem("accessToken")}`}})
            .then((response) => {
                console.log(response.data);
                this.$toast.success(response.data.msg, {position: "top-right"})
                //this.currentlyBorrowed = !this.currentlyBorrowed;
            })
            .catch((error) => {
                console.log(error.response.data);
                this.$toast.error(error.response.data.msg, {position: "top-right"})
            })
        },

        purchaseBook(bookID) {
            axios.get(`user/purchase_book/${bookID}`, {headers: {Authorization:  `Bearer ${localStorage.getItem("accessToken")}`}})
            .then((response) => {
                console.log(response.data);
                this.$toast.success(response.data.msg, {position: "top-right"})
                this.purchased = !this.purchased;
            })
            .catch((error) => {
                console.log(error.response.data);
                this.$toast.error(error.response.data.msg, {position: "top-right"})
            })
        },

        returnBook(bookID) {
            axios.delete(`user/return_book/${bookID}`, {headers: {Authorization:  `Bearer ${localStorage.getItem("accessToken")}`}})
            .then((response) => {
                this.$toast.success(response.data.msg, {position: "top-right"});
                this.currentlyBorrowed = !this.currentlyBorrowed;
            })
            .catch((error) => {
                console.log(error.response.data);
                this.$toast.error(error.response.data.msg, {position: "top-right"});
            })
        },

        addReview() {
            axios.post("user/add_review", {content: this.content, book_id: this.book.id, user_id: JSON.parse(localStorage.getItem("userInfo")).user_id})
            .then((response) => {
                this.reviews = response.data.reviews;
                this.content = "";
            })
            .catch((error) => {
                console.log(error.response.data);
            })
        },

        openBook(bookID) {
            this.$router.push(`/read/${bookID}`);
        }
    }
}
</script>

<style scoped>
.page-container {
    display: flex;
    margin-left: 250px;
    margin-top: 100px;
}

.page-container img {
    height: 40vh;
    width: 30vh;
}

.page-container button {
    width: 30vh;
}

.book-desc {
    margin-left: 50px;
    margin-right: 300px;
}

.book-cover a {
    display: block;
    margin-top: 30px;
}

.review {
    margin-top: 50px;
    margin-left: 250px;
    margin-right: 300px;
    margin-bottom: 100px;
}

.review h6 {
    display: inline;
}
</style>