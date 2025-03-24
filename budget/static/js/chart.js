const ctx1 = document.getElementById('transactionChart');

new Chart(ctx1, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: 'Category',
      data: values,
      backgroundColor: [
        'rgba(255, 99, 132, 0.6)',   // Red
        'rgba(54, 162, 235, 0.6)',   // Blue
        'rgba(255, 206, 86, 0.6)',   // Yellow
        'rgba(75, 192, 192, 0.6)',   // Teal
        'rgba(153, 102, 255, 0.6)',  // Purple
        'rgba(255, 159, 64, 0.6)'    // Orange
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',  
        'rgba(54, 162, 235, 1)',  
        'rgba(255, 206, 86, 1)',  
        'rgba(75, 192, 192, 1)',  
        'rgba(153, 102, 255, 1)',  
        'rgba(255, 159, 64, 1)'  
      ],
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      }
    }
  }
});
const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: labels,
    datasets: [{
      label: 'Category',
      data: values,
      backgroundColor: [
        'rgba(255, 99, 132, 0.6)',   // Red
        'rgba(54, 162, 235, 0.6)',   // Blue
        'rgba(255, 206, 86, 0.6)',   // Yellow
        'rgba(75, 192, 192, 0.6)',   // Teal
        'rgba(153, 102, 255, 0.6)',  // Purple
        'rgba(255, 159, 64, 0.6)'    // Orange
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',  
        'rgba(54, 162, 235, 1)',  
        'rgba(255, 206, 86, 1)',  
        'rgba(75, 192, 192, 1)',  
        'rgba(153, 102, 255, 1)',  
        'rgba(255, 159, 64, 1)'  
      ],
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      }
    }
  }
});
