document.addEventListener("DOMContentLoaded", function () {
    const chartElement = document.getElementById("logChart");

    if (!chartElement) {
        return;
    }

    const infoCount = Number(chartElement.dataset.info);
    const warningCount = Number(chartElement.dataset.warning);
    const errorCount = Number(chartElement.dataset.error);

    new Chart(chartElement, {
        type: "pie",

        data: {
            labels: ["Info", "Warning", "Error"],

            datasets: [{
                data: [
                    infoCount,
                    warningCount,
                    errorCount
                ],

                backgroundColor: [
                    "#0d6efd",
                    "#ffc107",
                    "#dc3545"
                ],

                borderColor: "#ffffff",
                borderWidth: 2
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
});