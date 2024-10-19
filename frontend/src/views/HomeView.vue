<template>
  <div class="homepage">
    <header class="header">
      <nav class="navbar">
        <a class="brand-logo" style="font-weight: bold;">
          <span class="fa fa-gg"></span>STARK
        </a>
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

  <main class="main-content">
    <p class="headline">Get Insights, Track Trends, and Stay Ahead of the Market</p>
    <p class="know">Knowledge is the new currency, so invest wisely...</p>
    <router-link to="/login" class="try-now-button">Try Now</router-link>
   
  </main>


    <footer class="footer">
      <div class="footer-content">
        <div class="company-info">
          <p>Company Name: STARK</p>
          <p>Year Established: 2024</p>
          <p>Copyright Notice: © 2024 STARK. All rights reserved.</p>
        </div>
        <div class="social-media">
          <p>Follow Us:</p>
          <ul>
            <li><a href="https://www.facebook.com" target="_blank">Facebook</a></li> <br>
            <li><a href="https://www.twitter.com" target="_blank">Twitter</a></li> <br>
            <li><a href="https://www.instagram.com" target="_blank">Instagram</a></li> <br>
            <li><a href="https://www.linkedin.com" target="_blank">LinkedIn</a></li> <br>
          </ul>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: ''
    };
  },
  methods: {
    onSubmit() {
      // Handle search query submission
      console.log("Search query:", this.searchQuery);
    }
  }
}
</script>

<style scoped>
/* General styles for the homepage */
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

.main-content {
  margin-top: 0px;
  display: flex;
  flex-direction: column; /* Stack elements vertically */
  justify-content: center;
  align-items: center;
  background-image: url('@/assets/bgim (2).jpg'); /* Background image */
  background-size: cover;
  background-position: center;
  padding: 20px;
  min-height: 100vh; /* Full viewport height */
  width: 100%;
  overflow-y: auto;
  position: relative;
    opacity: 0.7; /* Adjust opacity here */

}

/* Headline styles */
.headline {
  font-size: 0.5em;
  color: #210715;
  text-align: center;
  margin-bottom: 20px; /* Space below the headline */
}
.know{
  font-weight:bold;
}

/* Try Now button styles */
.try-now-button {
  display: inline-block; /* Block level to ensure it appears on a new line */
  padding: 10px 20px;
  font-size: 1.2em;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px; /* Space above the button */
}

.try-now-button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}
.try-now-button:hover {
  background-color: #0056b3;
}

/* Pseudo-element for reducing image opacity */


.headline {
  font-weight: bold; /* Make the text bold */
  font-size: 2em; /* Increase font size */
  color: #090e13; /* Adjust color to stand out on the background */
  margin-top: 0px; /* Optional: adjust vertical spacing */
}

.footer {
  background-color: #e0e0e3;
  padding: 20px;
  display: flex; /* Use flexbox for layout */
  justify-content: space-between; /* Space between left and right */
  align-items: center; /* Center items vertically */
  flex-wrap: wrap; /* Allow items to wrap if necessary */
}

.footer-content {
  max-width: 1200px; /* Set maximum width for the footer content */
  margin: 0 auto; /* Center the content horizontally */
  width: 100%; /* Full width */
  display: flex; /* Use flexbox for footer content */
  justify-content: space-between; /* Space out company info and social media */
}

.company-info {
  flex: 1; /* Allow this section to grow */
  text-align: left; /* Align text to the left */
}

.social-media {
  flex: 1; /* Allow this section to grow */
  text-align: right; /* Align text to the right */
}

.social-media ul {
  list-style: none; /* Remove bullet points */
  padding: 0; /* Remove default padding */
  margin: 0; /* Remove default margin */
}

.social-media li {
  display: inline; /* Display links inline */
  margin: 0 10px; /* Space between links */
}

.social-media a {
  text-decoration: none; /* Remove underline */
  color: #007bff; /* Link color */
}

.social-media a:hover {
  text-decoration: underline; /* Underline on hover */
}

/* Media queries for responsiveness */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: center;
  }

  .nav-links {
    flex-direction: column;
    align-items: center;
  }

  .nav-links li {
    margin: 10px 0;
  }

  .main-content {
    padding: 10px;
  }
}

@media (max-width: 480px) {
  .nav-links {
    font-size: 1em;
  }

  .main-content {
    font-size: 1em;
  }

  .footer {
    font-size: 1em;
  }
}
</style>
