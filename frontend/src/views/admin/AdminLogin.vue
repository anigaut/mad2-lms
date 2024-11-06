<template>
    <div class="container-lg">
        <div class="row justify-content-center">
            <div class="col-9">
                <div class="login-form card border-2">
                    <div class="card-body">
                        <div class="text-center">
                            <h1 class="card-title">Login to Opus Admin Account</h1>
                        </div>

                        <form action="admin/login" method="post" v-on:submit.prevent="adminLogin">
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
                        <!-- <router-link to="admin/register" class="btn btn-danger">Create New Account</router-link> -->
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data () {
        return {
            email: "",
            password: "",
            errorMessage: ""
        }
    },

    methods: {
        adminLogin() {
            axios.post("admin/login", {
                email: this.email,
                password: this.password
            })
            .then((response) => {
                localStorage.setItem('accessToken', response.data.access_token);
                localStorage.setItem('adminInfo', JSON.stringify(response.data.admin_info));
                this.$toast.success("Logged In Successfully",{position: "top-right"});
                this.$router.push('/admin');
            })
            .catch((error) => {
                if(error.response) {
                    this.errorMessage = error.response.data.message;
                } else {
                    this.errorMessage = "Login Failed, Please try again";
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