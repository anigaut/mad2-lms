<template>
    <AdminNavbar/>
    <!-- Form to Edit Genre -->
    <div v-if="showEdit">
        <div class="row m-5">
            <div class="col-9">
                <div class="card border-2">
                    <div class="card-body">
                        <!-- <p>{{ genreToEdit }}</p> -->
                        <div class="text-center">
                            <h1 class="card-title">Edit Genre</h1>
                        </div>

                        <form action="/admin/edit_genre" method="POST" enctype="multipart/form-data" v-on:submit.prevent="editGenre(this.genreToEdit.id)">
                            <div class="m-4">
                                <div>
                                    <label class="form-label my-3">Name</label>
                                    <input type="text" class="form-control" v-model="name">
                                </div>

                                <div>
                                    <label class="form-label my-3">Description</label>
                                    <textarea class="form-control" v-model="description">Description</textarea>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary m-4" v-bind:disabled="!this.name">Submit</button>
                        </form>
                        
                        <p v-on:click="this.showEdit = !this.showEdit" class="btn btn-info mx-4">Close</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Form to Add Genre -->
    <div v-if="showAddForm">
        <div class="row m-5">
            <div class="col-9">
                <div class="card border-2">
                    <div class="card-body">
                        <div class="text-center">
                            <h1 class="card-title">Add a Genre</h1>
                        </div>

                        <form action="/admin/add_genre" method="POST" enctype="multipart/form-data" v-on:submit.prevent="addGenre">
                            <div class="m-4">
                                <div>
                                    <label class="form-label my-3">Name</label>
                                    <input type="text" class="form-control" v-model="name" required>
                                </div>

                                <div>
                                    <label class="form-label my-3">Description</label>
                                    <textarea class="form-control" v-model="description">Description</textarea>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary m-4" v-bind:disabled="!this.name">Submit</button>
                        </form>
                        
                        <p v-on:click="this.showAddForm = !this.showAddForm" class="btn btn-info mx-4">Close</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Display all genres -->
    <table class="m-5">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Action</th>
        </tr>
        <tr v-for="genre in genres" :key="genre.id">
            <td>{{ genre.id }}</td>
            <td>{{ genre.name }}</td>
            <td>{{ genre.description }}</td>
            <td>
                <button class="btn btn-dark mx-2" v-on:click="editForm(genre.id)">Edit</button>
                <button class="btn btn-dark" v-on:click="deleteGenre(genre.id)">Remove</button>
            </td>
        </tr>
    </table>

    <button class="btn btn-dark mx-5" v-on:click="showAddForm = !showAddForm">Add New Genre</button>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue'
import axios from 'axios';
export default {
    components: {AdminNavbar},
    data () {
        return {
            name: "",
            description: "",
            genres: [],
            showAddForm: false,
            showEdit: false,
            genreToEdit: ""

        }
    },

    created() {
        this.getGenres();
    },

    methods: {
        getGenres() {
            axios.get("admin/get_genres")
            .then((response) => {
                this.genres = response.data.genres;
                console.log(response.data.genres);
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

        addGenre() {
            axios.post("admin/add_genre", {name: this.name, description: this.description})
            .then((response) => {
                this.genres = response.data.genres;
                this.$toast.success(response.data.msg, {position: "top-right"});
                this.showAddForm = !this.showAddForm;
            })
            .catch((error) => {
                this.$toast.error(error.response.data.msg, {position: "top-right"});
                console.log(error.response.data);
                  
            })
        },

        deleteGenre(genreID) {
            axios.delete(`admin/delete_genre/${genreID}`)
            .then((response) => {
                this.genres = response.data.genres;
                this.$toast.success(response.data.msg, {position: "top-right"});
            })
            .catch((error) => {
                this.$toast.error(error.response.data.msg, {position: "top-right"});
                console.log(error.response.data)
            })
        },

        editForm(id) {
            this.showEdit = !this.showEdit;
            for (let i = 0 ; i < this.genres.length ; i++) {
                if (this.genres[i].id === id) {
                    this.genreToEdit = this.genres[i];
                    break
                }
            }
        },

        editGenre(genreID) {
            axios.post(`admin/edit_genre/${genreID}`, {name: this.name, description: this.description})
            .then((response) => {
                this.genres = response.data.genres;
                this.$toast.success(response.data.msg, {position: "top-right"});
                this.showEdit = !this.showEdit;
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