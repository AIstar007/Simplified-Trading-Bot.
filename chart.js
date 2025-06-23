const priceCtx = document.getElementById('priceChart').getContext('2d');
const rsiCtx = document.getElementById('rsiChart').getContext('2d');

let priceChart;
let rsiChart;
let latestData = [];

const smaCheckbox = document.getElementById('toggleSMA');
const emaCheckbox = document.getElementById('toggleEMA');
const rsiCheckbox = document.getElementById('toggleRSI');
const exportBtn = document.getElementById('exportCSV');

async function fetchPriceData() {
  const res = await fetch('/price_data');
  const data = await res.json();
  latestData = data;

  const labels = data.map(item => new Date(item.time).toLocaleTimeString());
  const close = data.map(item => item.close);
  const sma = data.map(item => item.SMA20);
  const ema = data.map(item => item.EMA20);
  const rsi = data.map(item => item.RSI);

  if (priceChart) priceChart.destroy();
  if (rsiChart) rsiChart.destroy();

  const datasets = [
    {
      label: 'Close Price',
      data: close,
      borderColor: '#00BFFF',
      backgroundColor: 'transparent',
      borderWidth: 2,
      pointRadius: 0
    }
  ];

  if (smaCheckbox.checked) {
    datasets.push({
      label: 'SMA (20)',
      data: sma,
      borderColor: '#FFD700',
      backgroundColor: 'transparent',
      borderWidth: 1,
      pointRadius: 0
    });
  }
  if (emaCheckbox.checked) {
    datasets.push({
      label: 'EMA (20)',
      data: ema,
      borderColor: '#FF69B4',
      backgroundColor: 'transparent',
      borderWidth: 1,
      pointRadius: 0
    });
  }

  priceChart = new Chart(priceCtx, {
    type: 'line',
    data: {
      labels,
      datasets
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: 'white' } }
      },
      scales: {
        x: { ticks: { color: 'white' } },
        y: { ticks: { color: 'white' } }
      }
    }
  });

  if (rsiCheckbox.checked) {
    rsiChart = new Chart(rsiCtx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'RSI (14)',
            data: rsi,
            borderColor: '#32CD32',
            borderWidth: 2,
            backgroundColor: 'transparent',
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { labels: { color: 'white' } }
        },
        scales: {
          x: { ticks: { color: 'white' } },
          y: {
            ticks: { color: 'white' },
            suggestedMin: 0,
            suggestedMax: 100,
            grid: { color: 'rgba(255,255,255,0.1)' }
          }
        }
      }
    });

    const lastRSI = rsi[rsi.length - 1];
    if (lastRSI >= 70 || lastRSI <= 30) {
      notifyUser(`⚠️ RSI Alert: RSI = ${lastRSI.toFixed(2)}`);
    }
  }
}

function notifyUser(message) {
  if (Notification.permission === 'granted') {
    new Notification('Trading Bot Alert', { body: message });
  } else if (Notification.permission !== 'denied') {
    Notification.requestPermission().then(permission => {
      if (permission === 'granted') {
        new Notification('Trading Bot Alert', { body: message });
      }
    });
  }
}

function exportToCSV() {
  if (!latestData.length) return;
  const headers = Object.keys(latestData[0]).join(',');
  const rows = latestData.map(row => Object.values(row).join(','));
  const csvContent = [headers, ...rows].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", "price_data.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

smaCheckbox.addEventListener('change', fetchPriceData);
emaCheckbox.addEventListener('change', fetchPriceData);
rsiCheckbox.addEventListener('change', fetchPriceData);
exportBtn.addEventListener('click', exportToCSV);

fetchPriceData();
setInterval(fetchPriceData, 60000);