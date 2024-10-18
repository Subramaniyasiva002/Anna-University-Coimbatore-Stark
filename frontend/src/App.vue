<template>
  <div id="app">
    <header>
      <h1>User Authentication App</h1>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
        <button v-if="isAuthenticated" @click="logout">Logout</button>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: false,
    }
  },
  created() {
    // Check if user is authenticated by checking local storage
    this.isAuthenticated = !!localStorage.getItem('username');
  },
  methods: {
    logout() {
      // Call the logout API
      fetch('http://localhost:5000/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => {
        if (response.ok) {
          localStorage.removeItem('username');
          this.isAuthenticated = false;
          this.$router.push('/login');
        }
      })
      .catch(error => {
        console.error('Error logging out:', error);
      });
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

header {
  background: #42b983;
  padding: 10px;
  color: white;
}

nav {
  margin-bottom: 20px;
}

nav a {
  margin: 0 10px;
  color: white;
  text-decoration: none;
}

nav button {
  margin-left: 10px;
  cursor: pointer;
}
</style>
