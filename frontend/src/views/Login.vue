
<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <input type="text" v-model="Email" placeholder="Email" required />
      <input type="password" v-model="Password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      Email: '',
      Password: '',
      errorMessage: ''
    }
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          Email: this.Email,
          Password: this.Password
        });
        localStorage.setItem('Email', response.data.Email);
        this.$router.push('/dashboard');
      } catch (error) {
        this.errorMessage = error.response.data.message;
      }
    }
  }
}
</script>