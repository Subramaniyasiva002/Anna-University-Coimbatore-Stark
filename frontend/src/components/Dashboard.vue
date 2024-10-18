<template>
  <div>
    <h2>Stock Data</h2>
    <div v-if="stock">
      <p>Symbol: {{ stock.symbol }}</p>
      <p>Name: {{ stock.name }}</p>
      <p>P/E Ratio: {{ stock.pe_ratio }}</p>
      <p>P/B Ratio: {{ stock.pb_ratio }}</p>
    </div>
    <button @click="fetchStockData">Get Stock Data</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stock: null
    };
  },
  methods: {
    async fetchStockData() {
      const response = await fetch('/api/stock/AAPL');
      const data = await response.json();
      this.stock = data;
    }
  }
};
</script>
