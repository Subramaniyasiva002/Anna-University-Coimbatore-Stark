<template>
  <div class="dashboard-container p-4">
    <h2 class="text-2xl font-bold mb-4">Real-Time Stock Analysis Dashboard</h2>

    <div class="flex gap-4 mb-6">
      <input 
        v-model="symbol"
        class="border rounded px-4 py-2 w-48"
        placeholder="Enter stock symbol"
        @keyup.enter="subscribeToStock"
      />
      <button 
        @click="subscribeToStock" 
        :disabled="loading"
        class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded disabled:opacity-50 transition-colors"
      >
        {{ loading ? 'Loading...' : 'Track Stock' }}
      </button>
    </div>

    <div v-if="error" class="text-red-500 mb-4 p-3 bg-red-50 rounded">
      {{ error }}
    </div>

    <div v-if="stockData" class="bg-white rounded-lg shadow p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">{{ symbol.toUpperCase() }} Real-Time Data</h3>
        <span class="text-sm text-gray-500">Last updated: {{ formatTime(stockData.timestamp) }}</span>
      </div>

      <div class="chart-container mb-6">
        <canvas ref="chartCanvas"></canvas>
      </div>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="p-4 bg-gray-50 rounded">
          <div class="text-sm text-gray-600">Current Price</div>
          <div class="text-lg font-bold">${{ formatPrice(stockData.current_price) }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded">
          <div class="text-sm text-gray-600">Change</div>
          <div 
            class="text-lg font-bold" 
            :class="stockData.change >= 0 ? 'text-green-500' : 'text-red-500'"
          >
            {{ formatPrice(stockData.change) }} ({{ formatPrice(stockData.percent_change) }}%)
          </div>
        </div>
        <div class="p-4 bg-gray-50 rounded">
          <div class="text-sm text-gray-600">High</div>
          <div class="text-lg font-bold">${{ formatPrice(stockData.high_price) }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded">
          <div class="text-sm text-gray-600">Low</div>
          <div class="text-lg font-bold">${{ formatPrice(stockData.low_price) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from 'socket.io-client';
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  LineController // Add LineController for line charts
} from 'chart.js';

// Register Chart.js components, including LineController
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  LineController // Ensure the LineController is registered
);

export default {
  name: 'Dashboard',
  data() {
    return {
      symbol: '',
      socket: null,
      stockData: null,
      loading: false,
      error: null,
      chart: null,
      priceHistory: [],
      maxDataPoints: 50,
    };
  },
  methods: {
    formatPrice(price) {
      return typeof price === 'number' ? price.toFixed(2) : '0.00';
    },
    formatTime(timestamp) {
      if (!timestamp) return '';
      return new Date(timestamp).toLocaleTimeString();
    },
    initializeSocket() {
      this.socket = io('http://localhost:5173');
      
      this.socket.on('connect', () => {
        console.log('Connected to WebSocket');
      });

      this.socket.on('stock_update', (data) => {
        this.stockData = data;
        this.updateChart(data);
      });

      this.socket.on('error', (error) => {
        this.error = 'WebSocket error: ' + error;
      });
    },
    async subscribeToStock() {
      if (!this.symbol) {
        this.error = 'Please enter a stock symbol';
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        // Unsubscribe from previous symbol if exists
        if (this.stockData && this.stockData.symbol !== this.symbol) {
          this.socket.emit('unsubscribe', { symbol: this.stockData.symbol });
          this.priceHistory = [];
        }

        // Subscribe to new symbol
        this.socket.emit('subscribe', { symbol: this.symbol });
        
      } catch (error) {
        console.error('Error subscribing to stock:', error);
        this.error = 'Failed to subscribe to stock updates';
      } finally {
        this.loading = false;
      }
    },
    updateChart(data) {
      const timestamp = new Date(data.timestamp).toLocaleTimeString();
      
      this.priceHistory.push({
        time: timestamp,
        price: data.current_price
      });

      // Keep only the last maxDataPoints of data
      if (this.priceHistory.length > this.maxDataPoints) {
        this.priceHistory.shift();
      }

      this.renderChart();
    },
    renderChart() {
      const ctx = this.$refs.chartCanvas;

      // Ensure any existing chart is destroyed before creating a new one
      if (this.chart) {
        this.chart.destroy();
      }

      const labels = this.priceHistory.map(d => d.time);
      const prices = this.priceHistory.map(d => d.price);

      // Create a new chart
      this.chart = new Chart(ctx, {
        type: 'line', // Line chart type
        data: {
          labels,
          datasets: [{
            label: `${this.symbol.toUpperCase()} Price`,
            data: prices,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: {
            duration: 0
          },
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: `${this.symbol.toUpperCase()} Real-Time Price`
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              title: {
                display: true,
                text: 'Price ($)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Time (Hourly)'
              }
            }
          }
        }
      });
    }
  },
  mounted() {
    this.initializeSocket();
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
    if (this.socket) {
      this.socket.disconnect();
    }
  }
};
</script>

<style scoped>
/* General layout */
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px; /* Additional padding for spacing */
  background-color: #f4f6f8; /* Light background to separate content from the page */
  border-radius: 10px; /* Rounded container */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); /* Soft shadow for depth */
}

/* Typography and text alignment */
h2 {
  font-size: 2rem;
  color: #1f2937; /* Darker text color for better contrast */
  text-align: center; /* Center the main title */
  margin-bottom: 20px;
}

h3 {
  font-size: 1.5rem;
  color: #374151; /* Darker color for subtitles */
  text-align: left;
}

/* Input and button styling */
input {
  border: 1px solid #d1d5db; /* Light border */
  border-radius: 8px;
  padding: 10px;
  transition: border-color 0.3s ease;
  background-color: #ffffff; /* White background for inputs */
}

input:focus {
  outline: none;
  border-color: #3b82f6; /* Focus border color */
}

button {
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #2563eb; /* Darker blue on hover */
}

/* Stock data display */
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.grid div {
  background-color: #ffffff; /* White cards for stock data */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); /* Soft shadow for card depth */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.grid div:hover {
  transform: translateY(-5px); /* Slight lift on hover */
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1); /* Enhanced shadow on hover */
}

.grid .text-sm {
  color: #6b7280; /* Gray color for small text */
}

.grid .text-lg {
  font-size: 1.25rem;
  font-weight: bold;
  color: #111827; /* Darker color for price and values */
}

/* Chart container */
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  background-color: #f9fafb;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chart-container canvas {
  width: 100% !important;
  height: 100% !important;
}

/* Error message */
.text-red-500 {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  padding: 10px;
  border-radius: 5px;
}

/* Button disabled state */
button:disabled {
  background-color: #9ca3af; /* Gray color for disabled buttons */
  cursor: not-allowed;
}

/* Responsive design */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr); /* 2 columns for smaller screens */
  }
  .chart-container {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .grid {
    grid-template-columns: 1fr; /* 1 column for very small screens */
  }
  h2 {
    font-size: 1.5rem; /* Smaller title for small screens */
  }
}
</style>
