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
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>
