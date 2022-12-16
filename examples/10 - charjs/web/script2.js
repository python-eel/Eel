async function createchart() {

  let result = await eel.dashboard()();
  console.log(result)
  data = {
      labels: [
        'Red',
        'Blue',
        'Yellow'
      ],
      datasets: [{
        label: 'My First Dataset',
        data: [result[0], result[1], result[2]],
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)'
        ],
        hoverOffset: 4
      }]
    };
      config = {
      type: 'doughnut',
      data: data,
    };
  
    myChart = new Chart(document.getElementById('myChart'), config);
    
}
