<template>
    <UserNavbar/>
    <div class="container-lg">
        <div v-if="this.books.length === 0 && this.genres.length === 0 && this.booksByAuthor.length === 0">
            <div class="card bg-info-subtle mt-5" style="width: 100%;">
                <div class="card-body">
                    <h1>Couldn't Find Any Results for "{{ query }}"</h1>
                </div>
            </div>
        </div>

        <div v-else>
            <div class="card bg-info-subtle mt-5" style="width: 100%;">
                <div class="card-body">
                    <h1>Search Results for "{{ query }}"</h1>
                </div>
            </div>
        </div>

        <!-- Gets all books that match the search query -->
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
                                <a href="#" class="btn btn-primary">See More</a>
                            </div>
                        </div>
                    </div>
                  </div>
              </div>
          </div>
        </div>

        <!-- Gets all books that is by the author searched in the query -->
        <div v-if="this.booksByAuthor.length > 0">
            <div v-for="row in booksByAuthor" :key="row.id">
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
                                <a href="#" class="btn btn-primary">See More</a>
                            </div>
                        </div>
                    </div>
                  </div>
              </div>
          </div>
        </div>

        <!-- Gets all genres that match the query -->
        <div v-if="this.genres.length > 0">
            <div v-for="row in genres" :key="row.id" class="row m-5">
                <div class="card-container">
                    <div v-for="genre in row" :key="genre.id">
                        <div class="card">
                            <div class="card-content">
                                <div class="details">
                                    <h4>Genre: {{ genre.name }}</h4>
                                    <p>{{ genre.description }}</p>
                                </div>
                                <a href="#" class="btn btn-primary">See More</a>
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
            query: this.$route.fullPath.split("/").pop(),
            books: [],
            genres: [],
            booksByAuthor: []
        }
    },

    created() {
        this.search(this.$route.fullPath.split("/").pop());
    },

    methods: {
        search(query) {
            axios.get(`user/search/${query}`)
            .then((response) => {
                this.books = response.data.books;
                this.genres = response.data.genres;
                this.booksByAuthor = response.data.books_by_author;
                console.log(response.data);
            })
            .catch((error) => {
                console.log(error.response.data);
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