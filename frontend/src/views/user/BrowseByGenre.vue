<template>
    <UserNavbar/>
    <div class="container-lg">
        <div v-if="this.books.length > 0">
            <div v-for="row in books" :key="row.id">
              <div class="row m-5">
                  <div class="card-container">
                    <div v-for="book in row" :key="book.id">
                        <div class="card">
                            <img v-bind:src="book.cover_pic" alt="">
                            <div class="card-content">
                                <div class="details">
                                  <h4>{{ book.name }}</h4>
                                  <p>{{ book.author }}</p>
                                </div>
                                <button class="btn btn-primary" v-on:click="viewBook(book.id)">See More</button>
                            </div>
                        </div>
                    </div>
                  </div>
              </div>
          </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import UserNavbar from '@/components/UserNavbar.vue'

export default {
    components: {UserNavbar},
    data() {
        return {
            books: [],
        }
    },

    created() {
        this.getBooks(this.$route.fullPath.split("/").pop());
    },

    methods: {
        getBooks(genre) {
            axios.get(`user/browse/${genre}`)
            .then((response) => {
                this.books = response.data.books;
            })
            .catch((error) => {
                console.log(error.response.data);
            })
        },

        viewBook(bookID) {
            this.$router.push(`/books/${bookID}`);
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
    width: 15vw;
    margin: 20px;
}

.card img {
    height: 300px;
}
.card-content {
    padding: 15px;
}

.card-content a {
    margin-top: 5px;
    margin-bottom: 5px;
}


.details {
    height: 15vh;
}
</style>