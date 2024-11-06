<template>
    <AdminNavbar/>

    <div v-if="this.books.length === 0">
        <h1>No Books Present</h1>
    </div>

    <!-- Form to Add Book -->
    <div v-if="showAddBook">
        <div class="row m-5">
            <div class="col-9">
                <div class="card border-2">
                    <div class="card-body">
                        <div class="text-center">
                            <h1 class="card-title">Add a Book</h1>
                        </div>

                        <form action="/admin/add_book" method="POST" enctype="multipart/form-data" v-on:submit.prevent="addBook">
                            <div class="m-4">
                                <div>
                                    <label class="form-label my-3">Name</label>
                                    <input type="text" class="form-control" v-model="name" required>
                                </div>

                                <div>
                                    <label class="form-label my-3">Author</label>
                                    <input type="text" class="form-control" v-model="author" required>
                                </div>

                                <div>
                                    <label class="form-label my-3">Genre</label>
                                    <select v-model="genre" class="form-select">
                                        <option v-for="genre in genreNames" :key="genre.name">{{ genre }}</option>
                                    </select>
                                </div>

                                <div>
                                    <label class="form-label my-3">Description</label>
                                    <textarea class="form-control" v-model="description">Description</textarea>
                                </div>

                                <div>
                                    <label class="form-label my-3">Price (in ₹)</label>
                                    <input type="number" class="form-control" v-model="price" required>
                                </div>

                                <div>
                                    <label class="form-label my-3">PDF File</label>
                                    <input type="file" class="form-control" v-on:change="handleFileUpload($event, 'pdfFile')" required>
                                </div>

                                <div>
                                    <label class="form-label my-3">Cover Picture</label>
                                    <input type="file" class="form-control" v-on:change="handleFileUpload($event, 'coverPic')" required>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary m-4">Submit</button>
                        </form>
                        
                        <p v-on:click="this.showAddBook = !this.showAddBook" class="btn btn-info mx-4">Close</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Form to Edit Book -->
    <div v-if="showEditBook">
        <div class="row m-5">
            <div class="col-9">
                <div class="card border-2">
                    <div class="card-body">
                        <div class="text-center">
                            <h1 class="card-title">Edit Book Details</h1>
                        </div>

                        <form action="/admin/edit_book" method="POST" enctype="multipart/form-data" v-on:submit.prevent="editBook(this.bookToEdit.id)">
                            <div class="m-4">
                                <div>
                                    <label class="form-label my-3">Name</label>
                                    <input type="text" class="form-control" v-model="name">
                                </div>

                                <div>
                                    <label class="form-label my-3">Author</label>
                                    <input type="text" class="form-control" v-model="author">
                                </div>

                                <div>
                                    <label class="form-label my-3">Genre</label>
                                    <select v-model="genre" class="form-select">
                                        <option v-for="genre in genreNames" :key="genre.name">{{ genre }}</option>
                                    </select>
                                </div>

                                <div>
                                    <label class="form-label my-3">Description</label>
                                    <textarea class="form-control" v-model="description">Description</textarea>
                                </div>

                                <div>
                                    <label class="form-label my-3">Price (in ₹)</label>
                                    <input type="number" class="form-control" v-model="price">
                                </div>

                                <div>
                                    <label class="form-label my-3">PDF File</label>
                                    <input type="file" class="form-control" v-on:change="handleFileUpload($event, 'pdfFile')">
                                </div>

                                <div>
                                    <label class="form-label my-3">Cover Picture</label>
                                    <input type="file" class="form-control" v-on:change="handleFileUpload($event, 'coverPic')">
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary m-4">Submit</button>
                        </form>
                        
                        <p v-on:click="this.showEditBook = !this.showEditBook" class="btn btn-info mx-4">Close</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <table class="m-5">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Author</th>
            <th>Genre</th>
            <th>Description</th>
            <th>Price</th>
            <th>Action</th>
            <!-- <th>Files</th> -->
        </tr>
        <tr v-for="book in books" :key="book.id">
            <td>{{ book.id }}</td>
            <td>{{ book.name }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.genre }}</td>
            <td>{{ book.description }}</td>
            <td>{{ book.price }}</td>
            <td>
                <button class="btn btn-dark mx-2" v-on:click="editForm(book.id)">Edit</button>
                <button class="btn btn-dark mx-2" v-on:click="deleteBook(book.id)">Delete</button>
            </td>
            <!-- <td>
                <button class="btn btn-dark my-1" v-on:click="openFile(book.pdf_file)">PDF File</button>
                <button class="btn btn-dark" v-on:click="openFile(book.cover_pic)">Cover Picture</button>
            </td> -->
        </tr>
    </table>

    <button class="btn btn-dark mx-5" v-on:click="this.showAddBook = !this.showAddBook">Add New Book</button>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue'
