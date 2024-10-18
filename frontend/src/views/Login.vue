<template>
  <div class="homepage">
    <header class="header">
      <nav class="navbar">
        <a class="brand-logo" style="font-weight: bold;"><span class="fa fa-gg"></span>STARK</a>
        <ul class="nav-links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/login">Login</router-link></li>
          <li><router-link to="/register">Register</router-link></li>
          <li><router-link to="/contact">Contact</router-link></li>
        </ul>
        <form @submit.prevent="onSubmit" class="form-inline position-relative my-2 my-lg-0">
          <input 
            v-model="searchQuery" 
            class="form-control search" 
            type="search" 
            placeholder="Search here..." 
            aria-label="Search" 
            required
          />
        </form>
      </nav>
    </header>

    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="loginUser" class="login-form">
        <input type="text" v-model="Email" placeholder="Email" required class="input-field" />
        <input type="password" v-model="Password" placeholder="Password" required class="input-field" />
        <button type="submit" class="login-button">Login</button>
      </form>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p class="sign-up-prompt">
        If you don't have an account, <router-link to="/register">Sign Up</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: '',
      Email: '',
      Password: '',
      errorMessage: '',
      searchQuery: ''
    };
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
    },
    onSubmit() {
      // Add your search functionality here
      console.log(this.searchQuery);
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;  /* Center vertically */
  align-items: center;      /* Center horizontally */
  height: 100vh;           /* Full viewport height */
  width: 100vw;            /* Full viewport width */
  padding: 20px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.homepage {
  font-family: sans-serif;
  color: #333;
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow-x: hidden;
}

/* Header styles */
.header {
  background-color: #e0e0e3;
  padding: 20px;
  text-align: center;
  flex-shrink: 0;
}

.navbar {
  display: flex;
  justify-content: space-between; /* Space between brand logo and links */
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.brand-logo {
  text-decoration: none;
  color: black;
  font-size: 1.5em;
}

.nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-links li {
  margin: 0 15px;
}

.nav-links a {
  text-decoration: none;
  color: #000;
  font-size: 1.2em;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #555;
}

.login-form {
  width: 100%;
  max-width: 400px; /* Set maximum width for the form */
  display: flex;
  flex-direction: column;
  padding: 20px;
  justify-content: center; /* Center content inside the form */
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.input-field {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.login-button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.sign-up-prompt {
  margin-top: 20px; /* Add some space above the sign-up prompt */
}
</style>
