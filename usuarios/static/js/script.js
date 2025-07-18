document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('plant-data');

    fetch('/api/plant-data')
        .then(response => {
        if (!response.ok) throw new Error('Error en la petición: ' + response.status);
        return response.json();
        })
        .then(data => {
        const info = data.data[0].dataItemMap;
        const html = `
            <p>🔋 Potencia diaria (day_power): ${info.day_power ?? 'N/A'} kWh</p>
            <p>📅 Potencia mensual (month_power): ${info.month_power ?? 'N/A'} kWh</p>
            <p>⚡ Potencia total (total_power): ${info.total_power ?? 'N/A'} kWh</p>
            <p>🔌 Energía utilizada hoy (day_use_energy): ${info.day_use_energy ?? 'N/A'} kWh</p>
        `;
        container.innerHTML = html;
        })
        .catch(error => {
        container.innerHTML = `<p style="color: red;">Error al cargar datos: ${error.message}</p>`;
        });
    });