<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <input type="text" v-model="Email" placeholder="Eamil" required />
      <input type="password" v-model="Password" placeholder="Password" required />
      <button type="submit">Register</button>
    </form>
    <p v-if="successMessage">{{ successMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      Email: '',
      Password: '',
      successMessage: ''
    }
  },
  methods: {
    async registerUser() {
      try {
        await axios.post('http://127.0.0.1:5000/register', {
          Email: this.Email,
          Password: this.Password
        });
        this.successMessage = "User registered successfully!";
        this.$router.push('/login');
      } catch (error) {
        alert('Registration failed');
      }
    }
  }
}
</script>