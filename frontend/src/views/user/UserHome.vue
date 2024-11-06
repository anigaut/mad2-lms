<template>
      <UserNavbar/>
      <div class="container-lg">
            <div class="row m-5">
              <h2 class="mt-5">Best Sellers</h2> <hr>
                <div class="card-container">
                    <div v-for="book in books[0]" :key="book.id">
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

            <div class="row m-5">
              <h2 class="mt-3">Editors' Choice</h2> <hr>
                <div class="card-container">
                    <div v-for="book in books[1]" :key="book.id">
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
</template>

<script>
import UserNavbar from '@/components/UserNavbar.vue'
import axios from 'axios';
export default {  
  components: {UserNavbar},

  data () {
    return {
      errorMessage: "",
      text: "MAD2 Project Home",
      books: []
    }
  },

  created() {
      this.userHome();
    },

  methods: {
    userHome() {
      axios.get("user/home")
      .then((response) => {
          this.books = response.data.books;
          console.log(response.data.books);
      })
      .catch((error) => {
        console.log(error.response.data);
      })
    },

    viewBook(bookID) {
      this.$router.push(`/books/${bookID}`);
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