<template>
    <UserNavbar/>
    <div class="container-lg">
        <div class="row justify-content-center">
            <div class="col-9">
                <div class="login-form card border-2">
                    <div class="card-body">
                        <div class="text-center">
                            <h1 class="card-title">Login to Opus Books</h1>
                        </div>

                        <form action="/login" method="post" v-on:submit.prevent="userLogin">
                            <div>
                                <label class="form-label my-3">Email</label>
                                <input type="email" class="form-control" v-model="email" required>
                            </div>

                            <div>
                                <label class="form-label my-3">Password</label>
                                <input type="password" class="form-control" v-model="password" required>
                            </div>

                            <button type="submit" class="btn btn-primary my-4">Submit</button>
                        </form>
                        <div v-if="errorMessage" class="my-3" style="color: red">{{ errorMessage }}</div>
                        <router-link to="/register" class="btn btn-danger">Create New Account</router-link>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
import UserNavbar from '@/components/UserNavbar.vue';
export default {
    components: {UserNavbar},
    data () {
        return {
            email: "",
            password: "",
            errorMessage: ""
        }
    },

    methods: {
        userLogin() {
            axios.post("user/login",
                {email: this.email, password: this.password}
            )
            .then((response) => {
                localStorage.setItem("accessToken", response.data.access_token);
                localStorage.setItem("userInfo", JSON.stringify(response.data.user_info));
                this.$router.push("/");
                this.$toast.success("Logged In Successfully", {position: "top-right"});
            })
            .catch((error) => {
                if (error.response) {
                    this.errorMessage = error.response.data.message;
                } else {
                    this.errorMessage = "Login Failed, Please Try Again";
                }
            })
        }
    }
}

</script>

<style scoped>
.login-form {
    /* margin-top: 150px; */
    margin: 150px;
}
</style>