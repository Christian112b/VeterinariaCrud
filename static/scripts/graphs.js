$(document).ready(function () {
    // graphs es la variable de contexto enviada desde Flask
const data = JSON.parse(document.getElementById('graphs-data').textContent);

// 1. Mascotas por especie
let especies = data['graph1'].map(e => e.especie);
let cantidadesEspecie = data['graph1'].map(e => e.cantidad);
Plotly.newPlot('grafico-especie', [{
    x: especies,
    y: cantidadesEspecie,
    type: 'bar',
    marker: { color: 'teal' }
}], {
    title: 'Mascotas por especie',
    xaxis: { title: 'Especie' },
    yaxis: { title: 'Cantidad' }
});

// 2. Mascotas por raza
let razas = data['graph2'].map(e => e.raza);
let cantidadesRaza = data['graph2'].map(e => e.cantidad);
Plotly.newPlot('grafico-raza', [{
    x: razas,
    y: cantidadesRaza,
    type: 'bar',
    marker: { color: 'orange' }
}], {
    title: 'Mascotas por raza',
    xaxis: { title: 'Raza' },
    yaxis: { title: 'Cantidad' }
});

// 3. Mascotas registradas por mes
let meses = data['graph3'].map(e => e.mes);
let cantidadesMes = data['graph3'].map(e => e.cantidad);
Plotly.newPlot('grafico-mascotas-mes', [{
    x: meses,
    y: cantidadesMes,
    type: 'bar',
    marker: { color: 'purple' }
}], {
    title: 'Mascotas registradas por mes',
    xaxis: { title: 'Mes' },
    yaxis: { title: 'Cantidad' }
});

// 4. Distribución de edades de mascotas
let edades = data['graph4'].map(e => e.edad);
let cantidadesEdad = data['graph4'].map(e => e.cantidad);
Plotly.newPlot('grafico-edades', [{
    x: edades,
    y: cantidadesEdad,
    type: 'bar',
    marker: { color: 'green' }
}], {
    title: 'Distribución de edades de mascotas',
    xaxis: { title: 'Edad' },
    yaxis: { title: 'Cantidad' }
});

// 5. Citas por día
let fechas = data['graph5'].map(e => e.fecha);
let cantidadesFecha = data['graph5'].map(e => e.cantidad);
Plotly.newPlot('grafico-citas-dia', [{
    x: fechas,
    y: cantidadesFecha,
    type: 'bar',
    marker: { color: 'blue' }
}], {
    title: 'Citas por día',
    xaxis: { title: 'Fecha' },
    yaxis: { title: 'Cantidad' }
});

// 6. Citas por motivo
let motivos = data['graph6'].map(e => e.motivo);
let cantidadesMotivo = data['graph6'].map(e => e.cantidad);
Plotly.newPlot('grafico-citas-motivo', [{
    x: motivos,
    y: cantidadesMotivo,
    type: 'bar',
    marker: { color: 'red' }
}], {
    title: 'Citas por motivo',
    xaxis: { title: 'Motivo' },
    yaxis: { title: 'Cantidad' }
});
});