import axios from 'axios';
export default {
    components: {AdminNavbar},
    data() {
        return {
            showAddBook: false,
            showEditBook: false,
            bookToEdit: "",
            books: [],
            name: "",
            author: "",
            genre: "",
            description: "",
            price: "",
            pdfFile: null,
            coverPic: null,
            genreNames: []
        }
    },

    created() {
        this.getBooks();
    },

    methods: {
        getBooks() {
            axios.get("admin/get_books")
            .then((response) => {
                this.books = response.data.books;
                this.genreNames = response.data.genre_names;
                console.log(response.data.books);
                console.log(response.data.genre_names);
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

        handleFileUpload(event, file) {
            if (file === "pdfFile") {
                this.pdfFile = event.target.files[0];
            }
            else if (file === "coverPic") {
                this.coverPic = event.target.files[0];
            }
        },

        addBook() {
            const formData = new FormData();
            formData.append("pdf_file", this.pdfFile);
            formData.append("cover_pic", this.coverPic);
            formData.append("name", this.name);
            formData.append("author", this.author);
            formData.append("genre", this.genre);
            formData.append("description", this.description);
            formData.append("price", this.price)

            axios.post("admin/add_book", formData, {
                headers: {'Content-Type': 'multipart/form-data'}
            })
            .then((response) => {
                this.books = response.data.books;
                console.log(response.data.books);
                this.$toast.success(response.data.msg, {position: "top-right"});
                this.showAddBook = !this.showAddBook;
                this.name = "";
                this.author =  "";
                this.genre = "";
                this.description = "";
                this.price = "";
                this.pdfFile = null;
                this.coverPic = null;

            })
            .catch((error) => {
                this.$toast.error(error.response.data.msg, {position: "top-right"});
                console.log(error.response.data);
            }) 
        },

        openFile(path) {
            this.$router.push(`file:///home/anirudh/Desktop/IIT-M/MAD2_project/code/backend/${path}`)
        },

        editForm(id) {
            this.showEditBook = !this.showEditBook;
            for (let i = 0 ; i < this.books.length ; i++) {
                if (this.books[i].id === id) {
                    this.bookToEdit = this.books[i]
                    break
                }
            }
        },

        editBook(bookID) {
            const formData = new FormData();
            formData.append("pdf_file", this.pdfFile);
            formData.append("cover_pic", this.coverPic);
            formData.append("name", this.name);
            formData.append("author", this.author);
            formData.append("genre", this.genre);
            formData.append("description", this.description);
            formData.append("price", this.price)

            axios.post(`admin/edit_book/${bookID}`, formData, {
                headers: {'Content-Type': 'multipart/form-data'}
            })
            .then((response) => {
                this.books = response.data.books;
                this.$toast.success(response.data.msg, {position: "top-right"});
                this.showEditBook = !this.showEditBook;
            })
            .catch((error) => {
                this.$toast.error(error.response.data.msg, {position: "top-right"});
                console.log(error.response.data)
            })
        },

        deleteBook(bookID) {
            axios.delete(`admin/delete_book/${bookID}`)
            .then((response) => {
                this.books = response.data.books;
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