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
    </div>
  <div class="register-container">
    <h2>Create Account</h2>
    <form @submit.prevent="registerUser" class="register-form">
      <input type="email" v-model="Email" placeholder="Email" required class="input-field" />
      <input type="password" v-model="Password" placeholder="Password" required class="input-field" />
      <button type="submit" class="register-button">Register</button>
    </form>
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p class="login-prompt">
      Already have an account? <router-link to="/login">Login here</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      Email: '',
      Password: '',
      successMessage: ''
    };
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
        alert('Registration failed: ' + error.response.data.message);
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;  /* Full viewport height */
  width: 100vw;   /* Full viewport width */
  padding: 20px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
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

.register-form {
  width: 100%;
  max-width: 400px; /* Set maximum width for the form */
  display: flex;
  flex-direction: column;
  padding: 20px;
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

.register-button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #0056b3;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 10px;
}

.login-prompt {
  margin-top: 20px; /* Add some space above the login prompt */
  text-align: center;
}
</style>
