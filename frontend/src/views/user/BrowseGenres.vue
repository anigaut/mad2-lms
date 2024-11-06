<template>
    <UserNavbar/>
    <div class="container-lg">
        <div class="card bg-info-subtle mt-5" style="width: 100%;">
            <div class="card-body">
                <h1>Select the Genre You'd Like to Explore</h1>
            </div>
        </div>

        <div v-if="this.genres.length > 0">
            <div v-for="row in genres" :key="row.id">
                <div class="card-container">
                    <div v-for="genre in row" :key="genre.id">
                        <div class="card">
                            <div class="card-content">
                                <div class="details">
                                    <h4>{{ genre.name }}</h4>
                                    <p>{{ genre.description }}</p>
                                </div>
                                <button class="btn btn-primary" v-on:click="exploreGenre(genre.id)">See More</button>
                            </div>
                        </div>
                    </div>
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
            genres: [],
        }
    },

    created() {
        this.getGenres();
    },

    methods: {
        getGenres() {
            axios.get("user/browse")
            .then((response) => {
                this.genres = response.data.genres;
                console.log(response.data.genres);
            })
            .catch((error) => {
                console.log(error.response.data);
            })
        },

        exploreGenre(genreID) {
            this.$router.push(`/genres/${genreID}`);
         }
    },
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

.card-content {
    padding: 15px;
}

.card-content a {
    margin-top: 5px;
    margin-bottom: 5px;
}

.details {
    height: 35vh;
}
</style>