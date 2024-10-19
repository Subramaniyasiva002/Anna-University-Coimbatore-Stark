<template>
  <div id="app">
    
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

