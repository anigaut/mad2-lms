import axios from 'axios';

export function isLoggedIn() {
    if (localStorage.getItem("accessToken")) {
        return true
    } else {
        return false
    }
}
