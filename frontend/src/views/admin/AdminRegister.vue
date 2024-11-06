<template>
    <UserNavbar/>
    <div class="main">
        <div class="container-lg">
            <div class="registration-form row justify-content-center" style="margin: 50px 150px;">
                <div class="col-9">
                    <div class="card border-2">
                        <div class="card-body">
                            <div class="text-center">
                                <h1 class="card-title">Create your Opus Admin Account</h1>
                                <p class="lead">Already an Admin? Login <router-link to="/login">here</router-link></p>
                            </div>

                            <form action="admin/register" method="post" v-on:submit.prevent="adminRegister">
                                <div>
                                    <label class="form-label my-4">First Name</label>
                                    <input type="text" class="form-control" v-model="firstName" required>
                                </div>

                                <div>
                                    <label class="form-label my-4">Last Name</label>
                                    <input type="text" class="form-control" v-model="lastName"> 
                                </div>

                                <div>
                                    <label class="form-label my-4">Email (Must End With @opus.com)</label>
                                    <input type="email" name="email" class="form-control" v-model="email" required v-on:input="validEmailEnding">
                                </div>

                                <div v-if="this.email && !validEmail" class="my-3" style="color: red;">Your email must end with "@opus.com"</div>

                                <div>
                                    <label class="form-label my-4">Password</label>
                                    <input type="password" class="form-control" v-model="password" required>
                                </div>

                                <div>
                                    <label class="form-label my-4">Confirm Password</label>
                                    <input type="password" class="form-control" v-model="confirmPassword" required>
                                </div>

                                <div v-if="this.confirmPassword && this.password!==this.confirmPassword" class="my-3" style="color: red;">Passwords do not match</div>

                                <button type="submit" class="btn btn-primary mt-4" v-bind:disabled="this.password!==this.confirmPassword">Submit</button>
                            </form>
                            <div v-if="errorMessage" class="my-3" style="color: red">{{ errorMessage }}</div>
                        </div>
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
            errorMessage: "",
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            confirmPassword: "",
            validEmail: false
        }
    },
    methods: {
        validEmailEnding () {
            if(this.email.endsWith("@opus.com")) {
                this.validEmail = true;
            } else {
                this.validEmail = false;
            };
        },
        adminRegister() {
            axios.post("admin/register", {
                firstName: this.firstName,
                lastName: this.lastName,
                email: this.email,
                password: this.password
            })
            .then((response) => {
                localStorage.setItem("accessToken", response.data.access_token);
                localStorage.setItem("adminInfo", response.data.admin_info);
                this.$router.push('/admin');
            })
            .catch((error) => {
                if (error.response) {
                    this.errorMessage = error.response.data.message;
                } else {
                    this.errorMessage = "Something went wrong";
                }
            })
        }
    }
}
</script>